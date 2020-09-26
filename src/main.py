import os
from videoSpliter import cut_video

# This is mostly just for testing
sources = ["https://www.youtube.com/watch?v=cRguIOOiktg"]

# Checks to make sure the file structure exists, creates it if it doesnt
fileStructure = ["data",
                 "data/rawVideos",
                 "data/rawClips"]

for dir in fileStructure:
    if not os.path.exists(dir):
        os.mkdir(dir)

# Downloading all the YouTube Sources
# for vid in sources:
    # os.system("youtube-dl -o \"data/rawVideos/%(id)s.mp4\" -f mp4 {}".format(vid))

# Editing each of the videos
for targetVid in os.listdir("data/rawVideos"):
    cut_video(targetVid)