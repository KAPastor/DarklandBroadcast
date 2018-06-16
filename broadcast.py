#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Use text editor to edit the script and type in valid Instagram username/password

import subprocess
import time
import requests
import urllib.request
import json
from InstagramAPI import InstagramAPI
import os

# Pre- Main loop things to do:
# Get the admin account USERNAME (this file is not committed)
with open('./admin.txt', 'r') as myfile:
    ADMIN_USERNAME = myfile.read().replace('\n', '')
ADMIN_USERNAME = [x.strip() for x in ADMIN_USERNAME.split(',')]

# Now we will get the account information that we will broadcast from
with open('./login.txt', 'r') as myfile:
    LOGIN = myfile.read().replace('\n', '')
LOGIN = [x.strip() for x in LOGIN.split(',')]
BROADCAST_USERNAME = LOGIN[0]
BROADCAST_PASSWORD = LOGIN[1]

# In order to have admin's pass messages to the system via DM's we need to get
# the user ID from the user name.  To do this we need to instance the api
api = InstagramAPI(BROADCAST_USERNAME, BROADCAST_PASSWORD, debug=False)
assert api.login()
api.USER_AGENT = 'Instagram 39.0.0.19.93 Android'

api.searchUsername(ADMIN_USERNAME)
ADMIN_ID = api.LastJson["user"]["pk"]
print(ADMIN_ID)
#
#
# InstagramAPI.getv2Inbox()
# print(InstagramAPI.LastJson)
# InstagramAPI.direct_message('aaaaa','19688985')
# #
#
#
# url="https://www.instagram.com/kapastor/?__a=1"
# request = urllib.request.Request(url)
#
# request.add_header('User-Agent',"cheese")
#
# data = urllib.request.urlopen(request).read()
#
#
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
# response = requests.get(url, headers=headers)
#
#
# print(response)
#
#
#
#
#
#
# user_id = get_id('kapastor')
# print(user_id)
# # api.direct_message('Hellooooo','19688985')
#
# # Now we start the check Loop
# while True:
#     time.sleep(1)
#
# #
# # MEDIA_FOLDER = './Media/TheSimpsons/S01'
# #
# # # Get the caption:
# # with open(MEDIA_FOLDER + '/Caption.txt', 'r') as myfile:
# #     CAPTION = myfile.read().replace('\n', '')
# # with open(MEDIA_FOLDER + '/hashtags.txt', 'r') as myfile:
# #     HASHTAGS = myfile.read().replace('\n', '')
# # # Get the episode list:
# # episode_list = [];
# # for file in os.listdir(MEDIA_FOLDER):
# #     if file.endswith(".avi"):
# #         episode_list.append(os.path.join(MEDIA_FOLDER, file))
# #
# #
# # iteration = 1
# # # Loop over all of the episode_list
# # while True:
# #     for episode in episode_list:
# #         full_episode_caption = "ITERATION: " + str(iteration) + " \\\ " + CAPTION + " " + episode + " " + HASHTAGS
# #         # Post the update:
# #         photo_path = MEDIA_FOLDER + '/post.jpg'
# #         api.uploadPhoto(photo_path, caption=full_episode_caption)
# #
# #         # Start up the broadcast
# #         FILE_PATH = episode
# #         PUBLISH_TO_LIVE_FEED = False
# #         SEND_NOTIFICATIONS = False
# #
# #         assert api.createBroadcast()
# #         broadcast_id = api.LastJson['broadcast_id']
# #         upload_url = api.LastJson['upload_url']
# #
# #         # we now start a boradcast - it will now appear in the live-feed of users
# #         assert api.startBroadcast(broadcast_id, sendNotification=SEND_NOTIFICATIONS)
# #         ffmpeg_cmd = "ffmpeg -rtbufsize 256M -re -i '{file}' -vf 'transpose=1' -acodec libmp3lame -ar 44100 -b:a 256k -pix_fmt yuv420p -profile:v baseline -s 720x1280 -bufsize 6000k -vb 400k -maxrate 1500k -deinterlace -vcodec libx264 -preset veryfast -g 30 -r 30 -f flv '{stream_url}'".format(
#             file=FILE_PATH,
#             stream_url=upload_url.replace(':443', ':80', ).replace('rtmps://', 'rtmp://'),
#         )
#
#         print("Hit Ctrl+C to stop broadcast")
#         try:
#             subprocess.call(ffmpeg_cmd, shell=True)
#         except KeyboardInterrupt:
#             print('Stop Broadcasting')
#
#         assert api.stopBroadcast(broadcast_id)
#
#         print('Finished Broadcast')
#
#         if PUBLISH_TO_LIVE_FEED:
#             api.addBroadcastToLive(broadcast_id)
#             print('Added Broadcast to LiveFeed')
#
#     iteration = iteration + 1
