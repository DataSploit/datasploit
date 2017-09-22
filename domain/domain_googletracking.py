#!/usr/bin/env python

import base
import config as cfg
import re
import requests
import sys
from config import spyonweb_access_token
from termcolor import colored

ENABLED = True

'''
Author: @khasmek

Original Idea: @jms_dot_py

Original article -
# Tried putting on HTTPS, but the CERT is broken on this website.
http://www.automatingosint.com/blog/2017/07/osint-website-connections-tracking-codes/

Original code -
https://github.com/automatingosint/osint_public/blob/master/trackingcodes/website_connections.py
'''


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n[+] Checking for Google tracking codes.\n' +
                  style.END, 'blue')


def clean_tracking_code(tracking_code):
    if tracking_code.count("-") > 1:
        return tracking_code.rsplit("-",1)[0]
    else:
        return tracking_code


def extract_tracking_codes(domain):
    tracking_codes = []
    connections = {}
    try:
        if not domain.startswith("http:"):
            site = "http://" + domain
        response = requests.get(site)
    except:
        connections['err'] = str(colored(style.BOLD +
                                 '\n[!] Failed to reach site.\n' + style.END, 'red'))
        return connections

    extracted_codes = []
    google_adsense_pattern   = re.compile("pub-[0-9]{1,}", re.IGNORECASE)
    google_analytics_pattern = re.compile("ua-\d+-\d+", re.IGNORECASE)
    extracted_codes.extend(google_adsense_pattern.findall(response.content))
    extracted_codes.extend(google_analytics_pattern.findall(response.content))
    for code in extracted_codes:
        code = clean_tracking_code(code)
        if code.lower() not in tracking_codes:
            if code not in connections.keys():
                connections[code] = [domain]
            else:
                connections[code].append(domain)

    return connections


def spyonweb_request(data,request_type="domain"):
    params = {}
    params['access_token'] = spyonweb_access_token
    response = requests.get('https://api.spyonweb.com/v1/' +
                            request_type + '/' + data, params=params)
    if response.status_code == 200:
        result = response.json()
        if result['status'] != "not_found":
            return result

    return None


def spyonweb_analytics_codes(connections):
    for code in connections:
        if code.lower().startswith("pub"):
            request_type = "adsense"
        elif code.lower().startswith("ua"):
            request_type = "analytics"
        results = spyonweb_request(code,request_type)
        if results:
            # the free tier is limited, account for this.
            if 'message' in results:
                if results['message'] == 'request quota exceeded':
                    error = 'conn refused'
                    connections[code].append(error)
            else:
                for domain in results['result'][request_type][code]['items']:
                    connections[code].append(domain)

    return connections


def main(domain):
    if spyonweb_access_token != "XYZ" and spyonweb_access_token != "":
        connections = extract_tracking_codes(domain)
        if 'err' in connections:
            return [ connections ]
        else:
            if len(connections.keys()):
                common_domains = {}
                tracking_codes = {}
                tracking_codes['Tracking Codes'] = connections.keys()
                dirty_domains = spyonweb_analytics_codes(connections)
                for k, v in dirty_domains.items():
                    common_domains[k] = (sorted(set(v)))
                return [ common_domains, tracking_codes ]
            else:
                return [ colored(style.BOLD + '\n[!] No tracking codes found!\n' +
                                 style.END, 'red') ]
    else:
        return [ colored(style.BOLD +
                         '[!] Error: No SpyOnWeb API token found. Skipping' +
                         style.END, 'red') ]


def output(data, domain=""):
    for i in data:
        try:
            for k, v in i.items():
                if k == 'err':
                    print '\n ERRORS:'
                    print v
                elif k == 'Tracking Codes':
                    print '\n' + k + ':'
                    for code in v:
                        print '\t' + str(code)
                else:
                    if 'conn refused' in v:
                        print colored(style.BOLD +
                                      '\n[!] Error: Connection requests exceeded!\n' +
                                      style.END, 'red')
                    print k + ':'
                    for url in v:
                        if url == 'conn refused':
                            v.remove('conn refused')
                        else:
                            print '\t' + str(url)
        except:
            print i
            data.remove(i)


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
