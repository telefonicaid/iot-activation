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
from utils import *
from cloud_selector_aws import *
#from cloud_selector_gcp import *


def cloud_configure(config):
    """ Use the configuration fil for select and load the Cloud configuration

    if the selected cloud is not implemented it returns an error code
    config_cloud["code"] = CODE_CLOUD_NOT_FOUND
    CODE_CLOUD_NOT_FOUND = 404 (utils.py)

    :param config: configuration
    :return: Cloud configuration
    """
    try:
        config_cloud = {}
        if config["cloud"] == "AWS":
            logger.debug("CLOUD: Selected connect to AWS:")
            config_cloud=read_config('config/Configuration_AWS.yaml')
            config_cloud["cloud"] = "AWS"
        else:
            if config["cloud"] == "GCP":
                logger.debug("CLOUD: Selected connect to Google Cloud:")
                config_cloud = read_config('config/Configuration_GCP.yaml')
                config_cloud["cloud"] = "GCP"
            else:
                logger.error("CLOUD: Cloud not defined")
                config_cloud["code"] = CODE_CLOUD_NOT_FOUND

        return config_cloud

    except Exception as e:
        logger.error("CLOUD: exception cloud_config()")
        traceback.print_exc(file=sys.stdout)


def cloud_publish(thing, topic, status, config_cloud):
    """ Invokes the publish function corresponding to the library of the selected cloud.

    if the selected cloud is not implemented it returns an error code
    config_cloud["code"] = CODE_CLOUD_NOT_FOUND
    CODE_CLOUD_NOT_FOUND = 404 (utils.py)

    :param thing:
    :param topic:
    :param status:
    :param config_cloud:
    :return:
    """
    try:
        response = {}

        if config_cloud["cloud"] == "AWS":
            logger.debug("CLOUD: Selected Publish in AWS:")
            response = cloud_publish_aws(thing, topic, status, config_cloud)
        else:
            if config_cloud["cloud"] == "GCP":
                logger.debug("CLOUD: Selected Publish in GCP:")
                response = cloud_publish_gcp(thing, topic, status, config_cloud)
            else:
                logger.error("CLOUD: Cloud not defined")
                response["code"] = CODE_ERROR_CLOUD_NOT_IMPLEMENTED
                response["msg"] = MSG_ERROR_CLOUD_NOT_IMPLEMENTED

        return response

    except Exception as e:
        logger.error("CLOUD: exception cloud_publish()")
        traceback.print_exc(file=sys.stdout)


def cloud_get_parameter(parameter_name, config_cloud):
    try:
        parameter = ""

        if config_cloud["cloud"] == "AWS":
            logger.debug("CLOUD: Selected get parameter for AWS:")
            parameter = cloud_get_parameter_aws(parameter_name, config_cloud)
        else:
            if config_cloud["cloud"] == "GCP":
                logger.debug("CLOUD: Selected Publish in GCP:")

            else:
                logger.error("CLOUD: Cloud not defined")

        return parameter

    except Exception as e:
        logger.error("CLOUD: exception cloud_get_parameter()")
        traceback.print_exc(file=sys.stdout)
