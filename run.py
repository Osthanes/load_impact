#!/usr/bin/python

import sys
import logging
import os

DEBUG = os.environ.get('DEBUG')

# ascii color codes for output
LABEL_GREEN = '\033[0;32m'
LABEL_RED = '\033[0;31m'
LABEL_COLOR = '\033[0;33m'
LABEL_NO_COLOR = '\033[0m'
STARS = "**********************************************************************"

def setup_logging():
    logger = logging.getLogger('pipeline')
    if DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # if logmet is enabled, send the log through syslog as well
    if os.environ.get('LOGMET_LOGGING_ENABLED'):
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        logger.addHandler(handler)
        # don't send debug info through syslog
        handler.setLevel(logging.INFO)

    # in any case, dump logging to the screen
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    if DEBUG:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

# Start
LOGGER = setup_logging()
