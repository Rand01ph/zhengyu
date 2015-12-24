#!/usr/bin/env python
# encoding: utf-8

DEBUG = False

MAIN_URL = "http://zy.tanyawei.com/"

WELCOME_TEXT = u"您好，这里是正誉官方微信。如有工商财税问题和工商会计事项办理进度可发微信进行提问，我们有专业的会计维护人员为您服务，紧急联系电话：020-22810165"

PHONE_NUMBER_TEXT = u"020-22810165"

MENU_SETTING = {
    "button": [
        {
            "name": "我要了解",
            "sub_button": [
                {
                    "type": "click",
                    "name": "联系我们",
                    "key": "phone_number",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "专业服务",
                    "key": "express",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "公司简介",
                    "key": "info",
                    "sub_button": []
                }
            ]
        },
        {
            "name": "我要办理",
            "sub_button": [
                {
                    "type": "click",
                    "name": "财富问答",
                    "key": "sign",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "财富问答",
                    "key": "sign",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "财富问答",
                    "key": "sign",
                    "sub_button": []
                }
            ]
        },
        {
            "name": "服务中心",
            "sub_button": [
                {
                    "type": "click",
                    "name": "财富问答",
                    "key": "sign",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "财富问答",
                    "key": "sign",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "财富问答",
                    "key": "sign",
                    "sub_button": []
                }
            ]
        }
    ]
}
