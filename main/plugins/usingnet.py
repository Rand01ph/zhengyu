#!/usr/bin/env python
# encoding: utf-8

import requests
import random
from .. import app, celery
from . import wechat_custom

default_answer = [u'么么哒', u'说啥呢……', u'叫我干嘛', u'纳尼……', u'=。=']

@celery.task
def chat(openid, text):
    usingnet_post_url = app.config['USINGNET_MESSAGE_URL'] + app.config['APP_ID']
    try:
        r = requests.post(usingnet_post_url, data=text)
        print 322332
    except Exception, e:
        app.logger.warning(u"usingnet 请求或解析失败: %s, text: %s" % (e, text))
        return wechat_custom.send_text(openid, random.choice(default_answer))
