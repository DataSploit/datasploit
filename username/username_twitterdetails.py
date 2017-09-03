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

    userinfo = api.get_user(screen_name=username)

    userdetails = {}
    userdetails['Followers'] = userinfo.followers_count
    userdetails['Following'] = userinfo.friends_count
    userdetails['Geolocation Enabled'] = userinfo.geo_enabled
    try:
        userdetails['Homepage'] = userinfo.entities['url']['urls'][0]['display_url']
    except KeyError:
        pass
    userdetails['Language'] = userinfo.lang
    userdetails['Number of Tweets'] = userinfo.statuses_count
    userdetails['Profile Description'] = userinfo.description.encode('utf8')
    userdetails['Profile Set Location'] = userinfo.location
    userdetails['Time Zone'] = userinfo.time_zone
    userdetails['User ID'] = userinfo.id
    userdetails['UTC Offset'] = userinfo.utc_offset
    userdetails['Verified Account'] = userinfo.verified

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

    for itm in tusers:
        itm = itm.strip('@')
        itm = itm.lower()
        userlist.append(itm)

    activitydetails = {
                       'Hashtag Interactions': hashlist[:10],
                       'User Interactions': userlist[:10]
                      }

    return activitydetails, userdetails


def main(username):
    if cfg.twitter_consumer_key != "" and cfg.twitter_consumer_secret != "" and cfg.twitter_access_token != "" and cfg.twiter_access_token_secret != "":
        r = requests.get("https://twitter.com/%s" % username)
        if r.status_code == 200:
            activitydetails, userdetails = twitterdetails(username)
            return [activitydetails, userdetails]
        else:
            return None
    else:
        return [False, "INVALID_API"]


def output(data, username=""):
    if data[1] == "INVALID_API":
        print colored(
            style.BOLD + '\n[-] Twitter API Keys not configured. Skipping Twitter search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
    else:
        if data:
            hashlist = data[0]['Hashtag Interactions']
            userlist = data[0]['User Interactions']
            userdetails = data[1]
            for k,v in userdetails.iteritems():
                try:
                    print k + ": " + str(v)
                except UnicodeEncodeError as e:
                    print colored(style.BOLD + '[!] Error: ' + str(e) + style.END, 'red')
            print "\n"
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
