#!/usr/bin/env python

import base
import sys
import requests
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def pagelinks(domain):
    time.sleep(0.3)
    try:
        req = requests.get('http://h1.nobbd.de/search.php?q=%s' % (domain))
        page_links = req.content.split("\n")
        return page_links
    except:
        print 'Connection time out.'
        return []


def banner():
    print colored(style.BOLD + '\n---> Finding disclosure bugs pagelinks:\n' + style.END, 'blue')


def main(domain):
    return pagelinks(domain)


def output(data, domain=""):
    for x in data:
        print x
    print "\n-----------------------------\n"


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Invalid argument please provide domain name as argument"
