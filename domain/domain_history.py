#!/usr/bin/env python

from . import base
import sys
import requests
from bs4 import BeautifulSoup
import re
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def netcraft_domain_history(domain):
    ip_history_dict = {}
    time.sleep(0.3)
    endpoint = "http://toolbar.netcraft.com/site_report?url=%s" % (domain)
    req = requests.get(endpoint)

    soup = BeautifulSoup(req.content, 'html.parser')
    urls_parsed = soup.findAll('a', href=re.compile(r'.*netblock\?q.*'))
    for url in urls_parsed:
        if urls_parsed.index(url) != 0:
            ip_history_dict[str(url).split('=')[2].split(">")[1].split("<")[0]] = str(url.parent.findNext('td')).strip(
                "<td>").strip("</td>")
    return ip_history_dict


def banner():
    print(colored(style.BOLD + '\n---> Searching Domain history in Netcraft\n' + style.END, 'blue'))


def main(domain):
    return netcraft_domain_history(domain)


def output(data, domain=""):
    for x in list(data.keys()):
        print("%s: %s" % (data[x], x))
    print("\n-----------------------------\n")


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
