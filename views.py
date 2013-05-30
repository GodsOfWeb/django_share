from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django_share.models import AppData
from rauth.service import OAuth2Service
import os
import binascii
import requests
import urllib
import urllib2
import json
import urlparse
import tweepy

APP_ID = ""
APP_SECRET = ""

def facebook_connect(request):
    args = {
        'client_id': APP_ID,
        'redirect_uri': "dev.artirion.com/fb_answer",
        'scope':'publish_stream,manage_pages',
    }
    url = 'https://graph.facebook.com/oauth/authorize?%s' % urllib.urlencode(args)
    return HttpResponseRedirect(url)

def fb_answer(request):
    args = {
        'client_id': APP_ID,
        'redirect_uri': "http://dev.artirion.com/fb_answer",
        'client_secret': APP_SECRET,
        'code': request.GET['code'],
    }
    url = 'https://graph.facebook.com/oauth/access_token?%s' % urllib.urlencode(args)
    response = urllib2.urlopen(url)
    with open('prova.json', 'w') as infile:
        json.dump({"facebook":urlparse.parse_qs(response.read())}, infile)
    return HttpResponse("OK")

def post_fb(request):
    with open('prova.json', 'r') as infile:
        data = json.load(infile)

    data = data["facebook"]
    post_data = {'access_token': data["access_token"], 'message':'hey this is a test!'}
    post_data = urllib.urlencode(post_data)
    print post_data
    response = urllib2.Request('https://graph.facebook.com/1492753571/feed', post_data)
    response = urllib2.urlopen(response)
    return HttpResponse(response)

def linkedin(request):
    try:
        app = AppData.objects.filter(nome="Linkedin")[0]
    except:
        return HttpResponse("Devi prima impostare i dettagli della tua Applicazione")

    Objlinkedin = OAuth2Service(
        client_id = app.app_id,
        client_secret= app.app_secret,
        name='linkedin',
        authorize_url='https://www.linkedin.com/uas/oauth2/authorization',
        access_token_url='https://www.linkedin.com/uas/oauth2/accessToken',
        base_url='http://www.linkedin.com/v1/'
    )

    try:
        data = {
            'code': request.GET["code"],
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://dev.artirion.com/linkedin'
        }

        session = Objlinkedin.get_raw_access_token(data=data)
        response = session.json()
        return HttpResponse("Copia l'access token: <input value='%s'>" % response["access_token"])

    except:
        params = {
            'scope': 'r_network rw_nus',
            'state': binascii.b2a_hex(os.urandom(15)),
            'response_type': 'code',
            'redirect_uri': 'http://dev.artirion.com/linkedin',
        }
        authorize_url = Objlinkedin.get_authorize_url(**params)
        return HttpResponseRedirect(authorize_url)
