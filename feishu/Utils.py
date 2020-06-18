# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/11 6:10 下午
@desc:
"""

import json
import requests

from .Logs import logger
from .FeishuException import RequestException


class FeishuBase:
    retry = 3


class Request:
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

        if retry:
            self.retry = retry
            self.adapter = requests.adapters.HTTPAdapter(max_retries=self.retry)
            self.session.mount("https://", self.adapter)
            self.session.mount("http://", self.adapter)

    def get(self, url, data):
        return self.response(url, data, 'get')

    def post(self, url, data=None):
        return self.response(url, data, 'post')

    def response(self, url, data, method):
        url = "%s%s" % (self.BASE_API_SERVER, url)
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
