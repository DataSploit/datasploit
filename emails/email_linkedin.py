#!/usr/bin/env python

import base
import requests
import sys
import vault
import json
from lxml import etree
import re
from termcolor import colored

ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def main(email):
    linkedin_user = vault.get_key('linkedin_user')
    linkedin_pass = vault.get_key('linkedin_pass')
    if (linkedin_user != None and linkedin_pass != None):
        # Login process
        s = requests.Session()
        r = s.get('https://www.linkedin.com/')
        tree = etree.HTML(r.content)
        loginCsrfParam = ''.join(tree.xpath(
            '//input[@id="loginCsrfParam-login"]/@value'))

        payload = {
            'session_key': linkedin_user,
            'loginCsrfParam': loginCsrfParam,
            'session_password': linkedin_pass,
        }
        req = s.post("https://www.linkedin.com/uas/login-submit?" +
                    "loginSubmitSource=GUEST_HOME", data=payload)
        for cookie in s.cookies:
            if "JSESSIONID" in str(cookie):
                csrfToken = re.findall('JSESSIONID=([^ ]*)', str(cookie))

        url = "https://www.linkedin.com/sales/gmail/profile/" + \
            "viewByEmail/%s" % email
        req = s.get(url)
        found = False
        if "Sorry, we couldn't find a matching LinkedIn" not in req.content:
            url = "https://www.linkedin.com/sales/gmail/profile/proxy/%s" % \
                (email)
            found = True
            req = s.get(url)
            id = re.findall(
                '\/voyager\/api\/identity\/profiles\/([a-z]*)\/profileView',
                req.text)
            url = "https://www.linkedin.com/voyager/api/identity/profiles/" + \
                id[0] + "/profileView"
            s.headers.update({'csrf-token': csrfToken[0].replace('"', '')})
            req = s.get(url)
            content = re.sub("\. ?\n", ",\n", req.content)
            content = re.sub(" = ", " : ", content)

            data = json.loads(content)
            return data
        else:
            return [False, "NO_DATA"]
    else:
        return [False, "INVALID_API"]

def banner():
    print colored(style.BOLD + '\n---> Checking Linkedin..\n' + style.END, 'blue')


def date_convert(date):
    date_conv = str(date.get("year", ""))
    if (date.get("month")):
        date_conv = "%s-%02d" % (date_conv, int(date.get("month")))
    return date_conv


def output(data, email=""):
    if type(data) == list and data[1] == "INVALID_API":
        print colored(
                style.BOLD + '\n[-] Linkedin username and password not configured. Skipping Linkedin Search.\n' + style.END, 'red')
    elif type(data) == list and data[1] == "NO_DATA":
        print colored(
                style.BOLD + "\n[-] Linkedin email don't exist" + style.END, 'red')
    else:
        if data.get("profile", "") != "":
            print "Name: %s %s" % (data.get("profile", "").get("firstName", ""), data.get("profile", "").get("lastName", ""))
            print "\nBio:"
            print "  %s" % (data.get("profile", "").get("headline", ""))

        if data.get("certificationView", "") != "":
            print "\nCertifications:"
            for certificate in data.get("certificationView", "").get("elements", ""):
                print "\t%s - Authority: %s" % (certificate.get("name", ""), certificate.get("authority", ""))

                if (certificate.get("timePeriod", "") != ""):
                    if (certificate.get("timePeriod", "").get("endDate", "") == ""):
                        print "\t\t(From %s to Unknown Date)" % (date_convert(certificate.get("timePeriod", "").get("startDate", "")))
                    else:
                        print "\t\t(From %s to %s)" % (
                            date_convert(certificate.get("timePeriod", "").get("startDate", "")),
                            date_convert(certificate.get("timePeriod", "").get("endDate", "")))

        if data.get("educationView", "") != "":
            print "\nEducations:"
            for education in data.get("educationView", "").get("elements", ""):
                print "\t%s - School: %s" % (education.get("degreeName", ""), education.get("schoolName", ""))
                if (education.get("description", "") != ""):
                    print "\t\tDescription: %s" % (education.get("description", ""))

                if (education.get("timePeriod", "") != ""):
                    if (education.get("timePeriod", "").get("endDate", "") == ""):
                        print "\t\t(From %s to Unknown Date)" % (date_convert(education.get("timePeriod", "").get("startDate", "")))
                    else:
                        print "\t\t(From %s to %s)" % (
                            date_convert(education.get("timePeriod", "").get("startDate", "")),
                            date_convert(education.get("timePeriod", "").get("endDate", "")))

        if data.get("positionGroupView", "") != "":
            print "\nPositions:"
            for position in data.get("positionGroupView", "").get("elements", ""):
                print "\t%s - Title: %s" % (position.get("name", ""), position.get("positions")[0].get("title", ""))

                if (position.get("timePeriod", "").get("endDate", "") == ""):
                    print "\t\t(From %s to Unknown Date)" % (date_convert(position.get("timePeriod", "").get("startDate", "")))
                else:
                    print "\t\t(From %s to %s)" % (
                        date_convert(position.get("timePeriod", "").get("startDate", "")),
                        date_convert(position.get("timePeriod", "").get("endDate", "")))

        print "Other Details:"
        if data.get("profile", "").get("locationName", "") != "":
            print "\tLocation: %s" % data.get("profile", "").get("locationName", "")

        print "Photos:"
        # if data.get("profile", "").get("miniProfile", "") != "":
        if (data.get("profile").get("miniProfile", "") != "" and
            data.get("profile").get("miniProfile", "").get(
            "picture", "") != ""):
            rootUrl = data.get("profile").get("miniProfile", "").get(
                "picture", "").get("com.linkedin.common.VectorImage", "").get("rootUrl", "")
            shrink = data.get("profile").get("miniProfile", "").get(
                "picture", "").get("com.linkedin.common.VectorImage", "").get("artifacts", "")[3].get(
                    "fileIdentifyingUrlPathSegment", "")
            print "\tLinkedin: %s" % (rootUrl + shrink)


if __name__ == "__main__":
    try:
        email = sys.argv[1]
        banner()
        result = main(email)
        output(result, email)
    except Exception as e:
        print e
        print "Please provide an email as argument"
