#!/usr/bin/env python

import base
import json
import praw
import sys
import vault

from datetime import datetime
from collections import Counter
from operator import itemgetter
from prawcore.exceptions import NotFound
from termcolor import colored


ENABLED = True
EXTRA_VERBOSE = False


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print(colored(style.BOLD + '\n[+] Getting information from Reddit\n' +
                  style.END, 'blue'))


def submission_latest(redditor):
    if redditor.submissions.new(limit=1):
        for submission in redditor.submissions.new(limit=1):
            return str(submission.url.encode('utf-8'))
    else:
        return "No submissions"


def submission_stats(redditor):
    temp_submissions = {}
    top_posted_subreddits = {}
    for submission in redditor.submissions.new(limit=None):
        sub = str(submission.subreddit)
        if sub in temp_submissions:
            temp_submissions[sub] += 1
        else:
            temp_submissions[sub] = 1
    for k, v in sorted(list(temp_submissions.items()),
                       key=itemgetter(1), reverse=True)[:10]:
        top_posted_subreddits[k] = v
    return top_posted_subreddits


def submissions_top(redditor):
    top_s = []
    for submission in redditor.submissions.top('all', limit=10):
        sub = {}
        sub['Title'] = submission.title.encode('utf-8')
        sub['URL'] = submission.url.encode('utf-8')
        sub['Subreddit'] = str(submission.subreddit)
        sub['Created Date'] = datetime.fromtimestamp(submission.created).strftime("%D %H:%M")
        sub['Score'] = submission.score
        sub['Comments'] = submission.num_comments
        sub['Crossposts'] = submission.num_crossposts
        sub['Mature Content'] = submission.over_18
        if submission.media:
            if 'oembed' in submission.media:
                if 'url' in submission.media['oembed']:
                    sub['Embedded Media Description'] = submission.media['oembed']['description']
                if 'url' in submission.media['oembed']:
                    sub['Embedded Media URL'] = submission.media['oembed']['url']
            if 'reddit_video' in submission.media:
                if 'fallback_url' in submission.media['reddit_video']:
                    sub['Reddit Video URL'] = submission.media['reddit_video']['fallback_url']
        top_s.append(sub)
    return top_s


def comment_latest(redditor):
    if redditor.comments.new(limit=1):
        for comment in redditor.comments.new(limit=1):
            return str(comment.link_permalink.encode('utf-8'))
    else:
        return "No comments"


def comment_stats(redditor):
    temp_comments = {}
    top_commented_subreddits = {}
    for comment in redditor.comments.new(limit=None):
        sub = str(comment.subreddit)
        if sub in temp_comments:
            temp_comments[sub] += 1
        else:
            temp_comments[sub] = 1
    for k, v in sorted(list(temp_comments.items()),
                       key=itemgetter(1), reverse=True)[:10]:
        top_commented_subreddits[k] = v
    return top_commented_subreddits


def comments_top(redditor):
    top_c = []
    for comment in redditor.comments.top('all', limit=10):
        comm = {}
        comm['URL'] = comment.link_permalink.encode('utf-8')
        comm['Subreddit'] = str(comment.subreddit)
        comm['Date Posted'] = datetime.fromtimestamp(comment.created).strftime("%D %H:%M")
        comm['Score'] = comment.score
        comm['Mature Content'] = comment.over_18
        top_c.append(comm)
    return top_c


def controversial_stats(redditor):
    n = 0
    c_posts = []
    for controversial_post in redditor.submissions.controversial('all'):
        n += 1
        post = {}
        post['Title'] = controversial_post.title.encode('utf-8')
        post['URL'] = controversial_post.url.encode('utf-8')
        post['Subreddit'] = str(controversial_post.subreddit)
        post['Score'] = controversial_post.score
        post['Comments'] = controversial_post.num_comments
        post['Crossposts'] = controversial_post.num_crossposts
        post['Date Posted'] = datetime.fromtimestamp(controversial_post.created).strftime("%D %H:%M")
        if controversial_post.media:
            if 'oembed' in controversial_post.media:
                if 'description' in controversial_post.media['oembed']:
                    post['Embedded Media Description'] = controversial_post.media['oembed']['description']
                if 'url' in controversial_post.media['oembed']:
                    post['Embedded Media URL'] = controversial_post.media['oembed']['url']
            if 'reddit_video' in controversial_post.media:
                if 'fallback_url' in controversial_post.media['reddit_video']:
                    post['Reddit Video URL'] = controversial_post.media['reddit_video']['fallback_url']
        if controversial_post.media:
            if 'title' in controversial_post.media:
                post['Embedded Media Title'] = controversial_post.media['oembed']['title']
        if controversial_post.secure_media_embed:
            if 'media_domain_url' in controversial_post.media:
                post['Embedded Media URL'] = controversial_post.secure_media_embed['media_domain_url']
        c_posts.append(post)
    c_stats = {'Total': n, 'Post Details': c_posts}
    return c_stats


