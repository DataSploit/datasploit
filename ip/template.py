#!/usr/bin/env python

from . import base
import vault
import sys

# Control whether the module is enabled or not
ENABLED = True


def banner():
    # Write a cool banner here
    pass


def main(ip):
    # Use the ip variable to do some stuff and return the data
    print(ip)
    return []


def output(data, ip=""):
    # Use the data variable to print out to console as you like
    for i in data:
        print(i)


if __name__ == "__main__":
    try:
        ip = sys.argv[1]
        banner()
        result = main(ip)
        output(result, ip)
    except Exception as e:
        print(e)
        print("Please provide an IP Address as argument")
