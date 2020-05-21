#!/usr/bin/env python

import base
import vault
import sys
import json
import time
import requests
import traceback
from termcolor import colored

# Control whether the module is enabled or not
ENABLED = True
WRITE_TEXT_FILE = True
MODULE_NAME = "Git_Repos_Commits"


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print(colored(style.BOLD + '\n[+] Scraping Git for Repos and Commits' + style.END, 'blue'))
    print(colored(style.BOLD + '[!] This is BETA code, might not provide correct results\n' + style.END, 'red'))


def find_repos(username):
    access_token = vault.get_key('github_access_token')
    list_repos = []
    url = "https://api.github.com/users/%s/repos?access_token=%s" % (username, access_token)
    req = requests.get(url)
    if 'API rate limit exceeded' not in req.text:
        data = json.loads(req.content)
        if "message" in data and data['message'] == "Not Found":
            return []
        for repos in data:
            if not repos['fork']:
                list_repos.append(repos['full_name'])
        return list_repos
    else:
        return "API_LIMIT"


def find_commits(repo_name):
    list_commits = []
    access_token = vault.get_key('github_access_token')
    for x in range(1, 10):
        url = "https://api.github.com/repos/%s/commits?page=%s&access_token=%s" % (repo_name, x, access_token)
        req = requests.get(url)
        data = json.loads(req.content)
        for commits in data:
            try:
                list_commits.append(commits['sha'])
            except:
                pass
        if len(data) < 30:
            return list_commits
        time.sleep(1)
    return list_commits


def main(username):
    if vault.get_key('github_access_token') != None:
        repo_list = find_repos(username)
        master_list = {}
        if not repo_list == "API_LIMIT":
            for i in repo_list:
                master_list[i] = find_commits(i)
        return master_list
    else:
        return [False, "INVALID_API"]


def output(data, username=""):
    if type(data) == list:
        if data[1] == "INVALID_API":
            print(colored(
                 style.BOLD + '\n[-] Github Access Token not configured. Skipping Gi Search.\nPlease refer to http://datasploit.readthedocs.io/en/latest/apiGeneration/.\n' + style.END, 'red'))
    else:
        print("[+] Found %s repos for username %s\n" % (len(data), username))
        counter = 1
        for repo_name, commits in data.items():
            print("%s. %s (%s commits)" % (counter, repo_name, len(commits)))
            for commit in commits:
                print("\t%s" % commit)
            print("")
            counter += 1

def output_text(data):
	text_data = []
	for repo_name, commits in data.items():
		for commit in commits:
			text_data.append(commit)
	return "\n".join(text_data)


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("Please provide a username as argument")
