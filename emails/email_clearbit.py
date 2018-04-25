#!/usr/bin/env python

import base
import vault
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
    print colored(style.BOLD + '\n---> Searching Clearbit\n' + style.END, 'blue')


def main(email):
    clearbit_apikey = vault.get_key('clearbit_apikey')
    if clearbit_apikey != None:
        headers = {"Authorization": "Bearer %s" % clearbit_apikey}
        req = requests.get("https://person-stream.clearbit.com/v2/people/find?email=%s" % (email), headers=headers)
        person_details = json.loads(req.content)
        if "error" in req.content and "queued" in req.content:
            print "This might take some more time, Please run this script again, after 5 minutes."
        else:
            return person_details
    else:
        return [False, "INVALID_API"]


def output(data, email=""):
    print data
    if type(data) == list and data[1] == "INVALID_API":
        print colored(
                style.BOLD + '\n[-] Clearbit API Key not configured. Skipping Clearbit Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
    else:
        for x in data.keys():
            print '%s details:' % x
            if type(data[x]) == dict:
                for y in data[x].keys():
                    if data[x][y] is not None:
                        print "%s:  %s, " % (y, data[x][y])
            elif data[x] is not None:
                print "\n%s:  %s" % (x, data[x])

        print "\n-----------------------------\n"


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
