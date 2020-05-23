#!/usr/bin/env python

import base
from Wappalyzer import Wappalyzer, WebPage
import sys
import time
from termcolor import colored

ENABLED = True


def wappalyzeit(domain):
    temp_list = []
    time.sleep(0.3)
    wappalyzer = Wappalyzer.latest()
    webpage = WebPage.new_from_url(domain)
    set1 = wappalyzer.analyze(webpage)
    if set1:

        for s in set1:
            temp_list.append("\t%s" % s)
        return temp_list
    else:
        return temp_list


def banner():
    print(colored(base.style.BOLD + '\n---> Wapplyzing web page of base domain:\n' + base.style.END, 'blue'))


def main(domain):
    data = {"HTTP": [], "HTTPS": []}
    print("Hitting HTTP and HTTPS:\n", end=' ')
    try:
        targeturl = "http://" + domain
        data["HTTP"] = wappalyzeit(targeturl)
    except:
        print("[-] HTTP connection was unavailable")
    try:
        targeturl = "https://" + domain
        data["HTTPS"] = wappalyzeit(targeturl)
    except:
        print("[-] HTTPS connection was unavailable")
    return data


def output(data, domain=""):
    for i in data:
        if data[i]:
            print("[+] Third party libraries in Use for %s:" % i)
            for j in data[i]:
                print(j)
        else:
            print("[-] Nothing found for %s. Make sure domain name is passed properly" % i)
    print("\n-----------------------------\n")


if __name__ == "__main__":
    try:
        domain = sys.argv[1]
        banner()
        result = main(domain)
        output(result, domain)
    except Exception as e:
        print(e)
        print("Please provide a domain name as argument")
