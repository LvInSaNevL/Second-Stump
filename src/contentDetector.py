import os
from datetime import datetime, time
import time
import json
import praw
import threading
from filelock import Timeout, FileLock

from utils import prettyPrint, bcolors, fullPath
from videoSpliter import cut_video
from videoEditor import VideoFormatter

# List of sources from various websites
ytSources = ["https://www.youtube.com/watch?v=cRguIOOiktg"]
redditSources = ["holdmycosmo",
                 "whatcouldgowrong",
                 "holdmybeer",
                 "perfectlycutscreams",
                 "ContagiousLaughter",
                 "funnyvideos"]

# Runs through the youtube sources and finds any new content to download
def youtube_detector(timestamp):
    # Downloading all the YouTube Sources
    for vid in ytSources:
        prettyPrint(bcolors.ENDC, os.popen("youtube-dl -o \"{}\" -f mp4 {}".format(fullPath("data/rawVideos/%(id)s.mp4"), fullPath(vid))).read())

    # Editing each of the videos
    for targetVid in os.listdir("data/rawVideos"):
        cut_video(targetVid)

# Runs through the reddit sources and finds any new content to download
def reddit_detector(timestamp, source):
    # Gets the creds from disk
    with open(fullPath("data/auth.json")) as jsonfile:
        auth = json.load(jsonfile)
    # Configures PRAW creds
    prettyPrint(bcolors.OKBLUE, "Authenticating provided credentials")
    redditAuth = praw.Reddit(client_id=auth['reddit']['client_id'],
                     client_secret=auth['reddit']['client_secret'],
                     user_agent=auth['reddit']['user_agent'],
                     username=auth['reddit']['username'],                     
                     password=auth['reddit']['password'])

    prettyPrint(bcolors.OKBLUE, "Checking and downloading content from {}".format(source))
    # Generates a list of moderators, this allows us to filter out their posts
    mods = [] 
    for moderator in redditAuth.subreddit(source).moderator():
        mods.append(str(moderator))

    # Downloads all of the videos
    for targetSubmission in redditAuth.subreddit(source).hot():
        if not (os.path.exists(fullPath("data/rawClips/{}.mp4".format(targetSubmission.id)))) and not (os.path.exists(fullPath("data/rawClips/{}.mp4".format(targetSubmission.id)))):
            if not (str(targetSubmission.author) in mods):
                prettyPrint(bcolors.OKBLUE, "Thread {} is now downloading {} from {} on Reddit.".format(threading.currentThread().ident, targetSubmission.id, source))
                prettyPrint(bcolors.ENDC, os.popen("youtube-dl --no-continue -o \"{}\" {}".format(fullPath("data/rawClips/{}.mp4".format(targetSubmission.id)), targetSubmission.url)).read())
                fT = threading.Thread(target=VideoFormatter, args=(targetSubmission.id,))
                fT.start()
                
# The main entry point for content detection
# This is mostly just a manager for spinning up and down threads, but it also allows a single call for all sources
def detectorDirector():
    # Reddit Detector
    startTime = time.perf_counter()
    prettyPrint(bcolors.OKBLUE, "Checking reddit sources and downloading any new content")
    redditThreads = []
    for source in redditSources:
        t = threading.Thread(target=reddit_detector, args=(datetime.utcnow(), source))
        redditThreads.append(t)
        t.start()
    prettyPrint(bcolors.OKBLUE, "All threads finished, closing all active processes")
    for threads in redditThreads:
        threads.join()
    # A little alert to let the user know the function is over and how long it took
    endTime = time.perf_counter()
    prettyPrint(bcolors.OKGREEN, f"Reddit sources checked and new content downloaded. Process took {endTime - startTime:0.4f} seconds")