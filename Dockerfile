FROM python:3

# This needs to be written but for now its just some random notes
# Again, this is not actually a dockerfile (yet)

# Apt dependencies
youtube-dl
ffmpeg

# Pip3 dependencies
scenedetect[opencv]
schedule
praw
moviepy

# MKV Tools installation
sudo add-apt-repository "deb https://mkvtoolnix.download/ubuntu/ xenial main"
sudo apt install apt-transport-https
wget -q -O - https://mkvtoolnix.download/gpg-pub-moritzbunkus.txt | sudo apt-key add -
sudo apt update
sudo apt install mkvtoolnix