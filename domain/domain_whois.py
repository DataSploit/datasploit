#!/usr/bin/env python

import base
import sys
import whois
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def whoisnew(domain):
    w = whois.whois(domain)
    return dict(w)


def banner():
    print colored(style.BOLD + '---> Finding Whois Information.' + style.END, 'blue')


def main(domain):
    return whoisnew(domain)


def output(data, domain=""):
    if 'creation_date' in data:
        data['creation_date'] = data['creation_date'].strftime('%m/%d/%Y')
    if 'creation_date' in data:
        data['expiration_date'] = data['expiration_date'].strftime('%m/%d/%Y')
    if 'creation_date' in data:
        data['updated_date'] = data['updated_date'].strftime('%m/%d/%Y')
    print data
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
