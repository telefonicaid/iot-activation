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
import json
import tempfile
import os.path
# Keywords
CODE_CLOUD_NOT_FOUND = 404
CODE_OK = 200
# ERROR list


def read_config_file(file_name):
    """ Load a yaml configuration file in a dictionary

    :param file_name: the name file
    :return: dictionary with the file structure
    """
    logger.debug('Reading file [ %s ]', file_name)
    logger.debug(file_name)
    with open(file_name, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    file_name_cf = "config/cf_parameter.yaml"
    if os.path.isfile(file_name_cf):
        with open(file_name_cf, 'r') as ff:
            config_kite = yaml.load(ff, Loader=yaml.FullLoader)
        ff.close()
        config["KITE"] = config_kite
    file_name_cf_coap = "config/cf_EnableCoAP.yaml"
    if os.path.isfile(file_name_cf_coap):
        with open(file_name_cf_coap, 'r') as fff:
            config_kite_coap = yaml.load(fff, Loader=yaml.FullLoader)
        fff.close()
        config["COAP"]["enable"] = config_kite_coap
    return config

def read_config(file_name):
    """ Load a yaml configuration file in a dictionary

    :param file_name: the name file
    :return: dictionary with the file structure
    """
    logger.debug('Reading file [ %s ]', file_name)
    logger.debug(file_name)
    with open(file_name, 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    f.close()
    return config

def tmp_file(file_content):
    fd_key, temp_path = tempfile.mkstemp()
    temp_file = open(temp_path, 'w')
    temp_file.write(file_content)
    temp_file.close()
    os.close(fd_key)
    return temp_path


def is_json(str_json):
    json_check = False
    try:
        json_var =json.loads(str_json)
        json_check = (type(json_var) != int) # if str_json is a integer, conversion to json works incorrectly
    except Exception as e:
        json_check = False
    finally:
        return json_check
