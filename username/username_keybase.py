#!/usr/bin/env python

import base
import sys
from termcolor import colored
import requests
import json

# Control whether the module is enabled or not
ENABLED = True

class style:
   BOLD = '\033[1m'
   END = '\033[0m'

def banner():
    # Write a cool banner here
    print colored(style.BOLD + '\n---> Searching User info @ Keybase\n' + style.END, 'blue')
    pass


def main(username):
    # Use the username variable to do some stuff and return the data
    url = "https://keybase.io/_/api/1.0/user/lookup.json?usernames=%s" %username
    req = requests.get(url)
    data = json.loads(req.text) 
    if 'them' in data:
        if data['them'][0] is not None:
            dict_them = data['them'][0]
            return dict_them
    else:
        dict_them = []
        return dict_them


def output(dict_them, username):
    # Use the data variable to print out to console as you like
    print "Username: %s" % username
    if len(dict_them) != 0:
        if 'profile' in dict_them:
            if len(dict_them['profile'].keys()) != 0:
                print colored(style.BOLD + 'Basic Information' + style.END, 'green')
                for item in dict_them['profile']:
                    if item != 'mtime':
                        print "%s: %s" % (item, dict_them['profile'][item])
        if 'proofs_summary' in dict_them:
            if len(dict_them['proofs_summary'].keys()) != 0:
                print colored(style.BOLD + '\nProfiles:' + style.END, 'green')
                if 'all' in dict_them['proofs_summary'].keys():
                    for x in dict_them['proofs_summary']['all']:
                        print "%s: %s" % (x['proof_type'], x['service_url'])
        if 'pictures' in dict_them:
            if len(dict_them['pictures'].keys()) != 0:
                print colored(style.BOLD + '\nProfile Image:' + style.END, 'green'),
                print dict_them['pictures']['primary']['url']
        if 'devices' in dict_them:
            if len(dict_them['devices'].keys()) != 0:
                print colored(style.BOLD + '\nDevice Information:' + style.END, 'green')
                print "[+] Total %s Devices found." % len(dict_them['devices'].keys())
                for x in dict_them['devices'].keys():
                    print "  - %s (%s)" % (dict_them['devices'][x]['name'], dict_them['devices'][x]['type'])
    else:
        print "User not found on Keybase"
    print ""


if __name__ == "__main__":
    username = sys.argv[1]
    banner()
    result = main(username)
    output(result, username)

