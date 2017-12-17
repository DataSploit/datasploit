#!/usr/bin/env python
import base
import config as cfg
import sys
from termcolor import colored


#module dependencies
import requests
from bs4 import BeautifulSoup

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n[+] Checking Gitlab user details\n' + style.END, 'blue')


def main(username):
    # Use the username variable to do some stuff and return the data
    gitlabdetails = []
    url = "https://gitlab.com/" + username
    if (requests.head(url, verify=False).status_code == 200):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        handle= soup.find("span", {"class" : "middle-dot-divider"})
        if handle:
            name= soup.find("div", {"class" : "cover-title"})
            gitlabdetails.append("Name: " +name.text.strip())
            handle= soup.find("span", {"class" : "middle-dot-divider"})
            mydivs = soup.findAll("div", { "class" : "profile-link-holder middle-dot-divider" })
            for div in mydivs:
                q=div.find('a', href=True)
                if q:
                  gitlabdetails.append(q['href'].strip())
                elif div.find("i", {"class" : "fa fa-map-marker"}):
                  gitlabdetails.append("Location:" + div.text.strip())
                elif div.find("i", {"class" : "fa fa-briefcase"}):
                  gitlabdetails.append("Organisation: " + div.text.strip())

    return gitlabdetails


def output(data, username=""):
    # Use the data variable to print out to console as you like
    if data:
        print "Gitlab user details:\n"
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
