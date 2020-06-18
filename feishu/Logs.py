# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/11 5:04 下午
@desc:
"""

import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(pathname)s %(module)s [%(funcName)s:%(lineno)d]: %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        'feishu': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}

SUPPORT_LOG_LEVEL = ['ERROR', 'WARNING', 'INFO', 'WARN', 'DEBUG']


def set_log_level(level):
    assert isinstance(level, str), level
    level = str(level).upper()
    assert level in SUPPORT_LOG_LEVEL, 'wrong log level:%s' % level
    logger.setLevel(getattr(logging, level))


logging.config.dictConfig(LOGGING)
logger = logging.getLogger('feishu')
logger.setLevel(logging.ERROR)
