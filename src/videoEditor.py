import os, sys
import time
import random
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.fx.audio_normalize import audio_normalize
from utils import prettyPrint, bcolors

def moviepyOutput(paths):
    clipData = []
    for path in paths:
        clipData.append(audio_normalize(VideoFileClip(path)))
    finalVideo = concatenate_videoclips(clipData, method='compose')
    finalVideo.write_videofile("data/output.mp4", fps=30)

def customOutput(paths):
    # Creates a list of the input files for FFMPEG
    with open("inputPaths.txt", "a") as inputPathFile:
        ouputString = ""
        for inputPath in paths: 
            ouputString += "file 'data/sync_{}' \n".format(inputPath)
        inputPathFile.write(ouputString)

    # Padding and syncing the audio streams
    for inVid in paths:
        prettyPrint(bcolors.ENDC, os.popen("ffmpeg -i {} -vf 'split[original][copy];[copy]scale=ih*16/9:-1,crop=h=iw*9/16,gblur=sigma=20[blurred];[blurred][original]overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2' -video_track_timescale 29971 -ac 1 data/sync_{}".format(inVid, inVid)).read())
    prettyPrint(bcolors.ENDC, os.popen("ffmpeg -f concat -safe 0 -i {} -c copy data/output.mp4".format("inputPaths.txt")).read())
    os.remove("inputPaths.txt")

def GenerateVideo():
    # Gets minimum length of video (between 11 and 16 minutes)
    videoLength = random.randint(120, 300)
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
    prettyPrint(bcolors.OKBLUE, "Actual video length is {} and contains {} videos. All file paths are listed below".format(datetime.timedelta(seconds=int(totalLength)), len(clipPaths)))
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

    #moviepyOutput(clipPaths)
    customOutput(clipPaths)

    # A little alert to let the user know the function is over and how long it took
    endTime = time.perf_counter()
    prettyPrint(bcolors.OKGREEN, f"Collected clips and edited video. Process took {endTime - startTime:0.4f} seconds")


# A little bit of structure. Allows me to call `videoEditor.py GenerateVideo` from the command line
# if __name__ == '__main__':
#    globals()[sys.argv[1]]()
GenerateVideo()