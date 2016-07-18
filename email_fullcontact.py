import requests
import sys
import config as cfg
import clearbit
import json
import time
import hashlib
from bs4 import BeautifulSoup
import re



def fullcontact(email):
	req = requests.get("https://api.fullcontact.com/v2/person.json?email=%s&apiKey=%s" % (email, cfg.fullcontact_api))
	data = json.loads(req.content)
	return data


email_id = sys.argv[1]
data = fullcontact(email_id)
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

