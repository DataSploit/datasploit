#!/usr/bin/env python

import base
import config as cfg
import requests
import json
import sys
import time
from termcolor import colored

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def emailhunter(domain):
    collected_emails = []
    time.sleep(0.3)
    url = "https://api.emailhunter.co/v1/search?api_key=%s&domain=%s" % (cfg.emailhunter, domain)
    res = requests.get(url)
    try:
        parsed = json.loads(res.text)
        if 'emails' in parsed.keys():
            for email in parsed['emails']:
                collected_emails.append(email['value'])
    except:
        print 'CAPTCHA has been implemented, skipping this for now.'
    return collected_emails


def banner():
    print colored(style.BOLD + '\n---> Harvesting Email Addresses:.\n' + style.END, 'blue')


def main(domain):
    if cfg.emailhunter != "":
        return emailhunter(domain)
    else:
        return [False, "INVALID_API"]


def output(data, domain=""):
    if type(data) == list and data[1] == "INVALID_API":
            print colored(
                style.BOLD + '\n[-] Emailhunter API key not configured, skipping Email Search.\nPlease refer to https://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
    else:
        for x in data:
            print str(x)


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        if result:
            output(result, domain)
        else:
            pass
    except Exception as e:
        print e
        print "Please provide a domain name as argument"
