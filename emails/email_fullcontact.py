#!/usr/bin/env python

import base
import requests
import sys
import config as cfg
import json
from termcolor import colored

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def main(email):
    if cfg.fullcontact_api != "":
        req = requests.get("https://api.fullcontact.com/v2/person.json?email=%s" % email,
                           headers={"X-FullContact-APIKey": cfg.fullcontact_api})
        data = json.loads(req.content)
        return data
    else:
        return [False, "INVALID_API"]


def banner():
    print colored(style.BOLD + '\n---> Checking Fullcontact..\n' + style.END, 'blue')


def output(data, email=""):
    if type(data) == list and data[1] == "INVALID_API":
        print colored(
                style.BOLD + '\n[-] Full-Contact API Key not configured. Skipping Fullcontact Search.\nPlease refer to https://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red')
    else:
        if data.get("status", "") == 200:
            if data.get("contactInfo", "") != "":
                print "Name: %s" % data.get("contactInfo", "").get('fullName', '')
            print "\nOrganizations:"
            for x in data.get("organizations", ""):
                if x.get('isPrimary', ''):
                    primarycheck = " - Primary"
                else:
                    primarycheck = ""
                if x.get('endDate', '') == '':
                    print "\t%s at %s - (From %s to Unknown Date)%s" % (
                        x.get('title', ''), x.get('name', ''), x.get('startDate', ''), primarycheck)
                else:
                    print "\t%s - (From %s to %s)%s" % (
                        x.get('name', ''), x.get('startDate', ''), x.get('endDate', ''), primarycheck)
            if data.get("contactInfo", "") != "":
                if data.get("contactInfo", "").get('websites', '') != "":
                    print "\nWebsite(s):"
                    for x in data.get("contactInfo", "").get('websites', ''):
                        print "\t%s" % x.get('url', '')
                if data.get("contactInfo", "").get('chats', '') != "":
                    print '\nChat Accounts'
                    for x in data.get("contactInfo", "").get('chats', ''):
                        print "\t%s on %s" % (x.get('handle', ''), x.get('client', ''))

            print "\nSocial Profiles:"
            for x in data.get("socialProfiles", ""):
                print "\t%s:" % x.get('type', '').upper()
                for y in x.keys():
                    if y != 'type' and y != 'typeName' and y != 'typeId':
                        print '\t%s: %s' % (y, x.get(y, ''))
                print ''

            print "Other Details:"
            if data.get("demographics", "") != "":
                print "\tGender: %s" % data.get("demographics", "").get('gender', '')
                print "\tCountry: %s" % data.get("demographics", "").get('country', '')
                print "\tTentative City: %s" % data.get("demographics", "").get('locationGeneral', '').encode('utf-8')

            print "Photos:"
            for x in data.get("photos", ""):
                print "\t%s: %s" % (x.get('typeName', ''), x.get('url', ''))

        else:
            print 'Error Occured - Encountered Status Code: %s. Please check if Email_id exist or not?' % data.get("status",
                                                                                                                   "")


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
