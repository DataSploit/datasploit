import sys
import requests
from bs4 import BeautifulSoup
import json


def github_search(query, code):
	print "\t\t\t[+] Searching domain results in github" + code + ":" + query + "\n"
	endpoint_git =  "https://github.com/search?q=\"" + query + "\"&type=" + code
	req = requests.get(endpoint_git) 
	soup = BeautifulSoup(req.content, 'html.parser')
	mydivs = soup.findAll("span", { "class" : "counter" })
	if mydivs and len(mydivs) >= 1:
		return "%s Results found in github Codes. \nExplore results manually: %s" % (str(mydivs[0]).split(">")[1].split("<")[0], endpoint_git)
	else:
		return None


def main():
	domain = sys.argv[1]
	#make Search github code for the given domain.
	git_results = github_search(domain, 'Code')
	if git_results is not None:
		print git_results
	else:
		print "Sad! Nothing found on github"
	print "\n-----------------------------\n"

if __name__ == "__main__":
	main()


