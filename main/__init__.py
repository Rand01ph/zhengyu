#!/usr/bin/env python
# encoding: utf-8

from flask import Flask

from flask_admin import Admin

import time
import logging
from logging.handlers import RotatingFileHandler

from redis import Redis
from wechat_sdk import WechatBasic
from .plugins.queue import make_celery
# Import the fixer
#from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__, instance_relative_config=True)
# 加载配置
app.config.from_object('config')
app.config.from_pyfile('config.py')

# Use the fixer
#app.wsgi_app = ProxyFix(app.wsgi_app)

# Flask-admin
# Flask and Flask-SQLAlchemy initialization here
admin = Admin(app, name='zhengyu-wechat', template_mode='bootstrap3')

# 队列
celery = make_celery(app)

# 记录日志
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.WARNING)
app.logger.addHandler(handler)

# 初始第三方库
redis = Redis()

# 初始化微信 SDK
wechat = WechatBasic(appid=app.config['APP_ID'],
                     appsecret=app.config['APP_SECRET'],
                     token=app.config['TOKEN'])

if not redis.exists("wechat:access_token"):
    # access_token 写入缓存
    wechat.grant_jsapi_ticket()
    redis.set("wechat:access_token",
              wechat.get_access_token()['access_token'], 7000)

#  # 初始化微信 SDK
#  if not redis.exists("wechat:access_token"):
    #  # 初始化微信实例
    #  wechat = WechatBasic(appid=app.config['APP_ID'],
                        #  appsecret=app.config['APP_SECRET'],
                        #  token=app.config['TOKEN'])
    #  d = wechat.grant_token()
    #  token = d['access_token']
    #  expired_at = d['access_token_expires_at']
    #  redis.set("wechat:access_token", token, (expired_at - time.time())*60)
    #  redis.set("wechat:access_token_expires_at", expired_at, (expired_at - time.time())*60)
#  else:
    #  wechat = WechatBasic(appid=app.config['APP_ID'],
                        #  appsecret=app.config['APP_SECRET'],
                        #  token=app.config['TOKEN'])

# 路由
from .routes import *
# 定时任务
from .plugins.cron import *
# 视图
from .views import dashboard
