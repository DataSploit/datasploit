#!/usr/bin/env python

# Credits: https://github.com/int0x80/tcispy

# The required token (github_travis_key) can be generated from the link https://github.com/settings/tokens/new by following the requirement present at https://travispy.readthedocs.io/en/stable/getting_started/

import base
import config as cfg
import sys
from termcolor import colored


#module dependencies
from travispy import TravisPy
import urllib2
import json

import warnings
warnings.filterwarnings('ignore')
    

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n[+] Checking Travis-CI user (author and associated committer) details\n' + style.END, 'blue')


def main(username):
    # Use the username variable to do some stuff and return the data
    if cfg.github_travis_key != "":
      token = TravisPy.github_auth(cfg.github_travis_key)
      q=urllib2.urlopen("https://api.travis-ci.org/repos/%s" % username)
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
      print colored(style.BOLD + '\n[-] Travis CI key not configured. Skipping basic checks.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')


def output(data, username=""):
    # Use the data variable to print out to console as you like
    if data:
        print "Name(s) and Email(s) of author and associated committer(s):\n"
        for dt in data:
            print dt
    else:
        print "No data found."


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print e
        print "Please provide a username as argument"
