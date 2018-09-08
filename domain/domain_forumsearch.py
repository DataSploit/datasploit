#!/usr/bin/env python2

import base
import requests
from bs4 import BeautifulSoup
import sys
import re
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def boardsearch_forumsearch(domain):
    time.sleep(0.3)
    req = requests.get(
        'http://boardreader.com/index.php?a=l&q=%s&d=0&extended_search=1&q1=%s&ltype=all&p=50' % (domain, domain))
    soup = BeautifulSoup(req.content, "lxml")
    text = soup.findAll('bdo', {"dir": "ltr"})
    links = {}
    for lk in text:
        links[lk.text] = re.search("'(.+?)'", lk.parent['onmouseover']).group(1)
    return links


def banner():
    print colored(style.BOLD + '\n---> Gathering links from Forums:\n' + style.END, 'blue')


def main(domain):
    return boardsearch_forumsearch(domain)


def output(data, domain=""):
    print "[+] Associated Forum Links\n"
    for tl, lnk in data.items():
        print "%s (%s)" % (lnk, tl)
    print "\n-----------------------------\n"


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
