# -*- coding: utf-8 -*-
import tweepy
import re
from collections import Counter

import requests
import sys
import config as cfg
import clearbit
import json
import time
import hashlib
from bs4 import BeautifulSoup

import os
import urllib

twitterex=0 #counter for identifying if twitter account is found

def git_user_details(username):
	req = requests.get("https://api.github.com/users/%s" % (username))
	return json.loads(req.content)

def usernamesearch(username):
	data = {"username":username}
	req = requests.post('https://usersearch.org/results_normal.php',data=data, verify=False)
	soup=BeautifulSoup(req.content, "lxml")
	atag=soup.findAll('a',{'class':'pretty-button results-button'})
	profiles=[]
	for at in atag:
		 if at.text=="View Profile":
			profiles.append(at['href'])
	return profiles

imglinks=[]
def extracting(prourl,tag,attribute,value,finattrib,profile):
	res=requests.get(prourl)
	soup=BeautifulSoup(res.content,"lxml")
	img=soup.find(tag,{attribute:value})
	if profile=="ask.fm":
		img[finattrib]="http:"+img[finattrib]
		imglinks.append(img[finattrib])
		path=username+"/"+profile+".jpg"
		urllib.urlretrieve(img[finattrib], path)
	else:
		imglinks.append(img[finattrib])
		path=username+"/"+profile+".jpg"
		urllib.urlretrieve(img[finattrib], path)

def profilepic(urls):
	
	
	if len(urls) or git_data['avatar_url']:
		if not os.path.exists(username):
			os.makedirs(username)
	if git_data.get("avatar_url", "") != "":
		path=username+"/github.jpg"
		urllib.urlretrieve(git_data['avatar_url'], path)
	for url in urls:
		if 'etsy' in url:
			try:
				tg='meta'
				att='property'
				val='og:image'
				valx='content'
				pro="etsy"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'gravatar' in url:
			try:
				tg='a'
				att='class'
				val='photo-0'
				valx='href'
				pro="gravatar"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass	
		elif 'youtube' in url:
			try:
				tg='link'
				att='itemprop'
				val='thumbnailUrl'
				valx='href'
				pro="youtube"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass		
		elif 'twitter' in url:
			try:
				tg='img'
				att='class'
				val='ProfileAvatar-image'
				valx='src'
				pro="twitter"
				extracting(url,tg,att,val,valx,pro)
				global twitterex
				twitterex=1
				continue
			except KeyError:
				pass
		elif 'photobucket' in url:
			try:
				tg='img'
				att='class'
				val='avatar smallProfile'
				valx='src'
				pro="photobucket"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'pinterest' in url:
			try:
				tg='meta'
				att='property'
				val='og:image'
				valx='content'
				pro="pinterest"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'ebay' in url:
			try:
				tg='img'
				att='class'
				val='prof_img img'
				valx='src'
				pro="ebay"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'steam' in url:
			try:
				tg='link'
				att='rel'
				val='image_src'
				valx='href'
				pro="steam"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'deviantart' in url:
			try:
				tg='img'
				att='class'
				val='avatar float-left'
				valx='src'
				pro="deviantart"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'last.fm' in url:
			try:
				tg='img'
				att='class'
				val='avatar'
				valx='src'
				pro="last.fm"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'vimeo' in url:
			try:
				tg='meta'
				att='property'
				val='og:image'
				valx='content'
				pro="vimeo"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'vimeo' in url:
			try:
				tg='meta'
				att='property'
				val='og:image'
				valx='content'
				pro="vimeo"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'ask.fm' in url:
			try:
				tg='meta'
				att='property'
				val='og:image'
				valx='content'
				pro="ask.fm"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'tripadvisor' in url:
			try:
				tg='img'
				att='class'
				val='avatarUrl'
				valx='src'
				pro="tripadvisor"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
		elif 'tumblr' in url:
			try:
				tg='link'
				att='rel'
				val='icon'
				valx='href'
				pro="tumblr"
				extracting(url,tg,att,val,valx,pro)
				continue
			except KeyError:
				pass
	print "Profile pics will be saved in %s" % username
	return imglinks


def twitterdetails(username):
	auth = tweepy.OAuthHandler(cfg.twitter_consumer_key, cfg.twitter_consumer_secret)
	auth.set_access_token(cfg.twitter_access_token, cfg.twiter_access_token_secret)

	#preparing auth
	api = tweepy.API(auth)

	
	f = open("temptweets.txt","w+")
	#writing tweets to temp file- last 1000
	for tweet in tweepy.Cursor(api.user_timeline, id=username).items(1000):
		f.write(tweet.text.encode("utf-8"))
		f.write("\n")
		


	#extracting hashtags
	f = open('temptweets.txt', 'r')
	q=f.read()
	strings = re.findall(r'(?:\#+[\w_]+[\w\'_\-]*[\w_]+)', q)	#Regex(s) Source: https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
	#extracting users
	tusers = re.findall(r'(?:@[\w_]+)', q)
	f.close()

	hashlist=[]
	userlist=[]
	for item in strings:
		item=item.strip( '#' )
		item=item.lower()
		hashlist.append(item)
	
	hashlist=hashlist[:10]
	for itm in tusers:
		itm=itm.strip( '@' )
		itm=itm.lower()
		userlist.append(itm)
	
	userlist=userlist[:10]
	
	return hashlist,userlist

username = sys.argv[1]


print "\t\t\t[+] Checking git user details\n"
try:
	git_data = git_user_details(username)
	print "Login: %s" % git_data['login']
	print "avatar_url: %s"  % git_data['avatar_url']
	print "id: %s" % git_data['id']
	print "Repos: %s" % git_data['repos_url']
	print "Name: %s" % git_data['name']
	print "Company: %s" % git_data['company']
	print "Blog: %s" % git_data['blog']
	print "Location: %s" % git_data['location']
	print "Hireable: %s" % git_data['hireable']
	print "Bio: %s" % git_data['bio']
	print "On GitHub: %s" % git_data['created_at']
	print "Last Activity: %s" % git_data['updated_at']
	print "\n-----------------------------\n"
except:
	print 'Git account do not exist on this username.'




print "\n\t\t\t[+] Username found on:\n"
links=usernamesearch(username)
for lnk in links:
	print lnk
print "\n-----------------------------\n"

imagelinks=profilepic(links)
imagelinks.append(git_data.get("avatar_url", ""))
print "\t\t\t[+] Finding Profile Pics\n"
for x in imagelinks:
	print x
print "\n\n-----------------------------\n"


if (twitterex==1):
#counting hashtag occurrence
	hashlist,userlist=twitterdetails(username)
	count= Counter(hashlist).most_common()
	print "Top Hashtag Occurrence for user "+username+" based on last 1000 tweets"
	for hash,cnt in count:
		print "#"+hash+" : "+str(cnt)
	print "\n"	
		
#counting user occurrence
	countu= Counter(userlist).most_common()
	print "Top User Occurrence for user "+username+" based on last 1000 tweets"
	for usr,cnt in countu:
		print "@"+usr+" : "+str(cnt)
