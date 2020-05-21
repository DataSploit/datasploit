#!/usr/bin/env python

from . import base
import sys
import requests
from bs4 import BeautifulSoup
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print(colored(style.BOLD + '\n---> Searching Whoismind for associated domains\n' + style.END, 'blue'))


def main(email):
    req = requests.get('http://www.whoismind.com/email/%s.html' % (email))
    soup = BeautifulSoup(req.content, "lxml")
    atag = soup.findAll('a')
    domains = []
    for at in atag:
        if 'href' in at and at.text in at['href']:
            domains.append(at.text)
    domains = list(set(domains))
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
