#!/usr/bin/env python

import json
import base
import sys
import whois
from termcolor import colored
import time
import datetime

ENABLED = True
OUTPUT_TYPE = "console"

class style:
    BOLD = '\033[1m'
    END = '\033[0m'

def whoisnew(domain):
    w = whois.whois(domain)
    return dict(w)

def banner():
    if(OUTPUT_TYPE == "console"):
        print colored(style.BOLD + '---> Finding Whois Information.' + style.END, 'blue')

def main(domain):
    return whoisnew(domain)

def output(data, domain=""):

    if(OUTPUT_TYPE == "console"):
        print data
        print "\n-----------------------------\n"

    if(OUTPUT_TYPE == "json"):
        js = {}
        for i in data:
            # convert iterables to json list
            if(hasattr(data[i], '__iter__')):
                js[i] = list()
                for j in data[i]:
                    js[i].append(j)
            # convert datetime to string
            elif (isinstance(data[i], datetime.datetime)):
                js[i] = data[i].strftime("%s")
            else:
                js[i] = str(data[i])
        
        print json.dumps(js)

if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        if(len(sys.argv) > 2):
             OUTPUT_TYPE=sys.argv[2]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
