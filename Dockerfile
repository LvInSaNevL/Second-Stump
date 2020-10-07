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

# Install apt-get dependencies
RUN apt-get clean && apt-get update
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
            tzdata
RUN apt-get clean && apt-get update

# Install MKVToolNix
RUN wget -q -O - https://mkvtoolnix.download/gpg-pub-moritzbunkus.txt | apt-key add - && \
    echo "deb https://mkvtoolnix.download/ubuntu/ focal main" >> /etc/apt/sources.list.d/mkvtoolnix.download.list && \
    echo "deb-src https://mkvtoolnix.download/ubuntu/ focal main" >> /etc/apt/sources.list.d/mkvtoolnix.download.list && \
    apt-get update && \
    apt-get install -y mkvtoolnix

# Install Pip3 dependencies
RUN pip3 install --force-reinstall \
         scenedetect[opencv] \
         schedule \
         praw \
         google-api-python-client \
         google-auth-oauthlib \
         google-auth-httplib2 

# Just makes sure everything is up to date and good to go
RUN apt-get update && apt-get autoremove && apt-get upgrade

# Coping the source files
COPY . /secondStump

# Setting up Docker
EXPOSE 7800
ENTRYPOINT [ "python3", "/secondStump/src/main.py", "deploy" ]