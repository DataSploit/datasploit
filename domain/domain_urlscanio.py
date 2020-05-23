#!/usr/bin/env python

import base
import json
import requests
import time
import vault
import sys

from termcolor import colored


# Control whether the module is enabled or not
ENABLED = True

# Set alternative UserAgent, if desired, here.
custom_agent = 'DataSploit - (https://github.com/DataSploit/datasploit)'


def banner():
    print((colored(base.style.BOLD + '\n[+] Scanning with urlscan.io.\n' +
                  base.style.END, 'blue')))


def build_headers(user_agent='', referer=''):
    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['API-key'] = vault.get_key('urlscanio_api')
    return headers


# We'll allow setting referer urls and public scans if using DataSploit as a
# module, but is otherwise hidden from the cli portion for ease of use.
def start_scan(domain, headers, public_scan=False, custom_agent='', referer=''):
    data = {}
    data['url'] = domain
    if public_scan:
        data['public'] = 'on'
    if custom_agent:
        data['customagent'] = custom_agent
    if referer:
        data['referer'] = referer
    r = requests.post("https://urlscan.io/api/v1/scan/",
                      headers=headers,
                      data=json.dumps(data))
    return r


def get_results(uuid):
    url = 'https://urlscan.io/api/v1/result/{}'.format(uuid)
    not_completed = True
    while not_completed:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                not_completed = False
                return r
            else:
                time.sleep(10)
        except requests.exceptions.ConnectionError:
            print((colored(base.style.BOLD + " [!] COULD NOT CONNECT TO URLSCAN.IO" +
                  base.style.END, 'red')))
            sys.exit(0)


def main(domain):
    headers = build_headers()
    if custom_agent:
        scan = start_scan(domain, headers, custom_agent=custom_agent).json()
    else:
        scan = start_scan(domain, headers).json()
    # No need to check for a completed scan immediately.
    time.sleep(5)
    results = get_results(scan['uuid'])
    return results.json()


def output(data, domain=""):
    task_fields = {
                   'uuid': 'Scan UUID',
                   'screenshotURL': 'Screenshot URL'
                  }
    lists_fields = {
                    'doamins': 'Domains',
                    'countries': "Countries",
                    'ips': 'IPs'
                   }
    stats_fields = {
                    'malicious': 'Malicious IPs',
                    'adBlocked': 'Ad Domains Blocked',
                    'totalLinks': 'Total Links',
                    'securePercentage': 'HTTPS Requests'
                   }
    master_fields = {
                     'task': task_fields,
                     'lists': lists_fields,
                     'stats': stats_fields
                    }
    for search_field, fields_lists in master_fields.items():
        for field, pname in fields_lists.items():
            if field in data[search_field]:
                if isinstance(data[search_field][field], list):
                    print((" [+] {}: {}".format(pname, ', '.join(data[search_field][field]))))
                else:
                    print((" [+] {}: {}".format(pname, data[search_field][field])))


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
