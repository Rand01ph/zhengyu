#!/usr/bin/env python
# encoding: utf-8

from flask.ext.sqlalchemy import SQLAlchemy
from .. import app, wechat, redis

db = SQLAlchemy(app)

from .user import *

def set_user_info(openid):
    """保存用户信息"""
    redis_prefix = "wechat:user:"
    cache = redis.hexists(redis_prefix + openid, 'nickname')

    if not cache:
        user_info = User.query.filter_by(openid=openid).first()
        if not user_info:
            try:
                user_info = wechat.get_user_info(openid)
                if 'nickname' not in user_info:
                    raise KeyError(user_info)
            except Exception, e:
                app.logger.warning(u"获取微信用户信息 API 出错: %s" % e)
                user_info = None
            else:
                user = User(openid=user_info['openid'],
                            nickname=user_info['nickname'],
                            sex=user_info['sex'],
                            province=user_info['province'],
                            city=user_info['city'],
                            country=user_info['country'],
                            headimgurl=user_info['headimgurl'])
                user.save()
                # 与查询的数据类型一样，方便 redis 写入
                user_info = user

        if user_info:
            # 写入缓存
            redis.hmset(redis_prefix + user_info.openid, {
                "nickname": user_info.nickname,
                "realname": user_info.realname,
                "sex": user_info.sex,
                "province": user_info.province,
                "city": user_info.city,
                "country": user_info.country,
                "headimgurl": user_info.headimgurl,
                "regtime": user_info.regtime
            })
    else:
        return None


def is_user_exists(openid):
    """用户是否存在数据库"""
    redis_prefix = "wechat:user:"
    cache = redis.exists(redis_prefix + openid)
    if not cache:
        user_info = User.query.filter_by(openid=openid).first()
        if not user_info:
            return False
        else:
            return True
    else:
        return True
