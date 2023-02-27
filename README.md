# emby_notify_telegram_bot
A simple telegram notify bot for Emby server

Use sqlite3 to store the item datas. Every 6 hours, the program will retrieve the last 200 items updated to the notify user library with valid primary images(if there's no valid primary image, it will be ignored). Check if the database have the newe items' ids and output the new itesm to the telegram channel.

## Use

Download

```
cd /opt && wget https://raw.githubusercontent.com/EdNovas/emby_notify_telegram_bot/main/emby_notify.py && chmod +x emby_notify.py
```

Fill in the config

Run in terminal

```
python3 emby_notify.py
```

## Config

```bash
EMBY_SERVER_URL = '<Your Emby Server URL>'
# It's your emby server address, it can be a ip or domain, need to have http:// or https:// at the front
# Example: 
# EMBY_SERVER_URL = 'https://emby.example.com'

EMBY_API_KEY = '<Your Emby API key>'
# This is your emby server api, you can get it from the API section in your emby server admin panel.

EMBY_USER_ID = '<Your Emby Sample User ID to get the updated videos>'
# Create a sample notify user, and get the user id from url.

SERVER_ID = '<Your emby Server ID>'
# Server id of your image

TELEGRAM_BOT_TOKEN = '<Your Telegram Bot>'
# Create the api from telegram bot father

TELEGRAM_CHAT_ID = '<Your Telegram Update Channel>'
# Get channel id from https://t.me/username_to_id_bot

CHANNEL = '<Your telegram channel>'
GROUP = '<Your telegram group>'
```

## Run with Systemd

Set the program to run every 6 hours

```bash
sudo vi /etc/systemd/system/emby-notify.timer
```

Input below text and save and exit.

```bash
[Unit]
Description=Run emby_notify.py every 6 hours

[Timer]
OnCalendar=*:0/6
Unit=emby-notify.service

[Install]
WantedBy=timers.target
```

Set systemctl for the main program

```bash
sudo nano /etc/systemd/system/emby-notify.service
```

Input below text and save and exit.

```bash
[Unit]
Description=Run emby_notify.py script

[Service]
Type=oneshot
ExecStart=python3 /opt/emby_notify.py
```

Run Systemctl

```bash
sudo systemctl daemon-reload
systemctl start emby_notifysudo systemctl start emby-notify.timer
sudo systemctl enable emby-notify.timer
```
