# Emby Notify Telegram Bot
一个简单的Emby剧集更新提醒telegraam机器人
A simple telegram notify bot for Emby server
使用 sqlite3 存储项目数据。 每 6 小时，程序将检索最后 200 个项目（您可以通过更改配置更改它）更新到具有有效主图像的通知用户库（如果没有有效的主图像，它将被忽略）。 检查数据库是否有新项目的 ID，并将新项目输出到电报频道。
Use sqlite3 to store the item datas. Every 6 hours, the program will retrieve the last 200 items(you can change it by change the config) updated to the notify user library with valid primary images(if there's no valid primary image, it will be ignored). Check if the database have the newe items' ids and output the new itesm to the telegram channel.

## Note
发布的频道消息都是中文的，如果你需要，你可以自己翻译并替换所有的汉字。
The published channel message is all written in Chinese, if you need, you can do the translation and replace all the Chinese characters by yourself.

## Use
下载
Download


```
cd /opt && wget https://raw.githubusercontent.com/EdNovas/emby_notify_telegram_bot/main/emby_notify.py && sudo chmod +x emby_notify.py
```
填写config文件配置
Fill in the config
测试运行
Run in terminal

```
python3 emby_notify.py
```

## Config
配置文件：
```bash
EMBY_SERVER_URL = '<Your Emby Server URL>'
# It's your emby server address, it can be a ip or domain, need to have http:// or https:// at the front
# Example: 
# EMBY_SERVER_URL = 'https://emby.example.com'

EMBY_API_KEY = '<Your Emby API key>'
# This is your emby server api, you can get it from the API section in your emby server admin panel.

EMBY_USER_ID = '<Your Emby Sample User ID to get the updated videos>'
# Create a sample notify user, and get the user id from url.

ITEMS_LIMIT = '<Input how many last items you want to get each time, default is 200>'

SERVER_ID = '<Your emby Server ID>'
# Server id of your playable video link(you can find it in any video play page url)

TELEGRAM_BOT_TOKEN = '<Your Telegram Bot>'
# Create the api from telegram bot father

TELEGRAM_CHAT_ID = '<Your Telegram Update Channel>'
# Get channel id from https://t.me/username_to_id_bot

CHANNEL = '<Your telegram channel>'
GROUP = '<Your telegram group>'
```

## Run with Systemd
设置每6小时运行一次
Set the program to run every 6 hours

```bash
sudo vi /etc/systemd/system/emby-notify.timer
```
用vi/vim/nano等任何你用的习惯的文字编辑器输入
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
sudo vi /etc/systemd/system/emby-notify.service
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
sudo systemctl start emby-notify.timer
sudo systemctl enable emby-notify.timer
```
