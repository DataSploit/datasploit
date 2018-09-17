#!/usr/bin/env python2

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
WRITE_TEXT_FILE = True
MODULE_NAME = "Domain_subdomains"


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

def check_and_append_other_domains(other_domain, other_related_domain_list):
    if other_domain not in other_related_domain_list:
        other_related_domain_list.append(other_domain)
    return other_related_domain_list

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
    req1 = requests.get("http://searchdns.netcraft.com/?host=%s" % domain)
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
                    url = "http://searchdns.netcraft.com/?host=%s&last=%s&from=%s&restriction=site%%20contains" % (
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


def ct_search(domain, subdomain_list, wildcard=True):

    '''
    ###################################################################
    Credits:
    This Code has been picked from @paulwebsec's git repo crt.sh.  
    https://github.com/PaulSec/crt.sh/blob/master/crtsh.py

    Please say Hi to him, We all love him :) 

    Few changes made:
        1. Removing class structure.
        2. Instead of passing all fields, just passing subdomain
        3. Checking for repeated subdomain entries 
    ###################################################################
    '''
    print colored(' [+] Extracting subdomains from Certificate Transparency Reports\n', 'blue')
    subdomain_list_tmp = []

    base_url = "https://crt.sh/?q="
    if wildcard:
        base_url += "%25."
    base_url += domain

    ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 ' + \
        'Firefox/40.1'
    r = requests.get(url=base_url, headers={'User-Agent': ua})

    if r.ok:
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            table = soup.findAll('table')[2]
            rows = table.find_all(['tr'])
            for row in rows:
                cells = row.find_all('td', limit=5)
                if cells:
                    '''tmp = {
                                                                                                'crtsh_id': cells[0].text,
                                                                                                'pem_url': 'https://crt.sh/?d=' + cells[0].text,
                                                                                                'logged_at': cells[1].text,
                                                                                                'not_before': cells[2].text,
                                                                                            }'''
                    tmp = {}
                    if wildcard:
                        tmp['domain'] = cells[3].text
                        #tmp['issuer'] = cells[4].text
                    else:
                        tmp['domain'] = domain,
                        #tmp['issuer'] = cells[3].text
                    check_and_append_subdomains(tmp['domain'], subdomain_list)
                    #subdomain_list_tmp.append(tmp)
        except IndexError:
            print("Error retrieving information.")

    return subdomain_list_tmp




'''def find_domains_from_next_page_ct(page_identifier, domain, subdomain_list, other_related_domain_list):
    url = "https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch/page?p=%s" % page_identifier
    req2 = requests.get(url)
    obj2 = req2.text
    new_obj2= obj2.replace(")]}'\n\n", '')
    dd2 = json.loads(new_obj2)
    details2 = dd2[0][1]
    for x in details2:
        if "*" in x[1]:
            x[1] = x[1].replace("*.", "")
        if x[1].endswith(domain):
            subdomain_list = check_and_append_subdomains(x[1], subdomain_list)
        else:
            other_related_domain_list = check_and_append_other_domains(x[1], other_related_domain_list)
    try:
        nextpage_details = dd2[0][3]
        if nextpage_details[3] != nextpage_details[4]:
            page_identifier = nextpage_details[1]
            find_domains_from_next_page_ct(page_identifier, domain, subdomain_list, other_related_domain_list)
    except:
        pass

def subdomains_from_google_ct(domain, subdomain_list, other_related_domain_list):
    print colored(' [+] Extracting subdomains from Certificate Transparency Reports\n', 'blue')
    url = 'https://transparencyreport.google.com/transparencyreport/api/v3/httpsreport/ct/certsearch?include_expired=true&include_subdomains=true&domain=%s' % (domain)
    req = requests.get(url)
    obj = req.text
    new_obj= obj.replace(")]}'\n\n", '')
    dd = json.loads(new_obj)
    details = dd[0][1]
    for x in details:
        if "*" in x[1]:
            x[1] = x[1].replace("*.", "")
        if x[1].endswith(domain):
            subdomain_list = check_and_append_subdomains(x[1], subdomain_list)
        else:
            other_related_domain_list = check_and_append_other_domains(x[1], other_related_domain_list)

    try:
        nextpage_details = dd[0][3]
        if nextpage_details[3] != nextpage_details[4]:
            page_identifier = nextpage_details[1]
            find_domains_from_next_page_ct(page_identifier, domain, subdomain_list, other_related_domain_list)
    except:
        pass
    return subdomain_list, other_related_domain_list'''

def subdomains_from_dnstrails(domain, subdomain_list):
    print colored(' [+] Extracting subdomains from DNSTrails\n', 'blue')
    url = 'https://app.securitytrails.com/api/domain/info/' + domain
    headers = {
        'User-Agent': 'Mozilla/5.0 Firefox/57.0',
        'Referer': 'https://dnstrails.com/',
        'Origin': 'https://dnstrails.com',
        'DNT': '1',
    }
    req = requests.get(url, headers=headers)
    if req.status_code == 200:
        data = json.loads(req.text)
        if 'result' in data and 'subdomains' in data['result'] and len(data['result']['subdomains']) != 0:
            subdomains_new = data['result']['subdomains']
            for a in range(0, len(subdomains_new)):
                subdomains_new[a] = subdomains_new[a] + '.' + domain
                #print subdomains_new[a]
                subdomain_list = check_and_append_subdomains(subdomains_new[a], subdomain_list)
        else:
            print colored(' [!] {}\n'.format(data['error']), 'yellow')
    else:
        print colored(' [+] DNSTrails API rate limit exceeded\n', 'yellow')
    return subdomain_list

def banner():
    print colored(style.BOLD + '---> Finding subdomains, will be back soon with list. \n' + style.END, 'blue')


def main(domain):
    time.sleep(0.3)
    subdomain_list = []
    other_related_domain_list = []
    subdomain_list = subdomains(domain, subdomain_list)
    subdomain_list = subdomains_from_netcraft(domain, subdomain_list)
    #subdomain_list, other_related_domain_list = subdomains_from_google_ct(domain, subdomain_list, other_related_domain_list)
    subdomains_from_ct = ct_search(domain, subdomain_list)
    subdomain_list = subdomains_from_dnstrails(domain, subdomain_list)
    # not printing list of 'other_related_domain_list' anywhere. This is done for later changes.
    return subdomain_list


def output(data, domain=""):
    print colored("List of subdomains found\n", 'green')
    for sub in data:
	if not re.match("\d{4}-\d{2}-\d{2}", sub):
            print sub


def output_text(data):
	ret_out = []
	for sub in data:
        	if not re.match("\d{4}-\d{2}-\d{2}", sub):
        		ret_out.append(sub)
	return "\n".join(ret_out)


if __name__ == "__main__":
    if len(sys.argv) != 0:
        #try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
        #except Exception as e:
    else:
        print "Please provide a domain name as argument"
