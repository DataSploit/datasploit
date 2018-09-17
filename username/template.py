#!/usr/bin/env python2

import base
import vault
import sys

# Control whether the module is enabled or not
ENABLED = True


def banner():
    # Write a cool banner here
    pass


def main(username):
    # Use the username variable to do some stuff and return the data
    print username
    return []


def output(data, username=""):
    # Use the data variable to print out to console as you like
    for i in data:
        print i


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print e
        print "Please provide a username as argument"
