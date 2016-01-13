#!/usr/bin/env python
# encoding: utf-8

DEBUG = False

MAIN_URL = "http://zhengyu.tanyawei.com/"

WELCOME_TEXT = u"您好，这里是正誉官方微信。如有工商财税问题和工商会计事项办理进度可发微信进行提问，我们有专业的会计维护人员为您服务，紧急联系电话：020-22810165"

COMMAND_NOT_FOUND_TEXT = u"正誉官方微信为您服务，如需人工服务"

CANCEL_COMMAND_TEXT = u"已回到正常模式啦~\n"

HELP_TEXT = u"\n\n请点击菜单\n服务中心－专属客服\n或者回复“客服”\n进入人工客服模式"

ENTER_CUSTOMER_STATE_TEXT = u"已进入客服模式\n回复你想要咨询的问题\n\n回复“取消”退出咨询"

CUSTOMER_OUTLINE_STATE_TEXT = u"客服暂时不在线，请稍后再来咨询"

FAQ_TEXT = u"您好，如您有什么问题可直接在公众微信号主键面输入问题，我们将会有专属客服为您解答，或拨打我们客服热线020-22810316，感谢您对正誉的支持！"

WECHAT_ACCOUNT_MEDIA_ID = u'_6fyppWmXw8VxJRnBeZvxs42wIxrQp4X4XNRyKI2WTw'

BUSINESS_ACCOUNT_INFO_TEXT = u'户名: \n广州市正誉企业管理咨询有限公司\n\n开户行：\n工行广州小北路支行\n\n账号：\n3602010819200081844'

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
                    "type": "view",
                    "name": "公司注册",
                    "url": "http://zhengyu.tanyawei.com/company_registry.html",
                    "sub_button": []
                },
                {
                    "type": "view",
                    "name": "财税代理",
                    "url": "http://zhengyu.tanyawei.com/tax_agents.html",
                    "sub_button": []
                },
                {
                    "type": "view",
                    "name": "顾问服务",
                    "url": "http://zhengyu.tanyawei.com/consultancy_service.html",
                    "sub_button": []
                },
                {
                    "type": "view",
                    "name": "商标注册",
                    "url": "http://zhengyu.tanyawei.com/trademark_registration.html",
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
                    "key": "faq",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "专家咨询",
                    "key": "zhuanjia",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "投诉处理",
                    "key": "tousu",
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
                    "key": "wechat_account",
                    "sub_button": []
                },
                {
                    "type": "click",
                    "name": "公司账户",
                    "key": "business_account",
                    "sub_button": []
                }
            ]
        }
    ]
}