def redditor_stats(redditor):
    stats = {}
    stats['Comment Karma'] = redditor.comment_karma
    stats['Link Karma'] = redditor.link_karma
    stats['Verified Email'] = redditor.has_verified_email
    stats['Account Created'] = datetime.fromtimestamp(redditor.created).strftime("%D %H:%M")
    stats['Avatar URL'] = redditor.icon_img
    stats['Reddit Employee'] = redditor.is_employee
    stats['Reddit Gold'] = redditor.is_gold
    stats['Moderator'] = redditor.is_mod
    stats['Verified Account'] = redditor.verified
    stats['Latest Submission'] = submission_latest(redditor)
    stats['Latest Comment'] = comment_latest(redditor)
    return stats


def main(username):
    user_stats = {}
    reddit_id = vault.get_key('reddit_id')
    reddit_secret = vault.get_key('reddit_secret')
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret,
                         user_agent=user_agent)
    redditor = reddit.redditor(username)
    try:
        user_stats['Redditor Stats'] = redditor_stats(redditor)
        user_stats['Top 10 Submitted to Subreddits'] = submission_stats(redditor)
        user_stats['Top 10 Commented in Subreddits'] = comment_stats(redditor)
        if EXTRA_VERBOSE:
            user_stats['Top Submissions'] = submissions_top(redditor)
            user_stats['Top Comments'] = comments_top(redditor)
            user_stats['Contriversial Posts'] = controversial_stats(redditor)
    except NotFound as e:
        user_stats['Error'] = str(e)
        pass
    return user_stats


def output(data, username=""):
    if 'Error' in data:
        print(str(data['Error']))
        del data['Error']
    else:
        for k, v in list(data['Redditor Stats'].items()):
            print(str(k) + ": " + str(v))
        print(colored(style.BOLD + '\n---> Top Ten Submitted to Subreddits\n' +
                      style.END, 'blue'))
        for k, v in sorted(list(data['Top 10 Submitted to Subreddits'].items()),
                           key=itemgetter(1), reverse=True):
            print(str(k) + ": " + str(v))
        print(colored(style.BOLD + '\n---> Top Ten Commented in Subreddits\n' +
                      style.END, 'blue'))
        for k, v in sorted(list(data['Top 10 Commented in Subreddits'].items()),
                           key=itemgetter(1), reverse=True):
            print(str(k) + ": " + str(v))
        print("\n")
        if EXTRA_VERBOSE:
            print(colored(style.BOLD + '---> Top Submissions\n' +
                          style.END, 'blue'))
            for submission in sorted(data['Top Submissions'],
                                     key=itemgetter('Score'), reverse=True):
                for k, v in list(submission.items()):
                    print(str(k) + ": " + str(v))
                print("\n")
            print(colored(style.BOLD + '---> Top Comments\n' +
                          style.END, 'blue'))
            for submission in sorted(data['Top Comments'],
                                     key=itemgetter('Score'), reverse=True):
                for k, v in list(submission.items()):
                    print(str(k) + ": " + str(v))
                print("\n")
            print(colored(style.BOLD + '---> Contriversial Posts\n' +
                          style.END, 'blue'))
            print("\nTotal: " + str(data['Contriversial Posts']['Total']))
            print("\nSee file output (if enabled) for more details. Due to API")
            print("limitations only the last 100 Contriversial posts can be accessed.")
            print("\n")


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print(e)
        print("Please provide a username as argument")
