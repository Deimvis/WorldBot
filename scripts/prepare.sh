#!/bin/bash

sudo amazon-linux-extras install python3
sudo yum install -y tmux

ROOT_DIR="/home/ec2-user/world_bot"
mkdir -p ${ROOT_DIR}
chmod -R 777 ${ROOT_DIR}
