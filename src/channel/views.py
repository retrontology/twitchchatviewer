from django.http import HttpResponse, Http404
from django.template.context import make_context
from django.template import loader, Template
from datetime import datetime
from webserver.messages import *
from webserver.channels import *

def index(request):
    template = loader.get_template('channel/index.html')
    limit = int(request.GET.get('limit', DEFAULT_LIMIT))
    page = int(request.GET.get('page', 0))
    page_count = get_channels_page_count(limit=limit)
    channels = get_channels(limit=limit, page=page)
    return HttpResponse(
        template.render
        (
            {
                'channels': channels,
                'page': page,
                'limit': limit,
                'last_page': page_count-1
            },
            request
        )
    )

def channel(request, channel):
    channel = channel.lower()
    template = loader.get_template('channel/channel.html')
    dbs = [x['channel'] for x in get_channels()]
    if channel in dbs:
        username = request.GET.get('username', None)
        limit = int(request.GET.get('limit', DEFAULT_LIMIT))
        page = int(request.GET.get('page', 0))
        filter = {}
        if username:
            filter['username'] = username
        page_count = get_channel_page_count(channel, limit)
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
        template = loader.get_template('channel/notfound.html')
        return HttpResponse(template.render({'channel': channel}, request), status=404)
