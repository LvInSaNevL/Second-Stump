# Second-Stump
An experimental bot to automate meme compilations


### Startup Guide
1. Copy data from [data/authExample.json](data/authExample.json) into a file called `data/auth.json`, and replace the placeholder information with your own. 
2. If you are running this from the command line you can run the command `src/main.py` and pass in one of the command line arguments, which are listed below.
    * `update`: Runs through the sources list and downloads any new content
    * `new`: Edits any longer compilation videos that may exist and generate a new finished video
    * `deploy`: Runs the code as if it would be deployed on a server. This argument will run the program until it is stopped by you. 
3. If you are deploying this to a Docker container, just simply run the command `sudo ./dockerStart.sh` and it will take care of everything
    * You will get an error `debconf: delaying package configuration, since apt-utils is not installed` during build. This seems to be harmeless but I'm not 100% how to fix it. 
    * If you are unable to run the script, run `chmod +x` and try again
    * `docker build` takes a real long time, only recommended if you are actually going to deploy

### Description of file structure
All file paths are from the root directory of this project.
* [assets](assets): Contain images and files related to the Second Stump YouTube channel and not directly related to the code base
* [data](data): Contains the working directory for the software backend
    * [data/rawVideos](data/rawVideos): This is where compilation videos are downloaded in preparation for ingest
    * [data/rawClips](data/rawClips): Contains the raw output of the inital cutting
* [src](src): Where the actual code base of Second Stump lives.
* [tools](tools): Various tools that I wrote during development of the project. Please visit the [README](tools/README.md) bundled in the directory for a detailed explination of each script