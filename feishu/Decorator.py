# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/11 7:36 下午
@desc:
"""

import time

from .Logs import logger
from functools import wraps


def _check(cls):
    """
        cls must have function:[get_tenant_access_token,get_app_access_token]
    """
    assert hasattr(cls, 'get_tenant_access_token'), 'get_tenant_access_token'
    assert hasattr(cls, 'get_app_access_token'), 'get_app_access_token'


def _get_token(cls, token_type):
    """
        when token expire flush,return token value
    """
    assert token_type in ['tenant_access_token', 'app_access_token'], token_type

    if not hasattr(cls.request, token_type) or not (getattr(cls.request, token_type) and
                                                    time.time() < getattr(cls.request, token_type)['expire']):
        setattr(cls.request, token_type, getattr(cls, 'get_%s' % token_type)())
        logger.debug('flush %s' % token_type)
    else:
        logger.debug('use cache %s' % token_type)
    return getattr(cls.request, token_type)[token_type]


def tenant_access_token(func):
    """
        auto add tenant_access_token to request headers
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0]
        _check(cls)
        cls.request.headers["Authorization"] = "Bearer " + _get_token(cls, 'tenant_access_token')
        return func(*args, **kwargs)

    return wrapper


def app_access_token(func):
    """
        auto add app_access_token to request headers
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        cls = args[0]
        _check(cls)
        cls.request.headers["Authorization"] = "Bearer " + _get_token(cls, 'app_access_token')
        return func(*args, **kwargs)

    return wrapper
