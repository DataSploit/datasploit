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
    # Write a cool banner here
    print colored(style.BOLD + "[+] Searching in VirusTotal Dataset" + style.END)
    pass


def main(ip):
    # Use the ip variable to do some stuff and return the data
    if cfg.virustotal_public_api != "":
        print ip
        api = cfg.virustotal_public_api
        params = "{'ip': '%s', 'apikey': '%s'}" % (ip, api)
        url = "http://www.virustotal.com/vtapi/v2/ip-address/report?ip=%s&apikey=%s" % (ip, api)
        req = requests.get(url, params)
        return req
    else:
        return [False, "INVALID_API"]


def output(data, ip=""):
    # Use the data variable to print out to console as you like
    if type(data) == list and data[1] == "INVALID_API":
        print colored(
                style.BOLD + '\n[-] VirusTotal API Key not configured. Skipping VirusTotal Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
        return None

    if data.status_code != "200":
        print "Response Code: " + str(data.status_code)
        data.raise_for_status()
        if data.text:
            parsed = json.loads(data.text)
            print json.dumps(parsed, indent=4, sort_keys=True)
        print ""
        return None

    parsed = data.json()
    print json.dumps(parsed, indent=4, sort_keys=True)
    print ""


if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        banner()
        result = main(ip)
        output(result, ip)
    except Exception as e:
        print e
        print "Please provide an IP Address as argument"
