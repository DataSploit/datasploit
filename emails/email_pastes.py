#!/usr/bin/env python

from . import base
import vault
import requests
import json
import sys
import re
from termcolor import colored

ENABLED = True


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
    google_cse_key = vault.get_key('google_cse_key')
    google_cse_cx = vault.get_key('google_cse_cx')
    url = "https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=\"%s\"&start=1" % (
        google_cse_key, google_cse_cx, email)
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
                google_cse_key, google_cse_cx, email, next_index)
            data = json.loads(requests.get(url).content)
	    if 'error' in data:
                return True, all_results
            else:
                all_results += data['items']
    return True, all_results


def banner():
    print(colored(style.BOLD + '\n---> Finding Paste(s)..\n' + style.END, 'blue'))


def main(email):
    if vault.get_key('google_cse_key') != None and vault.get_key('google_cse_cx') != None:
        status, data = google_search(email)
        return [status, data]
    else:
        return [False, "INVALID_API"]


def output(data, email):
    if data[0] == False:
        print(colored(
            style.BOLD + '[-] google_cse_key and google_cse_cx not configured. Skipping paste(s) search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    else:
        #print data[0]
        print("[+] %s results found\n" % len(data[1]))
        for x in data[1]:
	    title = x['title'].encode('ascii', 'ignore').decode('ascii')
            snippet = x['snippet'].encode('ascii', 'ignore').decode('ascii')
            link = x['link'].encode('ascii', 'ignore').decode('ascii')
            print("Title: %s\nURL: %s\nSnippet: %s\n" % (title, colorize(link), colorize(snippet)))


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except e as Exception:
        print(e)
