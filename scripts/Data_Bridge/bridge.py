########################################################################################################################
#                                                                                                                      #
# MIT License                                                                                                          #
#                                                                                                                      #
# Copyright (c) 2018 Telefonica R&D                                                                                    #
#                                                                                                                      #
# Permission is hereby granted, free of charge, to any person obtaining a copy  of this software and associated        #
# documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the  #
# rights in the Software without restriction, including without limitation the rights o use, copy, modify, merge,      #
# publish,  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and      #
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:                   #
#                                                                                                                      #
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO     #
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN   #
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER #
# DEALINGS IN THE SOFTWARE.                                                                                            #
#                                                                                                                      #
########################################################################################################################

from __future__ import print_function
from log import *
from utils import *
import json
import socket
from kite_platform import *
from cloud_selector import *



def bridge_routine(udp_msg, ip, config, config_cloud):
    """ this function get the ip message and configuration and do the magic!

            response["code"] = 000
            response["msg"] = "xxxxxxxxxxxxxxxxxx"

    :param udp_msg: string with the message
    :param ip: a ip address '0.0.0.0'
    :param config_cloud: the configuration cloud
    :return: response
    """
    try:
        response = {}
        response["code"] = CODE_ERROR_DEFAULT
        response["msg"] = MSG_ERROR_DEFAULT

        # KITE
        kite_file_key = cloud_get_parameter(config["KITE"]["private_key"], config_cloud)
        kite_file_cer = cloud_get_parameter(config["KITE"]["certificate"], config_cloud)

        logger.debug("PARSER: KITE:")
        kite = Kite(ip, kite_file_cer, kite_file_key)
        logger.info("GET information related to [ %s ] from  KITE Platform" % kite.ip)

        if kite.status_ok:
            logger.info("Found device cloud name [ %s ] and topic [ %s ] in KITE Platform" %(kite.device_name, kite.cloud_topic))
            if kite.device_name != '':

                logger.debug('PARSER: publishing:')

                if "location" in config and config["location"] == True:
                    location = {"longitude": kite.longitude, "latitude": kite.latitude}
                    json_msg = json.loads(udp_msg)
                    json_msg["location"]=location
                    msg = json.dumps(json_msg)
                else:
                    msg = udp_msg

                response = cloud_publish(kite.device_name, kite.cloud_topic, msg, config_cloud)

            else: #kite.device_name != '':
                logger.warning("Not Found device Cloud Name in KITE Platform")
                response["code"] = CODE_ERROR_KITE_CLOUD_ID
                response["msg"] = MSG_ERROR_KITE_CLOUD_ID
        else: # if kite.status_ok:
            logger.error("Not Connected to KITE Platform")
            response["code"] = CODE_ERROR_KITE_CONNECTION
            response["msg"] = MSG_ERROR_KITE_CONNECTION

        return response

    except Exception as e:
        logger.error('exception bridge_routine()')
        logger.error('message:{}'.format(e.message))
        traceback.print_exc(file=sys.stdout)

