#!/usr/bin/env python
# encoding: utf-8

from flask import request, render_template, jsonify, Markup, abort, \
        send_from_directory
from . import app, wechat, redis
from .utils import check_signature
from .response import wechat_response

@app.route("/", methods=['GET', 'POST'])
@check_signature
def handle_wechat_request():
    """
    处理回复微信请求
    """
    if request.method == 'POST':
        return wechat_response(request.data)
    else:
        # 微信接入验证
        return request.args.get('echostr', '')


@app.route(app.config['UPDATE_ACCESS_TOKEN_URL_ROUTE'], methods=["GET"])
def update_access_token():
    """
    读取微信最新 access_token，写入缓存
    """
    # 由于 wechat-python-sdk 中，generate_jsapi_signature -> grant_jsapi_ticket
    # 会顺带把 access_token 刷新了，所以先 grant_jsapi_ticket 再读取 access_token
    token = wechat.get_access_token()
    access_token = token['access_token']
    # 存入缓存，设置过期时间
    redis.set("wechat:access_token", access_token, 7000)
    return ('', 204)


@app.route(app.config['GET_QRCODE_URL_ROUTE'], methods=["GET"])
def groups_qrcode_show():
    qr_dict = {"action_name": "QR_LIMIT_STR_SCENE", "action_info": {"scene": {"scene_str": "default_value"}}}
    qr_str = ""
    groups_data = wechat.get_groups()
    for i in groups_data['groups']:
        qr_dict['action_info']['scene']['scene_str'] = i['id']
        qr_str += '<h1>'
        qr_str += i['name']
        qr_str += '</h1><br />'
        qr_str += '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket='
        qr_str += wechat.create_qrcode(qr_dict)['ticket']
        qr_str += '" /><br />'
    return qr_str


@app.errorhandler(404)
def page_not_found(error):
    return "page not found!"
