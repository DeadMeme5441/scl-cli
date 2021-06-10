#!/usr/bin/env bash
#--------------------------------------------#
# This block installs docker.                #
#--------------------------------------------#
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
sudo pip3 install grequests asyncio
#--------------------------------------------#

#--------------------------------------------#
# This block runs the container.             #
#--------------------------------------------#
docker build . -t deadunderscorememe/scl-cli
docker run -e PYTHONUNBUFFERED=1 --name scl -d -p 8080:3000 deadunderscorememe/scl-cli:latest
#--------------------------------------------#
# Run the Python script to access the API.   #
#--------------------------------------------#
