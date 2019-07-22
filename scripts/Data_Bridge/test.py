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
import socket
from cloud_selector import *
from kite_platform import *


def test_server():
    """
    Checks Server requirements
    :return: Boolean (True/False)
    """
    status = True
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)

    logger.info("Hostname : [ %s ]", host_name)
    logger.info("Host IP Address : [ %s ]", host_ip)

    return status


def test_python():
    """
    Checks Python requirements
    :return: Boolean (True/False)
    """
    logger.info("Checking Python version")
    logger.debug(sys.version_info)
    logger.info("Python version : [ %s.%s.%s ]", sys.version_info.major, sys.version_info.minor, sys.version_info.micro)

    return True


def test(config_file, config_cloud):
    """
    Checks program requirements
    :return: Boolean (True/False)
    """
    flag_test_server = test_server()
    flag_test_python = test_python()
    flag_test_cloud = cloud_test_credentials(config_file, config_cloud)

    # kite_file_key = cloud_get_parameter(config_file["KITE"]["private_key"], config_cloud)
    # kite_file_cer = cloud_get_parameter(config_file["KITE"]["certificate"], config_cloud)
    # flag_test_kite = kite_test_credentials(kite_file_cer,kite_file_key)

    return flag_test_server and flag_test_python and flag_test_cloud






