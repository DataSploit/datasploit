#!/usr/bin/env python

import base
import config as cfg
import sys
import requests
import json
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n---> Checking breach status in HIBP (@troyhunt)\n' + style.END, 'blue')


def main(email):
    req = requests.get("https://haveibeenpwned.com/api/v2/breachedaccount/%s" % (email))
    if 'Attention Required! | CloudFlare' in req.content:
        print "CloudFlare detected"
        return {}
    if req.content != "":
	try:
            return json.loads(req.content)
	except:
	    return {}
    else:
        return {}


def output(data, email=""):
    if data:
        print colored("Pwned at %s Instances\n", 'green') % len(data)
        for x in data:
            print "Title: %s\nBreachDate: %s\nPwnCount: %s\nDescription: %s\nDataClasses: %s\n" % (
                x.get('Title', ''), x.get('BreachDate', ''), x.get('PwnCount', ''), x.get('Description', ''),
            ", ".join(map(lambda y: y.encode('utf-8',"replace") ,x.get('DataClasses',[]))))
    else:
        print colored("[-] No breach status found.", 'red')


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
