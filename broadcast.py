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
import threading
from threading import Thread

# Shared instance of the API that should be modified by the threads
api = []

# Main entry location for the script to run
def main():
    global api
    # To start with we will load the admin user name and passwords
    [ADMIN_USERNAME,ADMIN_ID] = getAdminCredentials('./admin.txt')
    [BROADCAST_USERNAME,BROADCAST_PASSWORD] = getBroadcasterCredentials('./login.txt')

    # Now we will define the API for InstagramAPI
    api = InstagramAPI(BROADCAST_USERNAME, BROADCAST_PASSWORD, debug=False)
    api.login()
    api.USER_AGENT = 'Instagram 39.0.0.19.93 Android'

    # With this there are now two process loops.  The first is to run the broadcaster
    # and the second is to look for any DM commands coming in from the admin account
    # We will run these two methods on diffrent threads
    Thread(target = pollAdminCommands,args=[]).start()
    # Initial command will always play the simpsons by default
    Thread(target = runBroadcast,args=[]).start()


def pollAdminCommands():
    global api
    print ('Starting up the admin thread')
    # Now we can start the polling of the incoming commands
    last_admin_command_thread_ID = [] # The first DM from the admin is not usable
    while True:
        # Wait 5 seconds between checking for admin messages
        time.sleep(5)
        api.getv2Inbox()
        for i in range(0,1):
            item_ID = api.LastJson['inbox']['threads'][0]['items'][0]['item_id']
            print (item_ID)
            command_str = api.LastJson['inbox']['threads'][0]['items'][0]['text']
            latest_DM_username_pk = api.LastJson['inbox']['threads'][0]['users'][0]['pk']
            latest_DM_username_un = api.LastJson['inbox']['threads'][0]['users'][0]['username']
            print(command_str)
            print (str(item_ID) + ":" +str(last_admin_command_thread_ID))
            print(latest_DM_username_un)

            if latest_DM_username_un in ['kapastor']:
                if not last_admin_command_thread_ID:
                        # First call to the command_str
                        last_admin_command_thread_ID = item_ID
                elif item_ID not in last_admin_command_thread_ID:
                        last_admin_command_thread_ID = item_ID
                        # Now check the command string
                        print(command_str)


def runBroadcast():
    global api
    print ('Starting up the broadcast thread')

# Returns the username and ID of the admin account for instagram commands
def getAdminCredentials(admin_path):
    print ('Retrieving the admin credentials...')
    with open(admin_path, 'r') as myfile:
        ADMIN_ID = myfile.read().replace('\n', '')
    ADMIN_ID = [x.strip() for x in ADMIN_ID.split(',')]
    ADMIN_USERNAME = ADMIN_ID[0]
    ADMIN_ID = ADMIN_ID[1]
    print ('Retrieving the admin credentials...DONE')

    return [ADMIN_USERNAME,ADMIN_ID]

# Returns the broadcaster information
def getBroadcasterCredentials(broadcaster_path):
    print ('Retrieving the broadcaster credentials...')
    with open(broadcaster_path, 'r') as myfile:
        LOGIN = myfile.read().replace('\n', '')
    LOGIN = [x.strip() for x in LOGIN.split(',')]
    BROADCAST_USERNAME = LOGIN[0]
    BROADCAST_PASSWORD = LOGIN[1]
    print ('Retrieving the broadcaster credentials...DONE')

    return [BROADCAST_USERNAME,BROADCAST_PASSWORD]

