import os, sys
import time
import random
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.fx.audio_normalize import audio_normalize
from utils import prettyPrint, bcolors

def GenerateVideo():
    # Gets minimum length of video (between 11 and 16 minutes)
    videoLength = random.randint(240, 300)
    prettyPrint(bcolors.OKBLUE, "Expected video length is {}".format(datetime.timedelta(seconds=videoLength)))

    # A list of which clips to use and how long the video is currently
    clipPaths = []
    totalLength = 0

    # Randomly selecting clips to add until the video is long enough
    while (totalLength < videoLength):
        newChoice = "data/rawClips/{}".format(random.choice(os.listdir("data/rawClips")))

        if newChoice not in clipPaths:
            try:
                totalLength += float(os.popen("ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}".format(newChoice)).read())
                clipPaths.append(newChoice)
            except Exception as e:
                prettyPrint(bcolors.WARNING, "Exception thrown, continuing with process. Exception: {}".format(e))
            
    
    # Just some output for the user
    prettyPrint(bcolors.OKBLUE, "Actual video length is {} and contains {} videos. All file paths are listed below".format(datetime.timedelta(seconds=videoLength), len(clipPaths)))
    # Logs the video files for future reference
    logString = ""
    spacing = len(str(datetime.datetime.now())) + 4
    for path in clipPaths:
        for x in range(4):
            logString += "{} || ".format(path)
        logString += "\n"
        for x in range(spacing):
            logString += " "
    prettyPrint(bcolors.ENDC ,logString)

    # Edits the video together
    startTime = time.perf_counter()
    clipData = []
    for path in clipPaths:
        clipData.append(audio_normalize(VideoFileClip(path)))
    finalVideo = concatenate_videoclips(clipData, method='compose')
    finalVideo.write_videofile("data/output.mp4", fps=30)

    # A little alert to let the user know the function is over and how long it took
    endTime = time.perf_counter()
    prettyPrint(bcolors.OKGREEN, f"Collected clips and edited video. Process took {endTime - startTime:0.4f} seconds")


# A little bit of structure. Allows me to call `videoEditor.py GenerateVideo` from the command line
if __name__ == '__main__':
    globals()[sys.argv[1]]()
