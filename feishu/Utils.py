# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/11 6:10 下午
@desc:
"""
import sys
import json
import requests
import time

from .Logs import logger
from .FeishuException import RequestException


class FeishuBase:
    retry = 3
    def __init__(self, app_id, app_secret, retry=None):

        self.app_id = app_id
        self.app_secret = app_secret

        assert app_id is None or isinstance(app_id, str), app_id
        assert app_secret is None or isinstance(app_secret, str), app_secret
        assert (
                retry is None
                or isinstance(retry, int)
                or isinstance(retry, urllib3.util.Retry)
        )

        self.request = Request(
            retry=retry
        )
        # assert app_verification_token is None or isinstance(app_verification_token, str), app_verification_token
    
    def get_tenant_access_token(self):
        """
        租户TOKEN
        :return:
        """
        url = "/auth/v3/tenant_access_token/internal/"
        req_body = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        self.request.tenant_access_token = self.request.get(url, req_body)
        self.request.tenant_access_token['expire'] += time.time()
        return self.request.tenant_access_token

    def get_app_access_token(self):
        """
        APP TOKEN
        :return:
        """
        url = "/auth/v3/app_access_token/internal/"
        req_body = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        self.request.app_access_token = self.request.get(url, req_body)
        self.request.app_access_token['expire'] += time.time()
        return self.request.app_access_token



class Request(FeishuBase):
    BASE_API_SERVER = 'https://open.feishu.cn/open-apis'

    def __init__(self, timeout=None, retry=None, **kwargs):
        self.port = 443
        self.protocol = "https"
        self.timeout = timeout
        self.verify = kwargs.get("verify", True)
        self.session = requests.Session()
        self.headers = {
            "Content-Type": "application/json"
        }

        self.app_access_token = None
        self.tenant_access_token = None

        self.retry = retry if retry else self.retry

        self.adapter = requests.adapters.HTTPAdapter(max_retries=self.retry)
        self.session.mount("https://", self.adapter)
        self.session.mount("http://", self.adapter)

    def get(self, url, data):
        return self.response(url, data, 'get')

    def put(self, url, data):
        return self.response(url, data, 'put')

    def post(self, url, data=None):
        return self.response(url, data, 'post')

    def response(self, url, data, method):
        url = "%s%s" % (self.BASE_API_SERVER, url)
        if sys.version_info.major == 2:
            data = bytes(json.dumps(data)).encode(encoding='utf8')
        else:
            data = bytes(json.dumps(data), encoding='utf8')

        r = getattr(self.session, method)(url=url,
                                          headers=self.headers,
                                          data=data,
                                          timeout=self.timeout,
                                          ).json()
        status_code = r.get('code', -1)

        if status_code != 0:
            raise RequestException(status=status_code, data=r.get('msg'))
        logger.debug('request url:%s; response:%s' % (url, r))
        return r
