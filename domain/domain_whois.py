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
        creation_date = data['creation_date']
        data['creation_date'] = creation_date[0].strftime('%m/%d/%Y') if isinstance(creation_date, list) \
            else creation_date.strftime('%m/%d/%Y')
    if 'expiration_date' in data:
        expiration_date = data['expiration_date']
        data['expiration_date'] = expiration_date[0].strftime('%m/%d/%Y') if isinstance(expiration_date, list) \
            else expiration_date.strftime('%m/%d/%Y')
    if 'updated_date' in data:
        updated_date = data['updated_date']
        data['updated_date'] = updated_date[0].strftime('%m/%d/%Y') if isinstance(updated_date, list) \
            else updated_date.strftime('%m/%d/%Y')
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
