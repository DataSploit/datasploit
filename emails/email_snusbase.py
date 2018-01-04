#!/usr/bin/env python

### Uses the snusbase.com API to query service for leaked accounts based on the email address
### API: snusbase.com
### Make sure your secret API url and token are saved in the config.py file
### Maintained by @khast3x

import base
import config as cfg
import requests
import json
from termcolor import colored
import sys

# Control whether the module is enabled or not
ENABLED = True
class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored('\n---> Checking snusbase database leak\n', "blue")
    pass

def snusbaseemailsearch(email):

    url = cfg.snusbase_secret_url
    payload = {"type": "email", "term": email}
    headers = {
        'Authorization': cfg.snusbase_token,
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.content

def main(email):
    # Use the email variable to do some stuff and return the data
    if cfg.snusbase_secret_url != "" and cfg.snusbase_token != "":
        return json.loads(snusbaseemailsearch(email))
    else:
        return [False, "INVALID_API"]
    print email
    return []


def output(data, email=""):
    if data["result"]:
        for res in data["result"]:
            print colored("---------------------", "yellow")
            # Colour result if password is present
            if res["password"]:
                print colored("email: %s", "green") % res["email"]
                print colored("password: %s", "green") % res["password"]
            else:
                print "email: %s" % res["email"]
                print "password: %s" % res["password"]
            # Print only if present
            if res["username"]:
                print "username: %s" % res["username"]
            if res["hash"]:
                print "hash: %s" % res["hash"]
                print "salt: %s" % res["salt"]
        print colored("\nFound %s results\n", "blue") % data["result_size"]

    else:
        print "\n--- No data found in snusbase ---\n"
        return


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
