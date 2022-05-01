from django.http import HttpResponse, Http404
from django.template import loader
from datetime import datetime
from webserver.messages import *

def index(request):
    template = loader.get_template('channel/index.html')
    return HttpResponse(template.render({'channels': sorted(get_channels())}, request))

def channel(request, channel):
    channel = channel.lower()
    template = loader.get_template('channel/channel.html')
    dbs = get_channels()
    if channel in dbs:
        username = request.GET.get('username', None)
        limit = int(request.GET.get('limit', DEFAULT_LIMIT))
        page = int(request.GET.get('page', 0))
        filter = {}
        if username:
            filter['username'] = username
        page_count = get_page_count(
            channel=channel,
            filter=filter,
            limit=limit
        )
        messages = get_channel_messages(
            channel=channel,
            filter=filter,
            limit=limit,
            page=page
        )
        context = {
            'username': username,
            'messages': messages,
            'channel': channel,
            'page': page,
            'limit': limit,
            'last_page': page_count-1
        }
        return HttpResponse(template.render(context, request))
    else:
        raise Http404("Channel not found in database") 
