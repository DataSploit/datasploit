#!/usr/bin/env python

import base
import config as cfg
import requests
import json
import sys
import re
from termcolor import colored

ENABLED = False


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def colorize(string):
    colourFormat = '\033[{0}m'
    colourStr = colourFormat.format(32)
    resetStr = colourFormat.format(0)
    lastMatch = 0
    formattedText = ''
    for match in re.finditer(
            r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+(\.[a-zA-Z]{2,4})|/(?:http:\/\/)?(?:([^.]+)\.)?datasploit\.info/|/(?:http:\/\/)?(?:([^.]+)\.)?(?:([^.]+)\.)?datasploit\.info/)',
            string):
        start, end = match.span()
        formattedText += string[lastMatch: start]
        formattedText += colourStr
        formattedText += string[start: end]
        formattedText += resetStr
        lastMatch = end
    formattedText += string[lastMatch:]
    return formattedText


def google_search(email):
    url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=\"%s\"&start=1" % (
        cfg.google_cse_key, cfg.google_cse_cx, email)
    all_results = []
    r = requests.get(url, headers={'referer': 'www.datasploit.info/hello'})
    data = json.loads(r.content)
    if 'error' in data:
        return False, data
    if int(data['searchInformation']['totalResults']) > 0:
        all_results += data['items']
        while "nextPage" in data['queries']:
            next_index = data['queries']['nextPage'][0]['startIndex']
            url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=\"%s\"&start=%s" % (
                cfg.google_cse_key, cfg.google_cse_cx, email, next_index)
            data = json.loads(requests.get(url).content)
        if 'error' in data:
            return True, all_results
        else:
            all_results += data['items']
    return True, all_results


def banner():
    print colored(style.BOLD + '\n---> Finding Paste(s)..\n' + style.END, 'blue')


def main(email):
    if cfg.google_cse_key != "" and cfg.google_cse_key != "XYZ" and cfg.google_cse_cx != "" and cfg.google_cse_cx != "XYZ":
        status, data = google_search(email)
        return [status, data]
    else:
        return False, "INVALID_API"


def output(data, email=""):
    if type(data) == list and not data[0]:
        if data[1] == "INVALID_API":
            print colored(
                style.BOLD + '\n[-] google_cse_key and google_cse_cx not configured. Skipping paste(s) search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
        else:
            print "Error Message: %s" % data[1]['error']['message']
            print "Error Code: %s" % data[1]['error']['code']
            print "Error Description: %s" % data[1]['error']['errors'][0]['reason']
    else:
        print "[+] %s results found\n" % len(data[1])
        for x in data[1]:
            print "Title: %s\nURL: %s\nSnippet: %s\n" % (x['title'].encode('utf-8'), colorize(x['link'].encode('utf-8')), colorize(x['snippet'].encode('utf-8')))


if __name__ == "__main__":
    #try:
    email = sys.argv[1]
    banner()
    result = main(email)
    if result:
        output(result, email)
    #except Exception as e:
    #print e
    
