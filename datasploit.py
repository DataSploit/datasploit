#!/usr/bin/env python
import sys
import re
import os

def printart():
    print "\n\t  ____/ /____ _ / /_ ____ _ _____ ____   / /____  (_)/ /_"
    print "\t  / __  // __ `// __// __ `// ___// __ \ / // __ \ / // __/"
    print "\t / /_/ // /_/ // /_ / /_/ /(__  )/ /_/ // // /_/ // // /_  "
    print "\t \__,_/ \__,_/ \__/ \__,_//____// .___//_/ \____//_/ \__/  "
    print "\t                               /_/                        "
    print "\t\t\t\t\t\t"
    print "                Open Source Assistant for #OSINT            "
    print "                     website: www.datasploit.info               "
    print "\t"


def main(): 

    printart()
    print "User Input: "+ sys.argv[1]
    if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "--h":
        print "Usage datasploit.py <input>"
        print "We will try to autodetect the input and perform relevent OSINT"
    elif re.match('[^@]+@[^@]+\.[^@]+', sys.argv[1]):
        print "Looks like an EMAIL, running Email_OSINT...\n"
        command='./emailOsint.py '+sys.argv[1]
        # insecure way used-os.command**************. Do not expose to web interface
        os.system(command)
    #http://stackoverflow.com/questions/8022530/python-check-for-valid-email-address
    elif re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', sys.argv[1]):
        print "Looks like an IP, running IP_OSINT...\n"
        command='./ipOsint.py '+sys.argv[1]
        os.system(command)
    #http://stackoverflow.com/questions/10086572/ip-address-validation-in-python-using-regex
    elif re.match('^[a-zA-Z\d-]{,63}(\.[a-zA-Z\d-]{,63}).$', sys.argv[1]):
        print "Looks like a DOMAIN, running Domain_OSINT...\n"
        command='./domainOsint.py -d'+sys.argv[1]
        os.system(command)
    #http://stackoverflow.com/questions/8467647/python-domain-name-check-using-regex
    else:
        print "Looks like a Username, running Username_OSINT...\n"
        command='./usernameOsint.py '+sys.argv[1]
        os.system(command)



if __name__ == "__main__":
    main()
