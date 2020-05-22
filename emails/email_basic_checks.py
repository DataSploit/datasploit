#!/usr/bin/env python

import base
import vault
import requests
import json
import sys
import re
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


def basic_checks(email):
    if re.match('[^@]+@[^@]+\.[^@]+', email):
        mailboxlayer_api = vault.get_key('mailboxlayer_api')
        if vault.get_key('mailboxlayer_api'):
            url = "http://apilayer.net/api/check?access_key=%s&email=%s&smtp=1&format=1" % (mailboxlayer_api, email)
            req = requests.get(url)
            resp = json.loads(req.text)
            return resp
        else:
            return -2
    else:
        return -1


def output(data, email=""):
    if data == -1:
        print(colored(base.style.BOLD + '\n[-] Please pass a valid email ID.\n' + base.style.END, 'red'))
    elif data == -2:
        print(colored(
            base.style.BOLD + '\n[-] MailBoxLayer_API Key not configured. Skipping basic checks.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + base.style.END,
            'red'))
    else:
        print("Is it a free Email Address?:", end=' ')
        print("No" if not data['free'] else "Yes")

        print("Email ID Exist?: ", end=' ')
        print("Yes" if data['smtp_check'] else "No")

        print("Can this domain recieve emails?: ", end=' ')
        print("Yes" if data['mx_found'] else "No")

        print("Is it a Disposable email?: ", end=' ')
        print("Yes" if data['disposable'] else "No")


def banner():
    print(colored(base.style.BOLD + '\n---> Basic Email Check(s)..\n' + base.style.END, 'blue'))


def main(email):
    return basic_checks(email)


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")
