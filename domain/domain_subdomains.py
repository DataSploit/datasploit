#!/usr/bin/env python

import base
import sys
import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored
import time
import warnings
import json

warnings.filterwarnings("ignore")

ENABLED = True


'''
Author(s): @upgoingstar & @khasmek
'''

class style:
    BOLD = '\033[1m'
    END = '\033[0m'



def check_and_append_subdomains(subdomain, subdomain_list):
    if subdomain not in subdomain_list:
        subdomain_list.append(subdomain)
    return subdomain_list


def subdomains(domain, subdomain_list):
    print colored(' [+] Extracting subdomains from DNS Dumpster\n', 'blue')
    r = requests.get("https://dnsdumpster.com/", verify=False)
    cookies = {}
    if 'csrftoken' in r.cookies.keys():
        cookies['csrftoken'] = r.cookies['csrftoken']
        data = {}
        data['csrfmiddlewaretoken'] = cookies['csrftoken']
        data['targetip'] = domain
        headers = {}
        headers['Referer'] = "https://dnsdumpster.com/"
        req = requests.post("https://dnsdumpster.com/", data=data, cookies=cookies, headers=headers, verify=False)
        soup = BeautifulSoup(req.content, 'lxml')
        subdomains_new = soup.findAll('td', {"class": "col-md-4"})
        for subd in subdomains_new:
            if domain in subd.text:
                subdomain_list = check_and_append_subdomains(subd.text.split()[0], subdomain_list)
    return subdomain_list


def subdomains_from_netcraft(domain, subdomain_list):
    print colored(' [+] Extracting subdomains Netcraft\n', 'blue')
    target_dom_name = domain.split(".")
    req1 = requests.get("https://searchdns.netcraft.com/?host=%s" % domain)

    #The page still shows HTTP in the HTML body, so this regex needs to staty at HTTP.
    link_regx = re.compile('<a href="http://toolbar.netcraft.com/site_report\?url=(.*)">')
    links_list = link_regx.findall(req1.content)
    for x in links_list:
        dom_name = x.split("/")[2].split(".")
        if (dom_name[len(dom_name) - 1] == target_dom_name[1]) and (dom_name[len(dom_name) - 2] == target_dom_name[0]):
            subdomain_list = check_and_append_subdomains(x.split("/")[2], subdomain_list)
    num_regex = re.compile('Found (.*) site')
    num_subdomains = num_regex.findall(req1.content)
    if not num_subdomains:
        num_regex = re.compile('First (.*) sites returned')
        num_subdomains = num_regex.findall(req1.content)
    if num_subdomains:
        if num_subdomains[0] != str(0):
            num_pages = int(num_subdomains[0]) / 20 + 1
            if num_pages > 1:
                last_regex = re.compile(
                    '<td align="left">%s.</td><td align="left">\n<a href="(.*)" rel="nofollow">' % (20))
                last_item = last_regex.findall(req1.content)[0].split("/")[2]
                next_page = 21

                for x in range(2, num_pages):
                    url = "https://searchdns.netcraft.com/?host=%s&last=%s&from=%s&restriction=site%%20contains" % (
                        domain, last_item, next_page)
                    req2 = requests.get(url)
                    link_regx = re.compile('<a href="http://toolbar.netcraft.com/site_report\?url=(.*)">')
                    links_list = link_regx.findall(req2.content)
                    for y in links_list:
                        dom_name1 = y.split("/")[2].split(".")
                        if (dom_name1[len(dom_name1) - 1] == target_dom_name[1]) and (
                                    dom_name1[len(dom_name1) - 2] == target_dom_name[0]):
                            subdomain_list = check_and_append_subdomains(y.split("/")[2], subdomain_list)
                    last_item = links_list[len(links_list) - 1].split("/")[2]
                    next_page = 20 * x + 1
        else:
            pass
    else:
        pass
    return subdomain_list

def subdomains_from_google_ct(domain, subdomain_list):
    print colored(' [+] Extracting subdomains from Certificate Transparency Reports\n', 'blue')
    next = ''
    while True:
        url = 'https://www.google.com/transparencyreport/jsonp/ct/search?domain=%s&incl_exp=true&incl_sub=true&token=%s&c=' % (domain,next)
        obj = json.loads('('.join(requests.get(url).text.split('(')[1:])[:-3])
        for x in obj['results']:
            if x['subject'].endswith(domain):
                subdomain_list = check_and_append_subdomains(x['subject'], subdomain_list)
        if 'nextPageToken' not in obj:
            break
        next = obj['nextPageToken']
    return subdomain_list


def banner():
    print colored(style.BOLD + '---> Finding subdomains, will be back soon with list. \n' + style.END, 'blue')


def main(domain):
    time.sleep(0.3)
    subdomain_list = []
    subdomain_list = subdomains(domain, subdomain_list)
    subdomain_list = subdomains_from_netcraft(domain, subdomain_list)
    subdomain_list = subdomains_from_google_ct(domain, subdomain_list)
    return subdomain_list


def output(data, domain=""):
    print colored("List of subdomains found\n", 'green')
    for sub in data:
        print sub


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
