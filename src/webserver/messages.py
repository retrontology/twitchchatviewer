from webserver.db import *
from math import ceil

DEFAULT_FIELDS = [
    'channel',
    'username',
    'timestamp',
    'content',
    'color',
    'emotes',
    'emotes_ffz',
    'emotes_bttv',
    'emotes_seventv'
]
DEFAULT_SORT = list({'timestamp': -1}.items())
    
def get_channel_messages(channel:str, filter={}, sort=DEFAULT_SORT, fields=DEFAULT_FIELDS, limit=DEFAULT_LIMIT, page=0):
    container = get_db()[MESSAGE_COLLECTION]
    project=get_project(fields)
    filter['channel'] = channel.lower()
    cursor = container.find(
        filter=filter,
        projection=project,
        sort=sort,
        skip=page*limit,
        limit=limit
    ).limit(limit)
    return parse_messages(cursor)

def get_channel_page_count(channel:str, limit=DEFAULT_LIMIT):
    channel = channel.lower()
    container = get_db()[CHANNEL_COLLECTION]
    result = container.find_one(
        filter={
            'channel': channel
        }, 
        projection={
            'message_count': 1, 
            '_id': 0
        }
    )
    if result:
        result = result['message_count']
    else:
        result = 0
    return ceil(result/limit)

def get_page_count(channel=None, username=None, filter={}, limit=DEFAULT_LIMIT):
    container = get_db()[MESSAGE_COLLECTION]
    if channel: filter['channel'] = channel
    if username: filter['username'] = username
    total = container.count_documents(filter=filter)
    return ceil(total / limit)

def get_user_color(username):
    username = username.lower()
    collection = get_db()[MESSAGE_COLLECTION]
    filter={
        'username': username
    }
    project={
        '_id': 0, 
        'color': 1
    }
    limit=1
    count = collection.count_documents(
        filter=filter,
        limit=limit
    )
    if count != 1:
        return None
    color = next(collection.find(
        filter=filter,
        projection=project,
        limit=limit
    ).limit(limit))['color']
    return color

def get_user_messages(username, channels=None, filter={}, sort=DEFAULT_SORT, fields=DEFAULT_FIELDS, limit=DEFAULT_LIMIT, page=0):
    container = get_db()[MESSAGE_COLLECTION]
    project=get_project(fields)
    filter['username'] = username
    cursor = container.find(
        filter=filter,
        projection=project,
        sort=sort,
        skip=page*limit,
        limit=limit
    ).limit(limit)
    return parse_messages(cursor)

def parse_messages(cursor):
    messages = []
    channels = {}
    for message in cursor:
        if message['channel'] not in channels:
            channels[message['channel']] = get_channel_id(message['channel'])
        message['channel_id'] = channels[message['channel']]
        message = parse_timestamp(message)
        messages.append(message)
    return messages

def get_channel_id(channel):
    channel = channel.lower()
    filter = {'channel': channel}
    return get_db()[CHANNEL_COLLECTION].find_one()['twitch_id']

def parse_timestamp(message):
    message['timestamp'] = message['timestamp'].strftime(TIMESTAMP_FORMAT)
    return message

def parse_usernames(message):
    words = message['content'].split()
    for word in words:
        if word[0] == '@' and len(word) > 1:
            target_user = word[1:]
            channel = message['channel']
            color = get_user_color(target_user)
            if color:
                color = f' color: {color};'
            else:
                color = ''
            replacement = f'<a style="text-decoration: none;{color}" href="/channel/{channel}?username={target_user}">{word}</a>'
            message['content'] = message['content'].replace(word, replacement, 1)
    return message