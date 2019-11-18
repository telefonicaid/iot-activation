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
from cloud_selector_aws import *

CODE_ERROR_CLOUD_NOT_IMPLEMENTED = 501
MSG_CLOUD_NOT_IMPLEMENTED = 'ERROR: Cloud id Not Implemented'


def cloud_configure(config):
    """
    Function Invocation for configure the selected Cloud
    :param config: configuration
    :return: Cloud configuration
    """
    try:
        if config["cloud"] == "AWS":
            logger.debug("CLOUD: Selected AWS log file:")
            config_cloud = cloud_configure_aws(config)
        else:
            logger.error("CLOUD: Cloud not defined")
            config_cloud = {"code": CODE_ERROR_CLOUD_NOT_IMPLEMENTED, "msg": MSG_CLOUD_NOT_IMPLEMENTED}

        return config_cloud

    except Exception as e:
        logger.error("CLOUD: exception cloud_config()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)


def cloud_publish(id, thing, topic, status, config_cloud):
    """
    Function Invocation for publish in the selected Cloud.
    :param thing:
    :param topic:
    :param status:
    :param config_cloud:
    :return: response = {"code": 200, "msg": "OK"}
    """
    response = {"code": 500, "msg": "Publish - Internal Server Error"}
    try:
        if config_cloud["cloud"] == "AWS":
            logger.debug("CLOUD: Selected Publish in AWS:")
            response = cloud_publish_aws(id, thing, topic, status, config_cloud)
        else:
            logger.error("%s - CLOUD: Cloud not defined", id)
            response = {"code": CODE_ERROR_CLOUD_NOT_IMPLEMENTED, "msg": MSG_CLOUD_NOT_IMPLEMENTED}

    except Exception as e:
        logger.error("CLOUD: exception cloud_publish()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    finally:
        return response


def cloud_get(id, thing, config_cloud):
    """
    Function Invocation for publish in the selected Cloud.
    :param id: uuid
    :param thing:
    :param config_cloud:
    :return: response = {"code": 200, "msg": "OK"}
    """
    response = {"code": 500, "msg": "Publish - Internal Server Error"}
    try:
        if config_cloud["cloud"] == "AWS":
            logger.debug("CLOUD: Selected Publish in AWS:")
            response = cloud_get_aws(id, thing, config_cloud)
        else:
            logger.error("%s - CLOUD: Cloud not defined", id)
            response = {"code": CODE_ERROR_CLOUD_NOT_IMPLEMENTED, "msg": MSG_CLOUD_NOT_IMPLEMENTED}

    except Exception as e:
        logger.error("CLOUD: exception cloud_publish()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    finally:
        return response


def cloud_get_parameter(parameter_name, config_cloud):
    """
    Function Invocation for the parameter stored in the selected Cloud
    :param parameter_name:
    :param config_cloud:
    :return: parameter {"code": 200, "msg": parameter_value}
    """
    parameter = {"code": 500, "msg": "Get parameter - Internal Server Error"}
    try:
        if config_cloud["cloud"] == "AWS":
            logger.debug("CLOUD: Selected get parameter for AWS:")
            parameter = cloud_get_parameter_aws(parameter_name)
        else:
            logger.error("CLOUD: Cloud not defined")
            parameter = {"code": CODE_ERROR_CLOUD_NOT_IMPLEMENTED, "msg": MSG_CLOUD_NOT_IMPLEMENTED}
    except Exception as e:
        logger.error("CLOUD: exception cloud_get_parameter()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return parameter


def cloud_log(config_cloud):
    parameter = {"code": 500, "msg": "Get parameter - Internal Server Error"}
    try:
        if config_cloud["cloud"] == "AWS":
            logger.debug("CLOUD: Selected set log for AWS:")
            parameter = cloud_log_aws(config_cloud)
        else:
            logger.error("CLOUD: Cloud not defined")
            parameter = {"code": CODE_ERROR_CLOUD_NOT_IMPLEMENTED, "msg": MSG_CLOUD_NOT_IMPLEMENTED}
    except Exception as e:
        logger.error("CLOUD: exception cloud_get_parameter()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return parameter


def test_cloud(config_file, config_cloud):
    """
    Function Invocation for test the credentials of the selected Cloud
    :param config_file:
    :param config_cloud:
    :return: Boolean (True/False)
    """
    logger.info("Testing Cloud Credentials")
    status = False
    try:
        if config_cloud["cloud"] == "AWS":
            logger.debug("CLOUD: Selected test credentials for AWS:")
            status_environment = cloud_test_aws(config_file, config_cloud)
            # status_cred = cloud_test_credentials_aws(config_file, config_cloud)
            status = status_environment
        else:
            logger.error("CLOUD: Cloud not defined")
    except Exception as e:
        logger.error("CLOUD: exception cloud_get_parameter()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return status
