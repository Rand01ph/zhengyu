#!/usr/bin/env python
# encoding: utf-8

import re
from main import wechat, app
import datetime
import requests
import json
from .plugins.state import *
from .plugins import usingnet

def wechat_response(data):
    """微信消息处理回复"""
    global message, openid

    wechat.parse_data(data)
    message = wechat.get_message()
    openid = message.source

    response = 'success'

    print message.raw

    if message.type == 'text':
        # 替换全角空格为半角空格
        message.content = message.content.replace(u'　', ' ')
        # 清除行首空格
        message.content = message.content.lstrip()

        commands = {
            u'取消': cancel_command,
            u'更新菜单': update_menu_setting,
            u'获取分组': get_user_group,
            u'获取二维码': get_qcode,
            u'客服': enter_customer_server
        }

        # 状态列表
        state_commands = {
            'customer': usingnet_server
        }

        # 匹配指令
        command_match = False
        for key_word in commands:
            if re.match(key_word, message.content):
                # 指令匹配后，设置默认状态
                set_user_state(openid, 'default')
                response = commands[key_word]()
                command_match = True
                break
        if not command_match:
            # 匹配状态
            state = get_user_state(openid)
            # 关键词、状态都不匹配，缺省回复
            if state == 'default' or not state:
                response = command_not_found()
            else:
                response = state_commands[state]()


    elif message.type == 'image':
        # 状态列表
        state_commands = {
            'customer': usingnet_server
        }
        # 匹配状态
        state = get_user_state(openid)
        # 关键词、状态都不匹配，缺省回复
        if state == 'default' or not state:
            response = command_not_found()
        else:
            response = state_commands[state]()

    elif message.type == 'voice':
        # 状态列表
        state_commands = {
            'customer': usingnet_server
        }
        # 匹配状态
        state = get_user_state(openid)
        # 关键词、状态都不匹配，缺省回复
        if state == 'default' or not state:
            response = command_not_found()
        else:
            response = state_commands[state]()

    elif message.type == 'click':
        commands = {
            'customer': enter_customer_server,
            'developing': developing,
            'template': template_message,
            'test': test
        }
        # 匹配指令后，重置状态
        set_user_state(openid, 'default')
        response = commands[message.key]()

    elif message.type == 'subscribe':
        print message.key
        if message.key != None:
            groups_will_id = message.key.split('_')[1]
        wechat.move_user(openid, int(groups_will_id))
        set_user_state(openid, 'default')
        response = subscribe()

    elif message.type == 'scan':
        print message.key
    else:
        pass

    # 保存最后一次交互的时间
    print openid
    set_user_last_interact_time(openid, message.time)

    return response

def usingnet_server():
    """优信客服服务"""
    timeout = int(message.time) - int(get_user_last_interact_time(openid))
    # 超过一段时间，退出模式
    if timeout > 20 * 60:
        set_user_state(openid, 'default')
        return command_not_found()
    else:
        usingnet.chat.delay(openid, message.raw)
        return 'success'

def enter_customer_server():
    """进入客服模式"""
    # 设置下班时间
    day_h, day_m, day_s = app.config['WORKING_TIME'].split('-')
    working_time = datetime.time(int(day_h),int(day_m),int(day_s))
    message_time = datetime.datetime.fromtimestamp(message.time).time()
    if message_time > working_time:
        return wechat.response_text('已经下班啦')
    else:
        set_user_state(openid, 'customer')
        return wechat.response_text(app.config['ENTER_CUSTOMER_STATE_TEXT'])

def update_menu_setting():
    """更新自定义菜单"""
    try:
        wechat.create_menu(app.config['MENU_SETTING'])
    except Exception, e:
        return wechat.response_text(e)
    else:
        return wechat.response_text('Done!')

def template_message():
    template_id=u"WYCLJc25ubEjXBZjOvWk6ihLOgtLQf6y3sv1PysrZdk"
    data = {}
    wechat.send_template_message(openid, template_id, data)
    return 'success'

def cancel_command():
    """取消状态"""
    content = app.config['CANCEL_COMMAND_TEXT']
    return wechat.response_text(content)

def command_not_found():
    """非关键词回复"""
    content = app.config['COMMAND_NOT_FOUND_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)

def developing():
    """开发公告"""
    return wechat.response_text('该功能开发中,敬请期待')

def test():
    """测试公告"""
    return wechat.response_text('该功能测试中,如遇到BUG请像客服反馈')

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
