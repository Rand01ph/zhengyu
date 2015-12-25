#!/usr/bin/env python
# encoding: utf-8

DEBUG = False

MAIN_URL = "http://zy.tanyawei.com/"

WELCOME_TEXT = u"您好，这里是正誉官方微信。如有工商财税问题和工商会计事项办理进度可发微信进行提问，我们有专业的会计维护人员为您服务，紧急联系电话：020-22810165"

COMMAND_NOT_FOUND_TEXT = u"收到你的留言啦！"

CANCEL_COMMAND_TEXT = u"已回到正常模式啦~\n"

HELP_TEXT = u"\n\n点击\n服务中心－专属客服\n进入人工客服模式"

ENTER_CUSTOMER_STATE_TEXT = u"已进入客服模式\n回复你想要咨询的问题\n\n回复“取消”退出咨询"

CUSTOMER_OUTLINE_STATE_TEXT = u"客服暂时不在线，请稍后再来咨询"

PHONE_NUMBER_TEXT = u"020-22810165"

WORKING_TIME = "23-00-00"

MENU_SETTING = {
    "button": [
        {
            "name": "公司业务",
            "sub_button": [
                {
                    "type": "click",
                    "name": "公司网站",
                    "key": "developing",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "公司注册",
                    "key": "developing",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "财税代理",
                    "key": "developing",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "顾问服务",
                    "key": "developing",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "商标注册",
                    "key": "template",
                    "sub_button": []
                }
            ]
        },
        {
            "name": "服务中心",
            "sub_button": [
                {
                    "type": "click",
                    "name": "专属客服",
                    "key": "customer",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "常见问题",
                    "key": "developing",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "专家咨询",
                    "key": "developing",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "投诉处理",
                    "key": "developing",
                    "sub_button": []
                }
            ]
        },
        {
            "name": "结算中心",
            "sub_button": [
                {
                    "type": "click",
                    "name": "微信结算",
                    "key": "developing",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "公司账户",
                    "key": "developing",
                    "sub_button": []
                }
            ]
        }
    ]
}
