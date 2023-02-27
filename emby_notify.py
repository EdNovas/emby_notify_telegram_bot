import requests
import json
import sqlite3

EMBY_SERVER_URL = '<Your Emby Server URL>'
EMBY_API_KEY = '<Your Emby API key>'
EMBY_USER_ID = '<Your Emby Sample User used ID to get the updated videos>'
SERVER_ID = '<Your emby Server ID>'
TELEGRAM_BOT_TOKEN = '<Your Telegram Bot>'
TELEGRAM_CHAT_ID = '<Your Telegram Update Channel>'
CHANNEL = '<Your channel>'
GROUP = '<Your group>'


conn = sqlite3.connect("emby_notify.db")
conn_cursor = conn.cursor()

# Create the video table if it doesn't already exist
conn_cursor.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        img_tag TEXT
    )
""")

try:
    url = f'{EMBY_SERVER_URL}/emby/Users/{EMBY_USER_ID}/Items/Latest?Limit=2&api_key={EMBY_API_KEY}'
    responses = requests.get(url).json()
except:
    print("Wrong input url address")
    conn.close()

for response in responses:
    item_id = response['Id']
    item_type = response['Type']
    item_name = response['Name']
    item_link = f'{EMBY_SERVER_URL}/web/index.html#!/item?id={item_id}&serverId={SERVER_ID}'
    
    additional_url = f'{EMBY_SERVER_URL}/emby/Videos/{item_id}/AdditionalPartsItems&api_key={EMBY_API_KEY}'
    additional_responses = requests.get(url).json()
    print(additional_responses)
    try:
        item_img = response['ImageTags']['Primary']
        item_img_url = f'{EMBY_SERVER_URL}/emby/Items/{item_id}/Images/Primary?maxHeight=900&maxWidth=600&tag={item_img}&quality=90'
    except:
        continue
    conn_cursor.execute("SELECT COUNT(*) FROM videos WHERE id=?", (item_id,))
    count = conn_cursor.fetchone()[0]
    if (count == 0):
        conn_cursor.execute("INSERT INTO videos (id, name, type, img_tag) VALUES (?, ?, ?, ?)", (item_id, item_name, item_type, item_img))
        conn.commit()
        if item_type == 'Movie':
            item_type_str = '电影'
        elif item_type == 'Episode':
            item_type_str = '电视剧'
        else:
            item_type_str = 'Unknown'
        message = f'#上新\nTitle: {item_name} \n类型: {item_type_str}\n\n频道 {CHANNEL}\n群组 {GROUP}'
        url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
        button = {'text': '点击播放', 'callback_data': 'button_clicked', 'url': item_link}
        keyboard = [[button]]
        reply_markup = {'inline_keyboard': keyboard}
        params = {'chat_id': TELEGRAM_CHAT_ID, 'caption': message, 'photo': item_img_url,'reply_markup': json.dumps(reply_markup),}
        # print(message, item_img_url)
        requests.post(url, params=params)
conn.close()
