#!/usr/bin/env python

from . import base
import vault
import requests
import json
import sys
import time
from termcolor import colored

ENABLED = True
WRITE_TEXT_FILE = True
MODULE_NAME = "Domain_Emails"


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def emailhunter(domain):
    collected_emails = []
    time.sleep(0.3)
    emailhunter_api = vault.get_key('emailhunter')
    url = "https://api.emailhunter.co/v1/search?api_key=%s&domain=%s" % (emailhunter_api, domain)
    res = requests.get(url)
    try:
        parsed = json.loads(res.text)
        if 'emails' in list(parsed.keys()):
            for email in parsed['emails']:
                collected_emails.append(email['value'])
        elif json.loads(res.text).get('status') == "error":
            print(colored(style.BOLD + '[-] %s\n' % json.loads(res.text).get('message') + style.END, 'red'))
    except:
        print('CAPTCHA has been implemented, skipping this for now.')
    return collected_emails


def banner():
    print(colored(style.BOLD + '\n---> Harvesting Email Addresses:.\n' + style.END, 'blue'))


def main(domain):
    if vault.get_key('emailhunter') != None:
        return emailhunter(domain)
    else:
        return [False, "INVALID_API"]


def output(data, domain=""):
    if type(data) == list and data[1] == "INVALID_API":
            print(colored(
                style.BOLD + '\n[-] Emailhunter API key not configured, skipping Email Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    else:
        for x in data:
            print(str(x))


def output_text(data):
	return "\n".join(data)


if __name__ == "__main__":
        domain = sys.argv[1]
        banner()
        result = main(domain)
        if result:
            output(result, domain)
