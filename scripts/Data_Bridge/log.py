########################################################################################################################
#                                                                                                                      #
# MIT License                                                                                                          #
#                                                                                                                      #
# Copyright (c) 2018 Telefonica R&D                                                                                    #
#                                                                                                                      #
# Permission is hereby granted, free of charge, to any person obtaining a copy  of this software and associated        #
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the  #
# rights in the Software without restriction, including without limitation the rights o use, copy, modify, merge,      #
# publish,  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and      #
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:                   #
#                                                                                                                      #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, NCLUDING BUT NOT LIMITED TO      #
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN   #
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER #
# DEALINGS IN THE SOFTWARE.                                                                                            #
#                                                                                                                      #
########################################################################################################################
from __future__ import print_function
import logging.handlers
import uuid
import sys
import os
import traceback


# Setting log
try:
    logger = logging.getLogger()
    if "LOG_LEVEL" in os.environ:
        if os.environ["LOG_LEVEL"] in ["INFO", "DEBUG", "WARNING", "ERROR"]:
            logger.setLevel(logging.os.environ["LOG_LEVEL"])
        else:
            logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    log_format = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s")
    handler.setFormatter(log_format)
    logger.addHandler(handler)

    filename = "log/data_bridge.log"
    loghandler = logging.handlers.TimedRotatingFileHandler(filename, when='midnight', backupCount=7)
    log_format = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s")
    loghandler.setFormatter(log_format)
    logger.addHandler(loghandler)

    logger.info("Setting log ")

except Exception as e:
    logger.error("exception main()")
    logger.error("message:{}".format(e.message))
    traceback.print_exc(file=sys.stdout)

