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
from Log import *
from Cloud_selector_AWS import *


"""
    PRIVATE: access the configuration to select the Cloud configuration 
    name: selector(config_cloud, config_scrt)
    param: config_cloud [yaml]
    param: config_scrt [yaml]
    return: Cloud configuration
"""
def selector(config_cloud, config_scrt):
    selection = ""
    for key, config_c in config_cloud.iteritems():
        if config_c["cloud"] == config_scrt["Connection"]:
            logger.info("CLOUD: Connecting with Cloud using conecction:")
            logger.info(config_scrt["Connection"])
            selection = config_c
    return selection


"""
    Access the configuration to select de connection to Cloud
    name: cloud_connector(config_cloud, config_scrt)
    param: config_cloud [yaml]
    param: config_scrt [yaml]
    return: Cloud connection
"""
def cloud_connector(config_cloud, config_scrt):
    try:
        # search for the chosen configuration
        connection = 0
        config_c = selector(config_cloud, config_scrt)

        if config_c["cloud"] == "AWS":
            logger.info("CLOUD: Selected connect to AWS:")
            connection = cloud_connector_AWS(config_c)
        else:
            if config_c["cloud"] == "AZURE":
                logger.info("CLOUD: No defined AZURE Connection")
            else:
                logger.error("Cloud not found")
                raise ValueError("No defined Connection")

        return connection

    except Exception as e:
        logger.error("exception cloud_connector()")

"""
    Access the configuration to select the Cloud and publish the status device
    name: cloud_publish(connection, status, config_cloud, config_scrt)
    param: connection to publish
    param: status to publish
    param: config_cloud [yaml]
    param: config_scrt [yaml]
    return: 0 if OK
"""
def cloud_publish(connection, status, config_cloud, config_scrt):
    try:
        # search for the chosen configuration
        config_c = selector(config_cloud, config_scrt)

        if config_c["cloud"] == "AWS":
            logger.info("CLOUD: Selected Publish in AWS:")
            cloud_publish_AWS(connection, status, config_cloud)
        else:
            if config_c["cloud"] == "AZURE":
                logger.info("CLOUD: Selected Publish in AZURE:")

            else:
                logger.error("Cloud not found")
                raise ValueError("No defined Publish")

        return 0

    except Exception as e:
        logger.error("exception cloud_publish()")

		