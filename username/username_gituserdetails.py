#!/usr/bin/env python

import base
import sys
import json
import requests
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n[+] Checking git user details\n' + style.END, 'blue')


def main(username):
    req = requests.get("https://api.github.com/users/%s" % username)
    return json.loads(req.content)


def output(data, username=""):
    if "message" in data and data["message"] == "Not Found":
        print 'Git account does not exist for this username.'
    else:
        print "Login: %s" % data['login']
        print "avatar_url: %s" % data['avatar_url']
        print "id: %s" % data['id']
        print "Repos: %s" % data['repos_url']
        print "Name: %s" % data['name']
        print "Company: %s" % data['company']
        print "Blog: %s" % data['blog']
        print "Location: %s" % data['location']
        print "Hireable: %s" % data['hireable']
        print "Bio: %s" % data['bio']
        print "On GitHub: %s" % data['created_at']
        print "Last Activity: %s" % data['updated_at']
        print "\n-----------------------------\n"


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print e
        print "Please provide a username as argument"
