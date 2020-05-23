#!/usr/bin/env python

import base
import requests
import sys
import json
import warnings
from termcolor import colored
import time

ENABLED = False


warnings.filterwarnings("ignore")


def checkpunkspider(reversed_domain):
    time.sleep(0.5)
    req = requests.post("http://www.punkspider.org/service/search/detail/" + reversed_domain, verify=False)
    try:
        return json.loads(req.content)
    except:
        return {}


def banner():
    print(colored(base.style.BOLD + '\n---> Trying luck with PunkSpider\n' + base.style.END, 'blue'))


def main(domain):
    reversed_domain = ""
    for x in reversed(domain.split(".")):
        reversed_domain = reversed_domain + "." + x
    reversed_domain = reversed_domain[1:]
    return checkpunkspider(reversed_domain)


def output(data, domain=""):
    if data is not None:
        if 'data' in list(data.keys()) and len(data['data']) >= 1:
            print(colored("Few vulnerabilities found at Punkspider", 'green'))
            for x in data['data']:
                print("==> ", x['bugType'])
                print("Method:", x['verb'].upper())
                print("URL:\n" + x['vulnerabilityUrl'])
                print("Param:", x['parameter'])
        else:
            print(colored("[-] No Vulnerabilities found on PunkSpider\n", 'red'))


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
