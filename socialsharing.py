# -*- coding: utf-8 -*-
from django_share.models import AppData, SocialAccount
import requests
import json
import tweepy

def twitter_post(message, link):
    if len(message) > 140:
        return "Il messaggio è troppo lungo"
    try:
        app = AppData.objects.filter(nome="Twitter")[0] 
    except:
        return "Devi prima impostare i dettagli della tua applicazione"

    result = []
    for account in app.account.all():
        if account.social == "Twitter":
            auth = tweepy.OAuthHandler(app.app_id, app.app_secret)
            auth.set_access_token(account.access_token, account.access_token_secret)
            api = tweepy.API(auth)
            try:
                result.append(api.update_status("%s %s" %(message, link)))
            except Exception, e:
                result.append(e)
    return result

def linkedin_post(message, link):
    try:
        app = AppData.objects.filter(nome="Linkedin")[0]
    except:
        return "Devi prima impostare i dettagli della tua applicazione"
 
    data_json = {
        "comment": "Condividiamo!",
        "content": {
            "title": message,
            "submitted-url": link,
            "submitted-image-url": "http://lnkd.in/Vjc5ec"
         },
         "visibility": {
            "code": "anyone"
         }
    }

    url = 'https://api.linkedin.com/v1/people/~/shares'
    headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
    result = []
    for account in app.account.all():
        params = {'oauth2_access_token': account.access_token }
        result.append(requests.request("POST", url, data=json.dumps(data_json), params=params, headers=headers, timeout=60))

    return result

def share(message, link):
    result = {}
    twitter = twitter_post(message, link)
    linkedin = linkedin_post(message, link)
    result["twitter]"] = twitter
    result["linkedin"] = linkedin

    return result
