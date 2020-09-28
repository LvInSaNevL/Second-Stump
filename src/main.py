import os
import sys
import schedule
import time
from contentDetector import reddit_detector
from videoEditor import GenerateVideo
from utils import prettyPrint, bcolors

# Main navigator
def timeManager(upload):
    if upload:
        reddit_detector(time.localtime)
        GenerateVideo()
    else:
        reddit_detector(time.localtime)

# Checks to make sure the file structure exists, creates it if it doesnt
fileStructure = ["data",
                 "data/rawVideos",
                 "data/rawClips"]

for dir in fileStructure:
    if not os.path.exists(dir):
        prettyPrint(bcolors.ENDC, os.popen('mkdir {}'.format(dir)).read())

# Checks to see if the data/rawClips directory is empty, if it is we need to fill it before anything can happen
if (len(os.listdir("data/rawClips")) == 0):
    timeManager(False)

# If blocks to check for command line arguments to allow testing
if (sys.argv[1] == "update"):
    timeManager(False)
    exit()
if (sys.argv[1] == "new"):
    timeManager(True)
    exit()
if (sys.argv[1] == "deploy"):
    # Sets up the schedule
    schedule.every(20).minutes.do(timeManager(False)) 
    schedule.every().day.at("9:30").do(timeManager(True))
    schedule.every().day.at("12:30").do(timeManager(True))
    schedule.every().day.at("17:30").do(timeManager(True))
    ### THIS WHILE LOOP IS THE MAIN LOOP ###
    while True:
        schedule.run_pending()
        time.sleep(1)
    exit()
else:
    print("Please use a valid command line argument")