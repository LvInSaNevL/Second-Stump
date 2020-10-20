import os
import sys
import schedule
import time as t    
import threading

from contentDetector import detectorDirector
from videoEditor import GenerateVideo
from videoUploader import newUpload
from tooling import *


# The programs file structure, used to verify that everything is exactly where it needs to be
fileStructure = ["data/rawVideos",
                 "data/rawClips",
                 "data/sync_data",
                 "data/output"]

for dir in fileStructure:
    formatDir = fullPath(dir)
    if not os.path.exists(formatDir):
        prettyPrint(bcolors.ENDC, os.popen('mkdir {}'.format(formatDir)).read())

# Checks to see if the data/rawClips directory is empty, if it is we need to fill it before anything can happen
#if (len(os.listdir(fullPath("data/rawClips"))) == 0):
#    detectorDirector()

def main():
    times = [
        ["00", detectorDirector],
        ["20", detectorDirector],
        ["40", detectorDirector],
        ["50", GenerateVideo]
    ]
    spinner = spinning_cursor()
    processThreads = []

    while (True):
        # Fancy CLI keep alive indicator
        now = t.strftime('%H:%M:%S')
        currentMinute = t.strftime('%M')
        if (len(processThreads) == 0):
            sys.stdout.write("\r{} Current time is {}".format(next(spinner), now))
            sys.stdout.flush()

        # Checking to do stuff
        for timePair in times:
            if (currentMinute == timePair[0]):
                newThread = threading.Thread(target=timePair[1]())
                processThreads.append(newThread)
                newThread.start()

        # Just to slow down the CPU
        t.sleep(1)

# The `update` argument simply cals contentDetector.detectorDirector() and gathers any new content from the various sources
if (sys.argv[1] == "update"):
    detectorDirector()
    exit()
# The `new` argument calls videoEditor.GenerateVideo() and renders out a new long format video out of the clips stored in `data/sync_data`
if (sys.argv[1] == "new"):
    GenerateVideo()
    exit()
# `deploy` is used to deploy it to a server. This argument contains the scheduler and will run until the container is shut down
if (sys.argv[1] == "deploy"):
    mainThread = threading.Thread(target=main)
    mainThread.name = "Main Thread"
    mainThread.start()
    exit(mainThread.join())
else:
    print("Please use a valid command line argument")