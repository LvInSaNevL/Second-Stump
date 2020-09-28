# Second-Stump
An experimental bot to automate meme compilations


### Startup Guide
1. Copy data from [data/authExample.json](data/authExample.json) into a file called `data/auth.json`, and replace the placeholder information with your own. 
2. If you are running this from the command line you can run the command `src/main.py` and pass in one of the command line arguments, which are listed below.
    * `update`: Runs through the sources list and downloads any new content
    * `new`: Edits any longer compilation videos that may exist and generate a new finished video
    * `deploy`: Runs the code as if it would be deployed on a server. This argument will run the program until it is stopped by you. 
3. If you are deploying this to a Docker container, just simply run these few commands. If you want more detailed information about these commands please check the [Docker Documentation](https://docs.docker.com/get-started/part2/)
    * `docker build --tag SecondStump:1.0 .`
    * `docker run --publish 8080:8080 --detatch SecondStump SecondStump:1.0`

### Description of file structure
All file paths are from the root directory of this project.
* [assets](assets): Contain images and files related to the Second Stump YouTube channel and not directly related to the code base
* [data](data): Contains the working directory for the software backend
    * [data/rawVideos](data/rawVideos): This is where compilation videos are downloaded in preparation for ingest
    * [data/rawClips](data/rawClips): Contains the raw output of the inital cutting
* [src](src): Where the actual code base of Second Stump lives.
* [tools](tools): Various tools that I wrote during development of the project. Please visit the [README](tools/README.md) bundled in the directory for a detailed explination of each script