main()
#
#
#
# # Define the last timestamp from incomming commands
#
# broadcast_id = []
# # Now we will get the account information that we will broadcast from
#
#
#
# # Start the main Loop
# while True:
#     # Lets sleep for a second
#     time.sleep(1)
#     # Now we should check to see if any messages are around
#     api.getv2Inbox()
#     print(api.LastJson['inbox']['threads'])
#     for i in range(0,1):
#         print(i)
#         item_ID = api.LastJson['inbox']['threads'][0]['items'][0]['item_id']
#         command_str = api.LastJson['inbox']['threads'][0]['items'][0]['text']
#         latest_DM_username_pk = api.LastJson['inbox']['threads'][0]['users'][0]['pk']
#         latest_DM_username_un = api.LastJson['inbox']['threads'][0]['users'][0]['username']
#         print(command_str)
#         print (str(item_ID) + ":" +str(last_admin_command_thread_ID))
#         print(latest_DM_username_un)
#
#         if latest_DM_username_un in ['kapastor']:
#             if not last_admin_command_thread_ID:
#                     # First call to the command_str
#                     last_admin_command_thread_ID = item_ID
#             elif item_ID not in last_admin_command_thread_ID:
#                     last_admin_command_thread_ID = item_ID
#                     # Now check the command string
#                     print(command_str)
#                     if command_str in ['!restart']:
#                         #api.direct_message('This is a help outcome!',str(latest_DM_username_pk))
#                         #api.getv2Inbox()
#                         if broadcast_id:
#                             api.stopBroadcast(broadcast_id)
#
#                         MEDIA_FOLDER = './Media/TheSimpsons/S01'
#                         episode_list = [];
#                         for file in os.listdir(MEDIA_FOLDER):
#                             if file.endswith(".avi"):
#                                 episode_list.append(os.path.join(MEDIA_FOLDER, file))
#
#                         for episode in episode_list:
#
#                             # Start up the broadcast
#                             FILE_PATH = episode
#                             PUBLISH_TO_LIVE_FEED = False
#                             SEND_NOTIFICATIONS = False
#
#                             api.createBroadcast()
#                             broadcast_id = api.LastJson['broadcast_id']
#                             upload_url = api.LastJson['upload_url']
#
#                             # we now start a boradcast - it will now appear in the live-feed of users
#                             api.startBroadcast(broadcast_id, sendNotification=SEND_NOTIFICATIONS)
#                             ffmpeg_cmd = "ffmpeg -rtbufsize 256M -re -i '{file}' -vf 'transpose=1' -acodec libmp3lame -ar 44100 -b:a 256k -pix_fmt yuv420p -profile:v baseline -s 720x1280 -bufsize 6000k -vb 400k -maxrate 1500k -deinterlace -vcodec libx264 -preset veryfast -g 30 -r 30 -f flv '{stream_url}'".format(
#                                 file=FILE_PATH,
#                                 stream_url=upload_url.replace(':443', ':80', ).replace('rtmps://', 'rtmp://'),
#                             )
#
#                             print("Hit Ctrl+C to stop broadcast")
#                             try:
#                                 subprocess.call(ffmpeg_cmd, shell=True)
#                             except KeyboardInterrupt:
#                                 print('Stop Broadcasting')
#
#                             assert api.stopBroadcast(broadcast_id)
#
#
#
#
#
#
# #
# # api.searchUsername(ADMIN_USERNAME)
# # ADMIN_ID = api.LastJson["user"]["pk"]
# # print(ADMIN_ID)
# # #
# # #
# # api.getv2Inbox()
# # print(api.LastJson)
# # api.direct_message('aaaaa','19688985')
# # #
# #
# #
#
# # # Now we start the check Loop
# # while True:
# #     time.sleep(1)
# #
# # #
# # # MEDIA_FOLDER = './Media/TheSimpsons/S01'
# # #
# # # # Get the caption:
# # # with open(MEDIA_FOLDER + '/Caption.txt', 'r') as myfile:
# # #     CAPTION = myfile.read().replace('\n', '')
# # # with open(MEDIA_FOLDER + '/hashtags.txt', 'r') as myfile:
# # #     HASHTAGS = myfile.read().replace('\n', '')
# # # # Get the episode list:
# # # episode_list = [];
# # # for file in os.listdir(MEDIA_FOLDER):
# # #     if file.endswith(".avi"):
# # #         episode_list.append(os.path.join(MEDIA_FOLDER, file))
# # #
# # #
# # # iteration = 1
# # # # Loop over all of the episode_list
# # # while True:
# # #     for episode in episode_list:
# # #         full_episode_caption = "ITERATION: " + str(iteration) + " \\\ " + CAPTION + " " + episode + " " + HASHTAGS
# # #         # Post the update:
# # #         photo_path = MEDIA_FOLDER + '/post.jpg'
# # #         api.uploadPhoto(photo_path, caption=full_episode_caption)
# # #
# # #         # Start up the broadcast
# # #         FILE_PATH = episode
# # #         PUBLISH_TO_LIVE_FEED = False
# # #         SEND_NOTIFICATIONS = False
# # #
# # #         assert api.createBroadcast()
# # #         broadcast_id = api.LastJson['broadcast_id']
# # #         upload_url = api.LastJson['upload_url']
# # #
# # #         # we now start a boradcast - it will now appear in the live-feed of users
# # #         assert api.startBroadcast(broadcast_id, sendNotification=SEND_NOTIFICATIONS)
# # #         ffmpeg_cmd = "ffmpeg -rtbufsize 256M -re -i '{file}' -vf 'transpose=1' -acodec libmp3lame -ar 44100 -b:a 256k -pix_fmt yuv420p -profile:v baseline -s 720x1280 -bufsize 6000k -vb 400k -maxrate 1500k -deinterlace -vcodec libx264 -preset veryfast -g 30 -r 30 -f flv '{stream_url}'".format(
# #             file=FILE_PATH,
# #             stream_url=upload_url.replace(':443', ':80', ).replace('rtmps://', 'rtmp://'),
# #         )
# #
# #         print("Hit Ctrl+C to stop broadcast")
# #         try:
# #             subprocess.call(ffmpeg_cmd, shell=True)
# #         except KeyboardInterrupt:
# #             print('Stop Broadcasting')
# #
# #         assert api.stopBroadcast(broadcast_id)
# #
# #         print('Finished Broadcast')
# #
# #         if PUBLISH_TO_LIVE_FEED:
# #             api.addBroadcastToLive(broadcast_id)
# #             print('Added Broadcast to LiveFeed')
# #
# #     iteration = iteration + 1
