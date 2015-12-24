#!/usr/bin/env python
# encoding: utf-8

from main import wechat, app
import datetime
import requests
import json
from .plugins.state import *

def wechat_response(data):
    """微信消息处理回复"""
    global message, openid

    wechat.parse_data(data)
    message = wechat.get_message()
    openid = message.source

    response = 'success'
    if message.type == 'text':
        # 替换全角空格为半角空格
        message.content = message.content.replace(u'　', ' ')
        # 清除行首空格
        message.content = message.content.lstrip()

        working_time = datetime.time(23,30,0)
        message_time = datetime.datetime.fromtimestamp(message.time).time()

        if message_time > working_time:
            response = wechat.response_text('已经下班啦')
        elif message.content == u'更新菜单':
            response = update_menu_setting()
        elif message.content == u'获取分组':
            response = get_user_group()
        elif message.content == u'获取二维码':
            response = get_qcode()
        else:
            usingnet_post_url = app.config['USINGNET_MESSAGE_URL'] + app.config['APP_ID']
            r = requests.post(usingnet_post_url, data=message.raw)
            print message.raw
            print r.status_code
            response = wechat.response_text('请稍后，正在为你转接客服')

    elif message.type == 'click':
        if message.key == 'phone_number':
            response = phone_number()
        elif message.key == 'score':
            response = wechat.response_text('成绩功能测试中')

    elif message.type == 'subscribe':
        print message.key
        if message.key != None:
            groups_will_id = message.key.split('_')[1]
        wechat.move_user(openid, int(groups_will_id))
        response = subscribe()

    elif message.type == 'scan':
        print message.key
    else:
        pass

    # 保存最后一次交互的时间
    print openid
    set_user_last_interact_time(openid, message.time)

    return response


def update_menu_setting():
    """更新自定义菜单"""
    try:
        wechat.create_menu(app.config['MENU_SETTING'])
    except Exception, e:
        return wechat.response_text(e)
    else:
        return wechat.response_text('Done!')

def get_user_group():
    """获取用户分组数据"""
    groups_data = wechat.get_groups()
    groups_name = ""
    for i in groups_data['groups']:
        groups_name += i['name']
        groups_name += '\n'
    return wechat.response_text(groups_name)

def get_qcode():
    """根据分组换取二维码"""
    # {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": "123"}}}
    qr_dict = {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": "default_value"}}}
    groups_data = wechat.get_groups()
    for i in groups_data['groups']:
        qr_dict['action_info']['scene']['scene_str'] = i['id']
        print wechat.create_qrcode(qr_dict)['ticket']
    return wechat.response_text(u'qrcode')

def subscribe():
    """回复订阅事件"""
    content = app.config['WELCOME_TEXT']
    return wechat.response_text(content)

def phone_number():
    """回复电话号码"""
    content = app.config['PHONE_NUMBER_TEXT']
    return wechat.response_text(content)
