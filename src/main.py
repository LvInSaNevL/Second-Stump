import os
import sys
import schedule
import time
from contentDetector import reddit_detector
from videoEditor import GenerateVideo
from utils import prettyPrint, bcolors, fullPath

# Checks to make sure the file structure exists, creates it if it doesnt
fileStructure = ["data",
                 "data/rawVideos",
                 "data/rawClips",
                 "data/sync_data",
                 "data/output"]

for dir in fileStructure:
    formatDir = fullPath(dir)
    if not os.path.exists(formatDir):
        prettyPrint(bcolors.ENDC, os.popen('mkdir {}'.format(formatDir)).read())

# Checks to see if the data/rawClips directory is empty, if it is we need to fill it before anything can happen
if (len(os.listdir(fullPath("data/rawClips"))) == 0):
    reddit_detector(time.localtime)

# If blocks to check for command line arguments to allow testing
if (sys.argv[1] == "update"):
    reddit_detector(time.localtime)
    exit()
if (sys.argv[1] == "new"):
    GenerateVideo()
    exit()
if (sys.argv[1] == "deploy"):
    # Sets up the schedule
    schedule.every(20).minutes.do(reddit_detector, time.localtime)  
    schedule.every().day.at("9:30").do(GenerateVideo)
    schedule.every().day.at("12:30").do(GenerateVideo)
    schedule.every().day.at("17:30").do(GenerateVideo)
    ### THIS WHILE LOOP IS THE MAIN LOOP ###
    while True:
        schedule.run_pending()
        time.sleep(1)
    exit()
else:
    print("Please use a valid command line argument")