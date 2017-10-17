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


def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key)+":")
      if isinstance(value, dict):
         pretty(value, indent+1)
      elif isinstance(value,list):
	 for v in value:
             print('\t' * (indent+1) + str(v))
      else:
         print('\t' * (indent+1) + str(value))


def main(domain):
    return whoisnew(domain)


def output(data, domain=""):
    pretty(data)
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
