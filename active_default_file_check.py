import requests
import re
import sys

list_urls = open("check_urls.txt")
existing_urls = []
host = sys.argv[1]
base_url = "http://" + host + "/"
print base_url

def check_page(url):
		req = requests.get(url)
		return req

#Checking non existig page
base_req = requests.get(base_url + "rejgwterlbjwfnvierwebjrwfebelivajr")
print "Setting base request code for non_existing page as " + str(base_req.status_code)
base_statuscode = base_req.status_code


#Check for any random non-existing-page
for read_from_file in list_urls:
	pagetohit = read_from_file.strip("\n")
	print "Checking %s" % (pagetohit)
	if (check_page(base_url + pagetohit).status_code != base_statuscode):
		existing_urls.append(base_url + pagetohit)
	else:
		pass

if (len(existing_urls) != 0):
	print "\n[+] Testing done, following URLs are existing."
	for foundpages in existing_urls:
		print foundpages
	print "\n"
	print "Note: Different status_code were returned which means file exist. \nIn certain cases, application might be restricting file access by returning \n403 forbidden / Rate limiting which verifies that file exist.\n"
else:
	"[-] No luck buddy..:("
