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

# Keywords
CODE_CLOUD_NOT_FOUND = 404

# ERROR list


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
        json.loads(str_json)
        json_check = True
    except Exception as e:
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return json_check
