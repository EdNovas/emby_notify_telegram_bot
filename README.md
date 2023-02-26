# emby_notify_telegram_bot
A simple telegram notify bot for Emby server

Use sqlite3 to store the item datas. Every 6 hours, the program will retrieve the last 200 items updated to the notify user library with valid primary images(if there's no valid primary image, it will be ignored). Check if the database have the newe items' ids and output the new itesm to the telegram channel.

## Run with Systemd

Set the program to run every 6 hours

```
sudo vi /etc/systemd/system/emby-notify.timer
```

Input below text and save and exit.

```
[Unit]
Description=Run emby_notify.py every 6 hours

[Timer]
OnCalendar=*:0/6
Unit=emby-notify.service

[Install]
WantedBy=timers.target
```

Set systemctl for the main program

```
sudo nano /etc/systemd/system/emby-notify.service
```

Input below text and save and exit.

```
[Unit]
Description=Run emby_notify.py script

[Service]
Type=oneshot
ExecStart=python3 /opt/emby_notify.py
```

```
sudo systemctl daemon-reload
systemctl start emby_notifysudo systemctl start emby-notify.timer
sudo systemctl enable emby-notify.timer
```
