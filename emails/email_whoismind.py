#!/usr/bin/env python

import base
import sys
import requests
from bs4 import BeautifulSoup
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True



def banner():
    print(colored(base.style.BOLD + '\n---> Searching Whoismind for associated domains\n' + base.style.END, 'blue'))


def main(email):
    req = requests.get('http://www.whoismind.com/email/%s.html' % (email))
    soup = BeautifulSoup(req.content, "lxml")
    atag = soup.findAll('a')
    domains = []
    for at in atag:
        if 'href' in at and at.text in at['href']:
            domains.append(at.text)
    domains = list(set(domains))
    if not domains:
        print(colored(base.style.BOLD + '\n[!] Nothing found for Whoismind\n' + base.style.END, 'red'))
    return domains


def output(data, email=""):
    for domain in data:
        if domain:
            print(domain)
    print("\n-----------------------------\n")


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print(e)
        print("Please provide an email as argument")
