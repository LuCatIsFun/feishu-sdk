# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/11 6:06 下午
@desc:
"""
import time
import urllib3
import json

from datetime import datetime

from .Logs import logger
from .Utils import FeishuBase, Request
from .Decorator import tenant_access_token, app_access_token

class Bitable(FeishuBase):
    @tenant_access_token
    def add_record(self,app_token,table_id,fields):
        url='/bitable/v1/apps/%s/tables/%s/records'%(app_token,table_id)
        return self.request.post(url, data=fields)

    @tenant_access_token
    def search_records(self,app_token,table_id,filter):
        url='/bitable/v1/apps/%s/tables/%s/records?filter=%s'%(app_token,table_id,filter)
        return self.request.get(url, data=None)

    @tenant_access_token
    def update_record(self,app_token,table_id,record_id,fields):
        url='/bitable/v1/apps/%s/tables/%s/records/%s'%(app_token,table_id,record_id)
        return self.request.put(url, data=fields)

    @tenant_access_token
    def tables(self,user_open_id):
        url='/bitable/v1/apps/%s/tables'%(user_open_id)
        return self.request.get(url, data=None)

class Bot(FeishuBase):
    MESSAGE_MAP = {
        'title': '标题',
        'action': '操作',
        'time': '时间',
        'detail': '详情',
        'system': '系统',
        'reason': '原因',
        'status': '状态',
        'new password': '新密码',
        'name': '名称',
        'username': '用户名',
        'default password': '默认密码',
        'approve user': '审批人',
        'approve result': '审批意见'
    }

    MESSAGE_IMAGE_KEY = None
    MESSAGE_AUTO_ADD_TIME = False
    MESSAGE_BUTTON_CONFIRM = True
    MESSAGE_NOTICE_NAME = '通知'


    @tenant_access_token
    def send_user_message(self, user_open_id, text=None):
        assert all([text]), 'At least one of "text" or "data" is not empty'
        url = "/im/v1/messages?receive_id_type=open_id"
        content={
            "text": text
        }
        data = {
            "receive_id": user_open_id,
            "msg_type": "text",
            "content":json.dumps(content)
        }
        return self.request.post(url, data=data)

    @tenant_access_token
    def send_user_card_message(self, user_open_id, text=None, **kwargs):
        url = "/message/v4/send/"
        card_body = self.get_card_message_body(text, **kwargs)
        card_body['open_id'] = user_open_id
        return self.request.post(url, data=card_body)

    @tenant_access_token
    def send_group_message(self, open_chat_id, text=None, data=None):
        assert any([text, data]), 'At least one of "text" or "data" is not empty'
        url = "/message/v4/send/"

        if not data:
            data = {
                "open_chat_id": open_chat_id,
                "msg_type": "text",
                "content": {
                    "text": text
                }
            }
        return self.request.post(url, data=data)

    @app_access_token
    def get_user_info(self, code):
        url = "/authen/v1/access_token"
        data = {
            "app_access_token": self.request.app_access_token['app_access_token'],
            "code": code,
            "grant_type": "authorization_code"

        }
        return self.request.post(url, data=data)['data']

    @tenant_access_token
    def get_bot_info(self):
        url = "/bot/v3/info/"
        return self.request.post(url)['bot']

    @tenant_access_token
    def create_group(self, **kwargs):
        """
            https://open.feishu.cn/document/ukTMukTMukTM/ukDO5QjL5gTO04SO4kDN
        """
        assert 'name' not in kwargs.keys() or isinstance(kwargs['name'], str), kwargs['name']
        assert 'description' not in kwargs.keys() or isinstance(kwargs['description'], str), kwargs['description']
        assert 'open_ids' not in kwargs.keys() or isinstance(kwargs['open_ids'], list), kwargs['open_ids']
        assert 'user_ids' not in kwargs.keys() or isinstance(kwargs['user_ids'], list), kwargs['user_ids']
        assert 'i18n_names' not in kwargs.keys() or isinstance(kwargs['i18n_names'], dict), kwargs['i18n_names']
        assert 'only_owner_add' not in kwargs.keys() or \
               isinstance(kwargs['only_owner_add'], bool), kwargs['only_owner_add']
        assert 'share_allowed' not in kwargs.keys() or \
               isinstance(kwargs['share_allowed'], bool), kwargs['share_allowed']
        assert 'only_owner_at_all' not in kwargs.keys() or \
               isinstance(kwargs['only_owner_at_all'], bool), kwargs['only_owner_at_all']
        assert 'only_owner_edit' not in kwargs.keys() or \
               isinstance(kwargs['only_owner_edit'], bool), kwargs['only_owner_edit']

        assert any(['open_ids' in kwargs.keys() and kwargs['open_ids'],
                    'user_ids' in kwargs.keys() and kwargs['user_ids']]), "user_ids and open_ids cannot both be empty"

        url = "/chat/v4/create/"
        return self.request.post(url, data=kwargs)

    def get_authorization_code_by_browser_url(self):
        redirect_uri = "https://example.com"
        return self.get_oauth_login_url(redirect_uri)

    def get_oauth_login_url(self, redirect_uri, state=None):
        url = self.request.BASE_API_SERVER + \
              "/authen/v1/index?app_id={app_id}&redirect_uri={redirect_uri}&state={state}".format(
                  redirect_uri=redirect_uri, app_id=self.app_id,
                  state=state if state else ''
              )
        return url

    def configuration_card_message(self, **kwargs):

        assert 'image_key' not in kwargs.keys() or isinstance(kwargs['image_key'], str), 'type must str'
        assert 'auto_add_time' not in kwargs.keys() or isinstance(kwargs['auto_add_time'], bool), 'type must bool'
        assert 'button_confirm' not in kwargs.keys() or isinstance(kwargs['button_confirm'], bool), 'type must bool'
        assert 'name' not in kwargs.keys() or isinstance(kwargs['name'], str), 'type must str'

        self.MESSAGE_IMAGE_KEY = kwargs['image_key'] if 'image_key' in kwargs.keys() else self.MESSAGE_IMAGE_KEY
        self.MESSAGE_AUTO_ADD_TIME = kwargs['auto_add_time'] if 'auto_add_time' in kwargs.keys() else \
            self.MESSAGE_AUTO_ADD_TIME
        self.MESSAGE_BUTTON_CONFIRM = kwargs['button_confirm'] if 'button_confirm' in kwargs.keys() else \
            self.MESSAGE_BUTTON_CONFIRM
        self.MESSAGE_NOTICE_NAME = kwargs['name'] if 'name' in kwargs.keys() else self.MESSAGE_NOTICE_NAME

    def get_card_message_body(self, text=None, **kwargs):

        assert 'title' in kwargs.keys(), 'title can not be null'

        if 'time' not in kwargs.keys() and self.MESSAGE_AUTO_ADD_TIME:
            kwargs['time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not text:
            body = {
                "tag": "div",
                "fields": []
            }
            for k in kwargs.keys():
                if k not in ['title', 'button']:
                    body['fields'].append({
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": "**%s**：%s" % (
                                self.MESSAGE_MAP.get(k, k),
                                kwargs[k]
                            )
                        }
                    })

        else:
            body = {
                "tag": "div",
                "text": {
                            "tag": "plain_text",
                            "content": text
                        }
            }
        extra = {
            "tag": "action",
            "actions": []
        }

        if 'button' in kwargs.keys() and kwargs['button']:
            for bt in kwargs['button']:
                if 'confirm' in bt.keys():
                    confirm = bt['confirm']
                else:
                    confirm = self.MESSAGE_BUTTON_CONFIRM
                button_body = {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": bt['title']
                    },
                    "type": bt['type'],
                    "value": bt['value'],
                }
                if confirm:
                    button_body['confirm'] = {
                        "title": {
                            "tag": "plain_text",
                            "content": "操作确认"
                        },
                        "text": {
                            "tag": "plain_text",
                            "content": "确认进行此操作吗？"
                        }
                    }
                extra['actions'].append(button_body)

        card_body = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True
                },
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": kwargs['title']
                    }
                },
                "elements": [
                    {
                        "tag": "hr"
                    },
                    {
                        "tag": "note",
                        "elements": [
                            {
                                "tag": "plain_text",
                                "content": self.MESSAGE_NOTICE_NAME
                            }
                        ]
                    }
                ]
            }
        }

        card_body['card']['elements'].insert(0, body)
        card_body['card']['elements'].insert(1, extra)
        if self.MESSAGE_IMAGE_KEY:
            card_body['card']['elements'][len(card_body['card']['elements'])-1]['elements'].insert(0, {
                                "tag": "img",
                                "img_key": self.MESSAGE_IMAGE_KEY,
                                "alt": {
                                    "tag": "plain_text",
                                    "content": "Note image size：16*16"
                                }
                            })
        logger.debug(card_body)
        return card_body
