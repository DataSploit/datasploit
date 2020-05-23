#!/usr/bin/env python

import base
import requests
from bs4 import BeautifulSoup
import sys
from termcolor import colored
import time

ENABLED = True


def wikileaks(domain):
    time.sleep(0.3)
    req = requests.get(
        'https://search.wikileaks.org/?query=&exact_phrase=%s&include_external_sources=True&order_by=newest_document_date' % (
            domain))
    soup = BeautifulSoup(req.content, "lxml")
    count = soup.findAll('div', {"class": "total-count"})
    divtag = soup.findAll('div', {'class': 'result'})
    links = {}
    for a in divtag:
        links[a.a.text.encode('utf-8')] = a.a['href']
    return links


def banner():
    print(colored(base.style.BOLD + '\n---> Searching through WikiLeaks\n' + base.style.END, 'blue'))


def main(domain):
    return wikileaks(domain)


def output(data, domain=""):
    for tl, lnk in list(data.items()):
        print("%s (%s)" % (repr(lnk), tl))
    print("")
    print("For all results, visit: " + 'https://search.wikileaks.org/?query=&exact_phrase=%s&include_external_sources=True&order_by=newest_document_date' % domain)
    print("\n-----------------------------\n")


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
