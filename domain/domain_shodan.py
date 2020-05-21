#!/usr/bin/env python

from . import base
import vault
import requests
import json
import sys
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def shodandomainsearch(domain):
    time.sleep(0.3)
    endpoint = "https://api.shodan.io/shodan/host/search?key=%s&query=hostname:%s&facets={facets}" % (
    vault.get_key('shodan_api'), domain)
    req = requests.get(endpoint)
    return req.content


def banner():
    print(colored(style.BOLD + '\n---> Searching in Shodan:\n' + style.END, 'blue'))


def main(domain):
    if vault.get_key('shodan_api') != None:
        return json.loads(shodandomainsearch(domain))
    else:
        return [False, "INVALID_API"]


def output(data, domain=""):
    if type(data) == list and data[1] == "INVALID_API":
        print(colored(
                style.BOLD + '\n[-] Shodan API Key not configured. Skipping Shodan search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    else:
        if 'matches' in list(data.keys()):
            for x in data['matches']:
                print("IP: %s\nHosts: %s\nDomain: %s\nPort: %s\nData: %s\nLocation: %s\n" % (
                x['ip_str'], x['hostnames'], x['domains'], x['port'], x['data'].replace("\n", ""), x['location']))
        print("-----------------------------\n")


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
