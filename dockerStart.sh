#!/bin/bash

echo -e "\033[94mRemoving any existing Second Stump containers\033[0m"
docker rm second_stump
echo -e "\033[94mBuilding Docker Image\033[0m"
docker build --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') --tag secondstump:0.6 .
echo -e "\033[94mRunning Docker Image\033[0m"
docker run -p 7800:80 -it --name second_stump -v data:/secondStump/data secondstump:0.6