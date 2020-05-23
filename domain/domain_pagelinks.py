#!/usr/bin/env python

import base
import sys
import requests
from termcolor import colored
import time

ENABLED = True


def pagelinks(domain):
    time.sleep(0.3)
    try:
        req = requests.get('http://api.hackertarget.com/pagelinks/?q=%s' % (domain))
        page_links = req.content.decode('UTF-8').split("\n")
        return page_links
    except requests.exceptions.ConnectionError as ce:
        print('Connection time out: '.format(ce))
        return []


def banner():
    print(colored(base.style.BOLD + '\n---> Finding Pagelinks:\n' + base.style.END, 'blue'))


def main(domain):
    return pagelinks(domain)


def output(data, domain=""):
    for x in data:
        print(x)
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
