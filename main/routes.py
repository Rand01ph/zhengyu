#!/usr/bin/env python
# encoding: utf-8

from flask import request, render_template, jsonify, Markup, abort, \
        send_from_directory
from . import app, wechat
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

@app.errorhandler(404)
def page_not_found(error):
    return "page not found!"
