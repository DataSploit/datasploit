#!/usr/bin/env python

import base
import sys
import urllib.request, urllib.error, urllib.parse
import re
import string
from termcolor import colored

ENABLED = True


def googlesearch(query, ext):
    google = "https://www.google.co.in/search?filter=0&q=site:"
    getrequrl = "https://www.google.co.in/search?filter=0&num=100&q=%s&start=" % query
    hdr = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }
    req = urllib.request.Request(getrequrl, headers=hdr)
    response = urllib.request.urlopen(req)
    data = response.read().decode('UTF-8')
    data = re.sub('<b>', '', data)
    for e in ('>', '=', '<', '\\', '(', ')', '"', 'http', ':', '//'):
        data = str.replace(data, e, ' ')

    r1 = re.compile('[-_.a-zA-Z0-9.-_]*' + '\.' + ext)
    res = r1.findall(data)
    return res


def banner():
    print(colored(base.style.BOLD + '\n---> Searching Google for domain results\n' + base.style.END, 'blue'))


def main(domain):
    list_ext = {"pdf": [], "xls": [], "docx": []}
    for x in list_ext:
        query = "site:%s+filetype:%s" % (domain, x)
        results = googlesearch(query, x)
        list_ext[x] = results
    return list_ext


def output(data, domain=""):
    for key, results in data.items():
        if results:
            results = set(results)
            for x in results:
                x = re.sub('<li class="first">', '', x)
                x = re.sub('</li>', '', x)
                print(x)


if __name__ == "__main__":
    try:
        banner()
        domain = sys.argv[1]
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
