import requests
import time
import json

EMBY_SERVER_URL = '<Your Emby Server URL>'
EMBY_API_KEY = '<Your Emby API key>'
EMBY_USER_ID = '<Your Emby Sample User used ID to get the updated videos>'
SERVER_ID = '<Your emby Server ID>'
TELEGRAM_BOT_TOKEN = '<Your Telegram Bot>'
TELEGRAM_CHAT_ID = '<Your Telegram Update Channel>'
CHANNEL = '<Your channel>'
GROUP = '<Your group>'
VIDEO_NAME = ''

def send_telegram_notification(message, photo_url, video_link):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    button = {'text': '点击播放', 'callback_data': 'button_clicked', 'url': video_link}
    keyboard = [[button]]
    reply_markup = {'inline_keyboard': keyboard}
    params = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message, 'photo': photo_url,'reply_markup': json.dumps(reply_markup),}
    requests.post(url, params=params)

def get_latest_video(user_id):
    global VIDEO_NAME
    url = f'{EMBY_SERVER_URL}/emby/Users/{user_id}/Items/Latest?api_key={EMBY_API_KEY}'
    response = requests.get(url).json()
    item_id = response[0]['Id']
    video_name = response[0]['Name']
    video_type = response[0]['Type']
    # print(item_id)
    # print(video_name)
    print(response[0])
    try:
        imageTag = response[0]['ImageTags']['Primary']
        # print(imageTag)
        image_url = f'{EMBY_SERVER_URL}/emby/Items/{item_id}/Images/Primary?maxHeight=900&maxWidth=600&tag={imageTag}&quality=90'
        # print(image_url)
    except:
        image_url = 'empty'
    # print(image_url)
    video_link = f'{EMBY_SERVER_URL}/web/index.html#!/item?id={item_id}&serverId={SERVER_ID}'
    # print(video_link)
    return video_name,video_type, image_url, video_link

def check_for_video_updates():
    global VIDEO_NAME
    video_name,video_type, image_url, video_link = get_latest_video(EMBY_USER_ID)
    # print(VIDEO_NAME)
    if video_type == 'Movie':
        video_type_str = '电影'
    elif video_type == 'Episode':
        video_type_str = '电视剧'
    else:
        video_type_str = 'Unknown'
    if (image_url != 'empty'):
        if (video_name != VIDEO_NAME):
            VIDEO_NAME = video_name
            message = f'#上新\nTitle: {video_name} \n类型: {video_type_str}\n\n频道 {CHANNEL}\n群组 {GROUP}'
            print(message)
            send_telegram_notification(message, image_url, video_link)
            
while True:
    check_for_video_updates()
    time.sleep(2)
