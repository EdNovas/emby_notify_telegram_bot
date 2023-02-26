# emby_notify_telegram_bot
A simple telegram notify bot for Emby server

## Run with Systemd

```
sudo vi /etc/systemd/system/emby_notify.service
```

Input below text and save and exit.

```
[Unit]
Description=Emby notification bot

[Service]
Type=simple
User=<your Linux username>
ExecStart=/usr/bin/python3 /opt/emby_notify.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```
systemctl start emby_notify
systemctl enable emby_notify
```
