#!/usr/bin/env python
# encoding: utf-8

import requests
import random
from .. import app, celery
from . import wechat_custom

default_answer = [u'么么哒', u'说啥呢……', u'纳尼……', u'=。=']


@celery.task
def chat(openid, text):
    usingnet_post_url = app.config['USINGNET_MESSAGE_URL'] + app.config['APP_ID']
    try:
        print text
        r = requests.post(usingnet_post_url, data=text)
        print r.status_code
    except Exception, e:
        app.logger.warning(u"usingnet customer请求或解析失败: %s, text: %s" % (e, text))
        return wechat_custom.send_text(openid, random.choice(default_answer))

    if online(openid):
        pass
    else:
        return wechat_custom.send_text(openid, app.config['CUSTOMER_OUTLINE_STATE_TEXT'])


def online(openid):
    usingnet_online_url = app.config['USINGNET_ONLINE_URL'] + app.config['USINGNET_TEAM_TOKEN']
    try:
        r = requests.get(usingnet_online_url)
        online_data = r.json()['data']
    except Exception, e:
        app.logger.warning(u"usingnet online api请求或解析失败: %s: %s" % e)
        return wechat_custom.send_text(openid, random.choice(default_answer))

    if online_data:
        return True
    else:
        return False
