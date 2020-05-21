#!/usr/bin/env python

# Credits: https://github.com/int0x80/tcispy

# The required token (github_access_token) can be generated from the link https://github.com/settings/tokens/new by following the requirement present at https://travispy.readthedocs.io/en/stable/getting_started/

import base
import sys
from termcolor import colored
import vault


#module dependencies
from travispy import TravisPy
import urllib.request, urllib.error, urllib.parse
import json

import warnings
warnings.filterwarnings('ignore')


# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print(colored(style.BOLD + '\n[+] Checking Travis-CI user (author and associated committer) details\n' + style.END, 'blue'))


def main(username):
    github_access_token = vault.get_key('github_access_token')
    if github_access_token != None:
        # Use the username variable to do some stuff and return the data
        token = TravisPy.github_auth(github_access_token)
        q=urllib.request.urlopen("https://api.travis-ci.org/repos/%s" % username)
        jsondata=json.loads(q.read())
        details=[]

        if jsondata:
            for data in jsondata:
                builds=token.builds(slug=data["slug"])
                for bd in builds:
                    bid=token.build(bd.id)
                    details.append((bid.commit.author_name,bid.commit.author_email))
                    details.append((bid.commit.committer_name,bid.commit.committer_email))
        details=list(set(details))
        return details
    else:
        return [ colored(style.BOLD +
                         '[!] Error: No github token for Travis CI found. Skipping' +
                         style.END, 'red') ]


def output(data, username=""):
    # Use the data variable to print out to console as you like
    if data:
        # Check if error and if list length is 1, and remove from file output if so
        if "[!] Error:" in data[0] and len(data) == 1:
            print(data[0])
            del data[0]
        else:
            print("Name(s) and Email(s) of author and associated committer(s):\n")
            for dt in data:
                print(dt[0] + ': ' + dt[1])
    else:
        print("No data found.")


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print(e)
        print("Please provide a username as argument")
