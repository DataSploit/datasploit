#!/usr/bin/env python

import base
import config as cfg
import os
import re
import sys
import tweepy
import requests
from collections import Counter
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print colored(style.BOLD + '\n[+] Getting information from Twitter\n' + style.END, 'blue')


def twitterdetails(username):
    auth = tweepy.OAuthHandler(cfg.twitter_consumer_key, cfg.twitter_consumer_secret)
    auth.set_access_token(cfg.twitter_access_token, cfg.twiter_access_token_secret)

    # preparing auth
    api = tweepy.API(auth)

    f = open("temptweets.txt", "w+")
    # writing tweets to temp file- last 1000
    for tweet in tweepy.Cursor(api.user_timeline, id=username).items(1000):
        f.write(tweet.text.encode("utf-8"))
        f.write("\n")

    # extracting hashtags
    f = open('temptweets.txt', 'r')
    q = f.read()
    strings = re.findall(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', q)
    tusers = re.findall(r'(?:@[\w_]+)', q)
    f.close()
    os.remove("temptweets.txt")

    hashlist = []
    userlist = []
    for item in strings:
        item = item.strip('#')
        item = item.lower()
        hashlist.append(item)

    hashlist = hashlist[:10]
    for itm in tusers:
        itm = itm.strip('@')
        itm = itm.lower()
        userlist.append(itm)

    userlist = userlist[:10]

    return hashlist, userlist


def main(username):
    if cfg.twitter_consumer_key != "" and cfg.twitter_consumer_secret != "" and cfg.twitter_access_token != "" and cfg.twiter_access_token_secret != "":
        r = requests.get("https://twitter.com/%s" % username)
        if r.status_code == 200:
            hashlist, userlist = twitterdetails(username)
            return [hashlist, userlist]
        else:
            return None
    else:
        return [False, "INVALID_API"]


def output(data, username=""):
    if data[1] == "INVALID_API":
        print colored(
            style.BOLD + '\n[-] Twitter API Keys not configured. Skipping Twitter search.\nPlease refer to https://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
    else:
        if data:
            hashlist = data[0]
            userlist = data[1]
            count = Counter(hashlist).most_common()
            print "Top Hashtag Occurrence for user " + username + " based on last 1000 tweets"
            for hash, cnt in count:
                print "#" + hash + " : " + str(cnt)
            print "\n"

            # counting user occurrence
            countu = Counter(userlist).most_common()
            print "Top User Occurrence for user " + username + " based on last 1000 tweets"
            for usr, cnt in countu:
                print "@" + usr + " : " + str(cnt)
        else:
            print "No Associated Twitter account found."


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print e
        print "Please provide a username as argument"
