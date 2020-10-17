import os
import sys
import schedule
import time as t
from datetime import datetime, time

from contentDetector import detectorDirector
from videoEditor import GenerateVideo
from videoUploader import newUpload
from tooling import prettyPrint, bcolors, fullPath

fileStructure = ["data/rawVideos",
                 "data/rawClips",
                 "data/sync_data",
                 "data/output"]
"""The programs file structure, used to verify that everything is exactly where it needs to be"""

for dir in fileStructure:
    formatDir = fullPath(dir)
    if not os.path.exists(formatDir):
        prettyPrint(bcolors.ENDC, os.popen('mkdir {}'.format(formatDir)).read())

# Checks to see if the data/rawClips directory is empty, if it is we need to fill it before anything can happen
if (len(os.listdir(fullPath("data/rawClips"))) == 0):
    detectorDirector()
"""Checks to see if the data/rawClips directory is empty, if it is we need to fill it before anything can happen"""

if (sys.argv[1] == "update"):
    """The `update` argument simply cals contentDetector.detectorDirector() and gathers any new content from the various sources"""
    detectorDirector()
    exit()
if (sys.argv[1] == "new"):
    """The `new` argument calls videoEditor.GenerateVideo() and renders out a new long format video out of the clips stored in `data/sync_data`"""
    GenerateVideo()
    exit()
if (sys.argv[1] == "deploy"):
    """`deploy` is used to deploy it to a server. This argument contains the scheduler and will run until the container is shut down"""
    schedule.every(20).minutes.do(detectorDirector)  
    """Every 20 minutes call `contentDetector.detectorDirector` to make sure we have every new piece of content avalible"""
    schedule.every().minute.at(":30").do(GenerateVideo)
    """Every 30 minutes generate a new video with `videoEditor.GenerateVideo()`. This gives me a 20 minutes, which should be more than enough, to render out a video and prepare it for upload"""
    # schedule.every().minute.at(":50").do(newUpload)
    """At the top of every hour `videoUploader/newUpload()` is called to upload the most recent video to YouTube. This is currently not working"""
    while True:
        schedule.run_pending()
        t.sleep(1)
    exit()
else:
    print("Please use a valid command line argument")