#!/bin/bash

cd /home/ec2-user/world_bot

container_id=$(docker ps -a -q --filter ancestor=bot)
docker stop $container_id
docker rm -f $container_id
docker rmi -f bot
docker build -t bot .
docker run \
  --env-file /home/ec2-user/secrets/.env \
  -v /home/ec2-user/database:/bot/database \
  bot
