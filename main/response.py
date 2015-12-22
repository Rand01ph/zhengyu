#!/usr/bin/env python
# encoding: utf-8

import re
from main import wechat, app

def wechat_response(data):
    """微信消息处理回复"""
    global message, openid

    wechat.parse_data(data)
    message = wechat.get_message()

    response = 'success'
    if message.type == 'text':
        # 替换全角空格为半角空格
        message.content = message.content.replace(u'　', ' ')
        # 清除行首空格
        message.content = message.content.lstrip()

        if message.content == u'电话':
            response = phone_number()
        elif re.match(u'^留言|^客服', message.content):
            response = leave_a_message()
        elif message.content == u'更新菜单':
            response = update_menu_setting()
        else:
            response = command_not_found()
    elif message.type == 'click':
        if message.key == 'phone_number':
            response = phone_number()
        elif message.key == 'score':
            response = wechat.response_text('成绩功能测试中')
    elif message.type == 'subscribe':
        response = subscribe()
    else:
        pass

    return response


def update_menu_setting():
    """更新自定义菜单"""
    try:
        wechat.create_menu(app.config['MENU_SETTING'])
    except Exception, e:
        return wechat.response_text(e)
    else:
        return wechat.response_text('Done!')

def subscribe():
    """回复订阅事件"""
    content = app.config['WELCOME_TEXT']
    return wechat.response_text(content)

def phone_number():
    """回复电话号码"""
    content = app.config['PHONE_NUMBER_TEXT']
    return wechat.response_text(content)
