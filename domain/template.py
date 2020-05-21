#!/usr/bin/env python

from . import base
import vault
import sys

# Control whether the module is enabled or not
ENABLED = True


def banner():
    # Write a cool banner here
    pass


def main(domain):
    # Use the domain variable to do some stuff and return the data
    print(domain)
    return []


def output(data, domain=""):
    # Use the data variable to print out to console as you like
    for i in data:
        print(i)


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
