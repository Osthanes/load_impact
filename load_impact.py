#!/usr/bin/python

import sys
import logging
import os
import requests
from loadimpact import (
    ApiTokenClient, ApiError, LoadZone, Test, TestConfig, TestResult, __version__ as li_sdk_version)

#DEBUG = os.environ.get('DEBUG')

# ascii color codes for output
LABEL_GREEN = '\033[0;32m'
LABEL_RED = '\033[0;31m'
LABEL_COLOR = '\033[0;33m'
LABEL_NO_COLOR = '\033[0m'
STARS = "**********************************************************************"

#load app url
TEST_URL = os.environ.get('TEST_URL')
TEST_ID = os.environ.get('TEST_ID')

def setup_logging():
    logger = logging.getLogger('pipeline')
#    if DEBUG:
#        logger.setLevel(logging.DEBUG)
#    else:
#        logger.setLevel(logging.INFO)

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
#    if DEBUG:
#        handler.setLevel(logging.DEBUG)
#    else:
#        handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger

# Start
logging.captureWarnings(True)
LOGGER = setup_logging()

#setup LI client
client = ApiTokenClient()

#if no test provided, create default
if not TEST_ID:
    LOGGER.info("No test ID provided, creating default test.")
    # Create user scenario
    load_script = """
    local response = http.get("%s")
    log.info("Load time: "..response.total_load_time.."s")
    client.sleep(10)
    """ % TEST_URL
    
    user_scenario = client.create_user_scenario({
        'name': "simple scenario",
        'load_script': load_script
    })

    # Create test config with user scenario created above
    config = client.create_test_config({
        'name': 'Default IBM Bluemix Test',
        'url': TEST_URL,
        'config': {
            "user_type": "sbu",
            "load_schedule": [{"users": 50, "duration": 5}],
            "tracks": [{
                "clips": [{
                    "user_scenario_id": user_scenario.id, "percent": 100
                }],
                "loadzone": LoadZone.AMAZON_US_ASHBURN
            }]
        }
    })
    LOGGER.info("Starting test [%s]" % user_scenario)
    
else:
    LOGGER.info("Test ID provided, starting test [%s]" % TEST_ID)
    config = client.get_test_config(TEST_ID)

#run test   
test = config.start_test()
    
#stream data
#stream = test.result_stream([
#    TestResult.result_id_from_name(TestResult.LIVE_FEEDBACK),
#    TestResult.result_id_from_name(TestResult.ACTIVE_USERS,
#                                   load_zone_id=world_id),
#    TestResult.result_id_from_name(TestResult.REQUESTS_PER_SECOND,
#                                   load_zone_id=world_id),
#    TestResult.result_id_from_name(TestResult.USER_LOAD_TIME,
#                                   load_zone_id=world_id)])
#
#for data in stream(poll_rate=3):
#    print data[TestResult.result_id_from_name(TestResult.LIVE_FEEDBACK)]
#    time.sleep(3)