#!/bin/bash

cd /home/ec2-user/world_bot

sudo yum install -y docker
sudo service docker start

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

docker rmi bot
docker build -t bot .
docker run \
  --env-file /home/ec2-user/secrets/.env \
  -v /home/ec2-user/database:/bot/database \
  bot
