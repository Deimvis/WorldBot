#!/bin/bash

cd /home/ec2-user/world_bot

export DB_PATH="/home/ec2-user/database/db.db"
export BOT_TOKEN=$(cat /home/ec2-user/.token/bot_token)

pip3 install -r requirements.txt

tmux new-session -d -s world_bot
sleep 5
tmux send-keys -t world_bot 'cd /home/ec2-user/world_bot' C-m
tmux send-keys -t world_bot 'python3 main.py' C-m
echo "World bot started"
