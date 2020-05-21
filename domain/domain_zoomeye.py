#!/usr/bin/env python

from . import base
import requests
import json
import sys
import vault
from termcolor import colored
import time

ENABLED = False


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def get_accesstoken_zoomeye(domain):
    username = vault.get_key('zoomeyeuser')
    password = vault.get_key('zoomeyepass')
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    datalogin = '{"username": "%s","password": "%s"}' % (username, password)
    s = requests.post("https://api.zoomeye.org/user/login", data=datalogin, headers=headers)
    responsedata = json.loads(s.text)
    if "error" in responsedata and responsedata['error'] == "bad_request":
	return False
    access_token1 = responsedata.get('access_token', "78c4a2dd70ddeffc5fc3c0639f86245a")
    return access_token1


def search_zoomeye(domain):
    time.sleep(0.3)
    zoomeye_token = get_accesstoken_zoomeye(domain)
    if not zoomeye_token:
	return [False, "BAD_API"]
    authData = {"Authorization": "JWT " + str(zoomeye_token)}
    req = requests.get('http://api.zoomeye.org/web/search/?query=site:%s&page=1' % domain, headers=authData)
    return True, req.text


def banner():
    print(colored(style.BOLD + '\n---> Finding hosts from ZoomEye\n' + style.END, 'blue'))


def main(domain):
    if vault.get_key('zoomeyepass') != "" and vault.get_key('zoomeyeuser') != "":
        zoomeye_results = search_zoomeye(domain)
	if zoomeye_results[0]:
	        return True, json.loads(zoomeye_results)
	else:
		return zoomeye_results
    else:
        return [False, "INVALID_API"]


def output(data, domain=""):
    if type(data) == list and data[1] == "INVALID_API":
        print(colored(
                style.BOLD + '\n[-] ZoomEye username and password not configured. Skipping Zoomeye Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    elif type(data) == list and data[1] == "BAD_API":
	print(colored(
                style.BOLD + '\n[-] ZoomEye API is not functional right now.\n' + style.END, 'red'))
    else:
        if 'matches' in list(data.keys()):
            print(len(data['matches']))
            for x in data['matches']:
                if x['site'].split('.')[-2] == domain.split('.')[-2]:
                    if 'title' in list(x.keys()):
                        print("IP: %s\nSite: %s\nTitle: %s\nHeaders: %s\nLocation: %s\n" % (
                            x['ip'], x['site'], x['title'], x['headers'].replace("\n\n", ""), x['geoinfo']))
                    else:
                        for val in list(x.keys()):
                            print("%s: %s" % (val, x[val]))
        print("\n-----------------------------\n")


if __name__ == "__main__":
    domain = sys.argv[1]
    banner()
    result = main(domain)
    if result:
        output(result, domain)
