#!/usr/bin/env python

import base
import os
import requests
import sys
import urllib.request, urllib.parse, urllib.error

from termcolor import colored
from bs4 import BeautifulSoup


# Control whether the module is enabled or not
ENABLED = True



def banner():
    print((colored(base.style.BOLD + '\n[+] Checking Tinder for username\n'
                  + base.style.END, 'blue')))


def fetch_content(username):
    r = requests.get('https://gotinder.com/@{}'.format(username))
    content = BeautifulSoup(r.content, 'lxml')
    return content


def check_useranme_exists(content):
    if content.find(id='card-container'):
        return True
    else:
        return False


def parse_page(content):
    userinfo = {
        'name': str(content.find(id='name').text),
        'age': content.find(id='age').text.encode('utf-8').strip(',\xc2\xa0'),
        'picture': str(content.find(id='user-photo').get('src')),
        'teaser': str(content.find(id='teaser').text.encode('ascii', 'ignore')),
    }
    return userinfo


def download_photo(username, url):
    file_path = str('profile_pic/{}'.format(username))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    path = file_path + "/tinder." + url.split('.')[-1]
    urllib.request.urlretrieve(url, path)


def main(username):
    userinfo = {}
    content = fetch_content(username)
    if check_useranme_exists(content):
        userinfo = parse_page(content)
        download_photo(username, str(content.find(id='user-photo').get('src')))
    if not userinfo:
        print(colored(base.style.BOLD + '\n[!] Nothing found on Tinder\n'
                      + base.style.END, 'red'))
    return userinfo


def output(data, username=""):
    if len(data) is 0:
        print('username not found')
    else:
        for k, v in data.items():
            print(('{k}: {v}'.format(k=k.capitalize(), v=v)))


if __name__ == "__main__":
    #try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    #except Exception as e:
    #    print e
    #    print "Please provide a username as argument"
