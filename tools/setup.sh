#!/bin/bash

# Define password for the database
export DB_PASSWORD=halitenewpassword

# Install python package manager
sudo apt-get update && apt-get install -y \
    python3 \
    python3-pip

sudo pip3 install -r requirements.txt


# make tmp directory for images
mkdir bots

# install halite binary
wget https://github.com/MetalBlueberry/Halite-competition/releases/download/v0.1.0/halite
chmod +x halite
sudo mv halite /usr/local/bin/

# Install docker
sudo apt-get install docker.io
sudo usermod -aG  docker ubuntu

# Copy AWS s3 credentials
echo "DONT FORGET TO COPY AWS CREDENTIALS"
