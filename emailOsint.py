import requests
import sys
import config as cfg
import clearbit
import json
import time
import hashlib
from bs4 import BeautifulSoup
import re
from email_fullcontact import fullcontact


email = sys.argv[1]
print email


def haveIbeenpwned(email):
	print "\t\t\t[+] Checking on Have_I_Been_Pwned...\n"
	req = requests.get("https://haveibeenpwned.com/api/v2/breachedaccount/%s" % (email))
	return json.loads(req.content)


def clearbit(email):
	header = {"Authorization" : "Bearer %s" % (cfg.clearbit_apikey)}
	req = requests.get("https://person.clearbit.com/v1/people/email/%s" % (email), headers = header)
	person_details = json.loads(req.content)
	if ("error" in req.content and "queued" in req.content):
		print "This might take some more time, Please run this script again, after 5 minutes."
		time.sleep(20)
	else:
		return person_details

def gravatar(email):
	gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() 
	return gravatar_url

def emaildom(email):
	req = requests.get('http://www.whoismind.com/email/%s.html'%(email))
	soup=BeautifulSoup(req.content, "lxml")
	atag=soup.findAll('a')
	domains=[]
	for at in atag:
		if at.text in at['href']:
			domains.append(at.text)
	domains=set(domains)
	return domains

def emailslides(email):
	req = requests.get('http://www.slideshare.net/search/slideshow?q=%s'%(email))
	soup=BeautifulSoup(req.content, "lxml")
	atag=soup.findAll('a',{'class':'title title-link antialiased j-slideshow-title'})
	slides={}
	for at in atag:
		slides[at.text]=at['href']
	return slides

def emailscribddocs(email):
	req = requests.get('https://www.scribd.com/search?page=1&content_type=documents&query=%s'%(email))
	soup=BeautifulSoup(req.content, "lxml")
	m = re.findall('(?<=https://www.scribd.com/doc/)\w+', req.text.encode('UTF-8'))
	m = set(m)
	m = list(m)
	links=[]
	length=len(m)
	for lt in range(0,length-1):
		links.append("https://www.scribd.com/doc/"+m[lt])
	return links
	
	
'''hbp = haveIbeenpwned(email)
for x in hbp:
	print "Pwned at %s Instances\n" % len(hbp)
	print "Title:%s\nBreachDate%s\nPwnCount%s\nDescription%s\nDataClasses%s\n" % (x['Title'], x['BreachDate'], x['PwnCount'], x['Description'],x['DataClasses'])
print "\n-----------------------------\n"
'''
print "\t\t\t[+] Finding user information based on emailId\n"

data = fullcontact(email)
if data.get("status","") == 200:
	print "Name: %s" % data.get("contactInfo","").get('fullName', '')
	print "\nOrganizations:"
	for x in data.get("organizations",""):
		if x.get('isPrimary', '') == True:
			primarycheck = " - Primary"
		else:
			primarycheck = ""
		if x.get('endDate','') == '':
			print "\t%s at %s - (From %s to Unknown Date)%s" % (x.get('title', ''), x.get('name',''), x.get('startDate',''), primarycheck)
		else:
			print "\t%s - (From %s to %s)%s" % (x.get('name',''), x.get('startDate',''), x.get('endDate',''), primarycheck)
	if data.get("contactInfo","").get('websites', '') != "":
		print "\nWebsite(s):"
		for x in data.get("contactInfo","").get('websites', ''):
			print "\t%s" % x.get('url', '')
	if data.get("contactInfo","").get('chats', '') != "":
		print '\nChat Accounts'
		for x in data.get("contactInfo","").get('chats', ''):
			print "\t%s on %s" % (x.get('handle', ''), x.get('client', ''))
	
	print "\nSocial Profiles:"
	for x in data.get("socialProfiles",""):
		print "\t%s:" % x.get('type','').upper()
		for y in x.keys():
			if y != 'type' and y != 'typeName' and y != 'typeId':
				print '\t%s: %s' % (y, x.get(y,''))
		print ''

	print "Other Details:"
	if data.get("demographics","") != "":
		print "\tGender: %s" % data.get("demographics","").get('gender', '')
		print "\tCountry: %s" % data.get("demographics","").get('country', '')
		print "\tTentative City: %s" % data.get("demographics","").get('locationGeneral', '')

	print "Photos:"
	for x in data.get("photos",""):
		print "\t%s: %s" % (x.get('typeName', ''), x.get('url', ''))

else:
	print 'Error Occured - Encountered Status Code: %s' % data.get("status","")



'''clb_data = clearbit(email)
for x in clb_data.keys():
	print '%s details:' % x
	if type(clb_data[x]) == dict:
		for y in clb_data[x].keys():
			if clb_data[x][y] is not None:
				print "%s:  %s, " % (y, clb_data[x][y])
	elif clb_data[x] is not None:
		print "\n%s:  %s" % (x, clb_data[x])

print "\n-----------------------------\n"

print "\t\t\t[+] Gravatar Link\n"
print gravatar(email)
print "\n-----------------------------\n"

print "\t\t\t[+] Associated Domains\n"
for doms in emaildom(email):
	print doms
'''
print "\n-----------------------------\n"

print "\t\t\t[+] Associated Slides\n"
slds=emailslides(email)
for tl,lnk in slds.items():
	print tl+"http://www.slideshare.net"+lnk
print "\n-----------------------------\n"

print "\t\t\t[+] Associated Scribd Docs\n"
scdlinks=emailscribddocs(email)
for sl in scdlinks:
	print sl
print ""
print "More results might be available:"
print "https://www.scribd.com/search?page=1&content_type=documents&query="+email
print "\n-----------------------------\n"


