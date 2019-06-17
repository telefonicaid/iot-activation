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
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO     #
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN   #
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER #
# DEALINGS IN THE SOFTWARE.                                                                                            #
#                                                                                                                      #
########################################################################################################################
from __future__ import print_function
from log import *
import yaml
import tempfile

# Keywords
CODE_CLOUD_NOT_FOUND = 404

CODE_MQTT_MSG_SENT = 200
CODE_MQTT_ACCEPTED = 200
CODE_MQTT_TIME_OUT = 504
CODE_MQTT_REJECTED = 400

MSG_MQTT_MSG_SENT = 'OK: msg published'
MSG_MQTT_ACCEPTED = 'OK: msg published accepted'
MSG_MQTT_TIME_OUT = 'OK: msg published no response'

# ERROR list
CODE_ERROR_DEFAULT = 418
MSG_ERROR_DEFAULT = 'ERROR: I am a teapot'

CODE_ERROR_KITE_CONNECTION = 404
CODE_ERROR_KITE_CLOUD_ID = 501
CODE_ERROR_CLOUD_NOT_IMPLEMENTED = 501

MSG_ERROR_KITE_CONNECTION = 'ERROR: connection with Kite not established'
MSG_ERROR_KITE_CLOUD_ID = 'ERROR: Cloud id not defined in Kite'
MSG_ERROR_CLOUD_NOT_IMPLEMENTED = 'ERROR: Cloud connector not implemented'

CODE_ERROR_AWS_TOPIC_RESERVED = 401
MSG_ERROR_AWS_TOPIC_RESERVED = 'ERROR: Try to publish in an unauthorized topic '


def read_config (file):
    """ Load a yaml configuration file in a dictionary

    :param file: file name
    :return: dictionary with the file structure
    """
    logger.debug('Reading file')
    logger.debug(file)
    with open(file, 'r') as f:
        config = yaml.load(f)
    f.close()
    return config


def read_config (file_name):
    """ Load a yaml configuration file in a dictionary

    :param file: file name
    :return: dictionary with the file structure
    """
    logger.debug('Reading file')
    logger.debug(file)
    with open(file_name, 'r') as f:
        config = yaml.load(f)
    f.close()
    return config


def tmp_file(file_content):

    fd_key, temp_path = tempfile.mkstemp()
    temp_file = open(temp_path, 'w')
    temp_file.write(file_content)
    temp_file.close()
    os.close(fd_key)

    return temp_path

