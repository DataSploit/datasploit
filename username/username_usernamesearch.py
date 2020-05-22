#!/usr/bin/env python

import base
import sys
import requests
from bs4 import BeautifulSoup
from termcolor import colored
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Control whether the module is enabled or not
ENABLED = True



def banner():
    print(colored(base.style.BOLD + '\n[+] Username found on\n' + base.style.END, 'blue'))


def main(username):
    data = {"username": username}
    req = requests.post('https://usersearch.org/results_normal.php', data=data, verify=False)
    soup = BeautifulSoup(req.content, "lxml")
    atag = soup.findAll('a', {'class': 'pretty-button results-button'})
    profiles = []
    for at in atag:
        if at.text == "View Profile":
            profiles.append(at['href'])
    return profiles


def output(data, username=""):
    for lnk in data:
        print(lnk)
    print("\n-----------------------------\n")


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print(e)
        print("Please provide a username as argument")
