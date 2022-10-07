from webserver.db import *
from math import ceil

DEFAULT_FIELDS = [
    'channel',
    'message_count'
]
    
def get_channels(filter={}, sort=DEFAULT_SORT, fields=DEFAULT_FIELDS, limit=DEFAULT_LIMIT, page=0):
    project = get_project(fields)
    sort = list({'channel': 1}.items())
    return [x for x in get_db()[CHANNEL_COLLECTION].find(
        filter=filter,
        projection=project,
        sort=sort,
        skip=page*limit,
        limit=limit
    )]

def get_channels_page_count(filter={},limit=DEFAULT_LIMIT):
    container = get_db()[CHANNEL_COLLECTION]
    total = container.count_documents(filter=filter)
    return ceil(total / limit)