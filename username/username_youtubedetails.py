#!/usr/bin/env python

import base
import vault
import httplib2
import os
import sys
import urllib.request, urllib.parse, urllib.error
from apiclient.discovery import build
from termcolor import colored


# Control whether the module is enabled or not
ENABLED = True


class style:
    BOLD = '\033[1m'
    END = '\033[0m'


def banner():
    print(colored(style.BOLD + '\n[+] Getting information from YouTube\n' +
                  style.END, 'blue'))


def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key, value in list(kwargs.items()):
            if value:
                good_kwargs[key] = value
    return good_kwargs


def get_channel_details(username, service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    results = service.channels().list(
        **kwargs
    ).execute()

    details = {}
    for result in results.get("items", []):
        # Localize some output through the api
        details['Localized Channel Title'] = result['snippet']["localized"]['title']
        details['Localized Description'] = result['snippet']["localized"]['description']
        details['Title'] = result['snippet']['title']
        details['Creation Date'] = result['snippet']['publishedAt']
        if 'country' in result['snippet']:
            details['Region'] = result['snippet']['country']
        details['Channel Comments'] = result['statistics']['commentCount']
        details['Channel Views'] = result['statistics']['viewCount']
        details['Channel Videos'] = result['statistics']['videoCount']
        details['Channel Subscriber'] = result['statistics']['subscriberCount']
        if 'url' in result['snippet']['thumbnails']['high']:
            url = result['snippet']['thumbnails']['high']['url']
            details['Avatar URL'] = url
            # save the profile image
            file_path = "profile_pic/%s" % username
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            path = file_path + "/youtube." + url.split('.')[-1]
            #urllib.urlretrieve(url, path)
        if 'customUrl' in result['snippet']:
            details["Full URL"] = str("https://www.youtube.com/channel/{id}"
                                      .format(id=result['snippet']['customUrl']))
        else:
            details["Full URL"] = str("https://www.youtube.com/channel/{id}"
                                      .format(id=result['id']))
        return details


def find_channel_by_username(service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    results = service.search().list(
        **kwargs
    ).execute()

    details = {}
    for result in results.get("items", []):
        if result['id']['kind'] == 'youtube#channel':
            details["Channel ID"] = result['snippet']['channelId']
        else:
            details = None
        # Assume the first result is the correct one. :|
        return details


def analyze_activity(service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)
    results = service.activities().list(
        **kwargs
    ).execute()

    recent_likes = {}
    recent_uploads = {}
    recent_playlist_items = {}
    for result in results.get("items", []):
        if result['snippet']['type'] == 'like':
            video_title = str(result['snippet']['title'].encode('utf-8'))
            video_description = result['snippet']['description']
            video_url = str("https://www.youtube.com/watch?v={id}"
                            .format(id=result['contentDetails']['like']['resourceId']['videoId']))
            recent_likes[video_url] = { 'Title': video_title, 'Description': video_description }
        recent_likes["Recently Liked Videos"] = str(len(recent_likes) - 1)
        if result['snippet']['type'] == 'upload':
            video_title = str(result['snippet']['title'].encode('utf-8'))
            video_description = result['snippet']['description']
            video_url = str("https://www.youtube.com/watch?v={id}"
                            .format(id=result['contentDetails']['upload']['videoId']))
            recent_uploads[video_url] = { 'Title': video_title, 'Description': video_description }
        recent_uploads["Recently Uploaded Videos"] = str(len(recent_uploads) - 1)
        if result['snippet']['type'] == 'playlistItem':
            video_title = str(result['snippet']['title'].encode('utf-8'))
            video_description = result['snippet']['description']
            video_url = str("https://www.youtube.com/watch?v={id}"
                            .format(id=result['contentDetails']['playlistItem']['resourceId']['videoId']))
            playlist_url = str("https://www.youtube.com/playlist?list={id}"
                               .format(id=result['contentDetails']['playlistItem']['playlistId']))
            if playlist_url in recent_playlist_items:
                # This could be a lot cleaner.
                wip_dict = recent_playlist_items[playlist_url].copy()
                new_dict = { video_title: { 'Description': video_description, 'Video URL': video_url } }
                wip_dict.update(new_dict)
                recent_playlist_items[playlist_url] = wip_dict
            else:
                recent_playlist_items[playlist_url] = { video_title: { 'Description': video_description, 'Video URL': video_url } }
        recent_playlist_items["Recently Updated Playlists"] = str(len(recent_playlist_items) - 1)
    channel_analysis = [ recent_likes, recent_uploads, recent_playlist_items ]

    return channel_analysis


def main(username):
    google_api = vault.get_key('google_api')
    if google_api != None:
        API_SERVICE_NAME = "youtube"
        API_VERSION = "v3"
        max_results = 50
        video_ids = []
        service = build(API_SERVICE_NAME, API_VERSION,
                        developerKey=google_api)
        channel_id = find_channel_by_username(service,
                                              part='snippet',
                                              maxResults=max_results,
                                              q=username)
        if channel_id is not None:
            channel_details = get_channel_details(username,
                                                  service,
                                                  part='snippet,contentDetails,statistics',
                                                  id=channel_id['Channel ID'])

            channel_analysis = analyze_activity(service,
                                                part='snippet,contentDetails',
                                                channelId=channel_id['Channel ID'],
                                                maxResults=max_results)
            return [ channel_id, channel_details, channel_analysis ]
        else:
            return [ colored(style.BOLD +'[!] Error: Channel not found for ' +
                             username + '\n' + style.END, 'red') ]
    else:
        return [ colored(style.BOLD + '[!] Error: No Google API key found. Skipping' +
                         style.END, 'red') ]


def output(data, username=""):
    for i in data:
        if type(i) == type(dict()):
            for k,v in i.items():
                # Don't feed more detailed dictionaries to the console
                if type(v) != type(dict()):
                    print(k + ': ' +  v)
        elif type(i) == type(list()):
            for v in i:
                if type(v) == type(dict()):
                    for k,v in v.items():
                        if type(v) != type(dict()):
                            print(k + ': ' +  v)
                else:
                    print(v)
        else:
            if "[!]" in i:
                print(i)
                data.remove(i)
            else:
                print(i)


if __name__ == "__main__":
    try:
        username = sys.argv[1]
        banner()
        result = main(username)
        output(result, username)
    except Exception as e:
        print(e)
        print("Please provide a username as argument")
