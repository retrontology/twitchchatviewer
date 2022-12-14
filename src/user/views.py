from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from datetime import datetime
from webserver.messages import *

# Create your views here.
def index(request):
    username = request.GET.get('username', None)
    if username:
        return(HttpResponseRedirect(f'/user/{username}'))
    else:
        template = loader.get_template('user/index.html')
        return HttpResponse(template.render({}, request))

def user(request, username):
    username = username.lower()
    limit = int(request.GET.get('limit', DEFAULT_LIMIT))
    page = int(request.GET.get('page', 0))
    page_count = get_page_count(
        username=username,
        limit=limit
    )
    if page_count == 0:
        template = loader.get_template('user/notfound.html')
        return HttpResponse(template.render({'username': username}, request), status=404)
    else:
        template = loader.get_template('user/user.html')
        messages = get_user_messages(
            username=username,
            limit=limit,
            page=page
        )
        context = {
            'username': username,
            'messages': messages,
            'page': page,
            'limit': limit,
            'last_page': page_count-1
        }
        return HttpResponse(template.render(context, request))