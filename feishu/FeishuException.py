# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/11 5:54 下午
@desc:
"""

import json


class FeishuException(Exception):
    """
        Error handling Feishu
    """

    def __init__(self, status, data):
        super(FeishuException, self).__init__()
        self.__status = status
        self.__data = data
        self.args = (status, data)

    @property
    def status(self):
        return self.__status

    @property
    def data(self):
        return self.__data

    def __str__(self):
        return "{status} {data}".format(status=self.status, data=json.dumps(self.data))


class UnknownException(FeishuException):
    """
    When Unknown Exception
    """


class RequestException(FeishuException):
    """
    When Request Exception
    """
