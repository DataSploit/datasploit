#!/usr/bin/env python

import base
import requests
import json
import sys
import config as cfg
from termcolor import colored
import time

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def get_accesstoken_zoomeye(domain):
    username = cfg.zoomeyeuser
    password = cfg.zoomeyepass
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    datalogin = '{"username": "%s","password": "%s"}' % (username, password)
    s = requests.post("https://api.zoomeye.org/user/login", data=datalogin, headers=headers)
    print s.text
    responsedata = json.loads(s.text)
    access_token1 = responsedata['access_token']
    return access_token1


def search_zoomeye(domain):
    time.sleep(0.3)
    zoomeye_token = get_accesstoken_zoomeye(domain)
    authData = {"Authorization": "JWT " + str(zoomeye_token)}
    req = requests.get('https://api.zoomeye.org/web/search/?query=site:%s&page=1' % domain, headers=authData)
    return req.text


def banner():
    print colored(style.BOLD + '\n---> Finding hosts from ZoomEye\n' + style.END, 'blue')


def main(domain):
    if cfg.zoomeyepass != "" and cfg.zoomeyeuser != "":
        zoomeye_results = search_zoomeye(domain)
        return json.loads(zoomeye_results)
    else:
        return [False, "INVALID_API"]


def output(data, domain=""):
    if type(data) == list and data[1] == "INVALID_API":
        print colored(
                style.BOLD + '\n[-] ZoomEye username and password not configured. Skipping Zoomeye Search.\nPlease refer to https://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
    else:
        if 'matches' in data.keys():
            print len(data['matches'])
            for x in data['matches']:
                if x['site'].split('.')[-2] == domain.split('.')[-2]:
                    if 'title' in x.keys():
                        print "IP: %s\nSite: %s\nTitle: %s\nHeaders: %s\nLocation: %s\n" % (
                            x['ip'], x['site'], x['title'], x['headers'].replace("\n\n", ""), x['geoinfo'])
                    else:
                        for val in x.keys():
                            print "%s: %s" % (val, x[val])
        print "\n-----------------------------\n"


if __name__ == "__main__":
    domain = sys.argv[1]
    banner()
    result = main(domain)
    if result:
        output(result, domain)

