FROM ubuntu:20.04

# Just some metadata for the program
# This is mostly just for humans like you :)
ARG BUILD_DATE
LABEL vendor="Cadosphere Interactive"
LABEL maintainer="Matthew Wollam<lvinsanevl.info@gmail.com>"
LABEL name="Second Stump"
LABEL description = "An experimental bot to automate collecting short memes and combining them into compilations"
LABEL usage="README.md"
LABEL org.label-schema.build-date=$BUILD_DATE

# Time zone info, stops TZData from hanging
ENV TZ=America/Indiana/Indianapolis
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Fixing an error that apt throws
# https://github.com/phusion/baseimage-docker/issues/58
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install apt-get dependencies
RUN apt-get clean -y && apt-get update -y
RUN apt-get install -y \
            --no-install-recommends apt-utils \
            ca-certificates \
            build-essential \
            wget \
            gnupg2 \
            curl \
            python3-pip \
            youtube-dl \
            ffmpeg \
            libdvdread7 \
            tzdata \
            apt-transport-https \
            python3.8 \
            nano
RUN apt-get clean -y && apt-get update -y

# Install MKVToolNix
RUN wget --no-check-certificate -q -O - https://mkvtoolnix.download/gpg-pub-moritzbunkus.txt | apt-key add - && \
    echo "deb https://mkvtoolnix.download/ubuntu/ focal main" >> /etc/apt/sources.list.d/mkvtoolnix.download.list && \
    echo "deb-src https://mkvtoolnix.download/ubuntu/ focal main" >> /etc/apt/sources.list.d/mkvtoolnix.download.list && \
    apt-get update && \
    apt-get install -y mkvtoolnix

# Install Pip3 dependencies
RUN pip3 install --force-reinstall \
         scenedetect[opencv] \
         schedule \
         praw \
         filelock \
         selenium \
         webdriver-manager \
         names

# Just makes sure everything is up to date and good to go
RUN apt-get update -y
RUN apt-get autoremove -y
RUN apt-get upgrade -y

# Build the file structure
RUN mkdir /secondStump \
          /secondStump/data

# Coping the source files
COPY . /secondStump
COPY data /secondStump/src/data

# Setting up Docker
EXPOSE 7800
ENTRYPOINT [ "python3", "/secondStump/src/main.py", "deploy" ]