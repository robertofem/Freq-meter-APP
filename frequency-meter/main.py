#!/usr/bin/env python3
"""Application main executable, for initializing the whole program"""
# Standard libraries
import logging.config
import sys

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)8s %(name)s '
                      '%(module)s:%(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(asctime)s %(levelname)8s: %(message)s'
        },
    },
    'handlers': {
        'file_view': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': 'tmp.log',
            'delay': True
        },
    },
    'loggers': {
        'view': {
            'handlers': ['file_view'],
            'level': 'DEBUG'
        },
    }
}

if __name__ == '__main__':
    from view import startup
    logging.config.dictConfig(LOGGING)
    sys.exit(startup.run())
