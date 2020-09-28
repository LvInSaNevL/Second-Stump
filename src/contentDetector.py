import os
import time
import json
import praw
from utils import prettyPrint, bcolors
from videoSpliter import cut_video

# List of sources from various websites
ytSources = ["https://www.youtube.com/watch?v=cRguIOOiktg"]
redditSources = ["TikTokCringe",
                 "holdmycosmo",
                 "Whatcouldgowrong",
                 "holdmybeer"]

# Runs through the youtube sources and finds any new content to download
def youtube_detector(timestamp):
    # Downloading all the YouTube Sources
    for vid in ytSources:
        prettyPrint(bcolors.ENDC, os.popen("youtube-dl -o \"data/rawVideos/%(id)s.mp4\" -f mp4 {}".format(vid)).read())

    # Editing each of the videos
    for targetVid in os.listdir("data/rawVideos"):
        cut_video(targetVid)

# Runs through the reddit sources and finds any new content to download
def reddit_detector(timestamp):
    prettyPrint(bcolors.OKBLUE, "Checking reddit sources and downloading any new content")
    startTime = time.perf_counter()
    # Gets the creds from disk
    with open("data/auth.json") as jsonfile:
        auth = json.load(jsonfile)
    # Configures PRAW creds
    prettyPrint(bcolors.OKBLUE, "Authenticating provided credentials")
    redditAuth = praw.Reddit(client_id=auth['reddit']['client_id'],
                     client_secret=auth['reddit']['client_secret'],
                     user_agent=auth['reddit']['user_agent'],
                     username=auth['reddit']['username'],                     
                     password=auth['reddit']['password'])

    # Loops through the video sources and downloads new content
    for targetSubreddit in redditSources:
        prettyPrint(bcolors.OKBLUE, "Checking and downloading content from {}".format(targetSubreddit))
        # Generates a list of moderators, this allows us to filter out their posts
        mods = [] 
        for moderator in redditAuth.subreddit(targetSubreddit).moderator():
            mods.append(str(moderator))

        # Downloads all of the videos
        for targetSubmission in redditAuth.subreddit(targetSubreddit).hot():
            if not (os.path.exists("data/rawClips/{}.mp4".format(targetSubmission.id))):
                if not (str(targetSubmission.author) in mods):
                    prettyPrint(bcolors.ENDC, os.popen("youtube-dl -o \"data/rawClips/{}.mp4\" {}".format(targetSubmission.id, targetSubmission.url)).read())
    
    # A little alert to let the user know the function is over and how long it took
    endTime = time.perf_counter()
    prettyPrint(bcolors.OKGREEN, f"Youtube sources checked and new content downloaded. Process took {endTime - startTime:0.4f} seconds")