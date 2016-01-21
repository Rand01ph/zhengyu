#!/usr/bin/env python
# encoding: utf-8

from flask import request, render_template, jsonify, Markup, abort, \
        send_from_directory, Response
import json
from . import app, wechat, redis
from .utils import check_signature
from .response import wechat_response
from wechat_sdk.exceptions import OfficialAPIError

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
    刷新微信 access_token，写入缓存
    """
    wechat.grant_token()
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

@app.route('/userinfo', methods=["GET"])
def userinfo_for_usingnet():
    user_id = request.args.get('openid')
    tags = []
    try:
        wechat.get_user_info(user_id)
    except OfficialAPIError, e:
        content = u"获取用户信息失败，错误信息： %s\n用户ID：%s"
        app.logger.warning(content % (e, user_id))
        wechat.grant_token()
        token = wechat.get_access_token()
        access_token = token['access_token']
        # 存入缓存，设置过期时间
        redis.set("wechat:access_token", access_token, 7000)
    finally:
        user_info = wechat.get_user_info(user_id)

    #  if "openid" not in user_info:
        #  content = u"获取用户信息失败: %s\n用户ID：%s"
        #  app.logger.warning(content % (user_info, user_id))
        #  if user_info["errcode"] == 40001:
            #  # access_token 失效，更新
            #  update_access_token()
            #  # 再次获取
            #  user_info = wechat.get_user_info(user_id)

    group_id = user_info['groupid']
    group_name = wechat.get_groups()['groups']
    for i in group_name:
        if i['id'] == group_id:
            tags.append(i['name'])
    user_info["tags"] = tags

    user_info.setdefault("name", user_info["nickname"])
    del(user_info["nickname"])

    user_info["email"] = ""
    user_info["phone"] = ""

    js = {"OK" : True, "data": user_info}
    return Response(json.dumps(js, sort_keys=True, indent=2),  mimetype='application/json')
#    return jsonify(user_info)

@app.route('/groups/', methods=["GET"])
def groups_for_usingnet():
    return jsonify(wechat.get_groups())

@app.route('/material_lis/', methods=["GET"])
def material_lis():
    return jsonify(wechat.get_material_list("image"))

@app.route('/update_menu_setting/', methods=["GET"])
def update_menu():
    try:
        wechat.create_menu(app.config['MENU_SETTING'])
    except Exception, e:
        return e
    else:
        return "Update menu OK"

@app.errorhandler(404)
def page_not_found(error):
    return "page not found!"
