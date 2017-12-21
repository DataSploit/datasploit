#!/usr/bin/env python

import base
import config as cfg
import sys
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


def banner():
    # Write a cool banner here
    pass


def main(bitcoin):
    # Use the bitcoin variable to do some stuff and return the data
    print bitcoin
    return []


def output(data, bitcoin=""):
    # Use the data variable to print out to console as you like
    for i in data:
        print i


if __name__ == "__main__":
    try:
        bitcoin = sys.argv[1]
        banner()
        result = main(bitcoin)
        output(result, bitcoin)
    except Exception as e:
        print e
        print "Please provide an valid Bitcoin address as argument"
