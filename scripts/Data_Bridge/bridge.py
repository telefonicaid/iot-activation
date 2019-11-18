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
from kite_platform import *
from cloud_selector import *


def bridge(id, udp_msg, ip, config, config_cloud, request):
    """ this function receive the ip, the message and the configuration.
    It do the magic!

            response["code"] = 000
            response["msg"] = "xxxxxxxxxxxxxxxxxx"

    :param id: uuid
    :param udp_msg: string with the message
    :param ip: a ip address '0.0.0.0'
    :param config: configuration
    :param config_cloud: the configuration cloud
    :return: response
    """
    response = {"code": 500, "msg": "Bridge - Internal Server Error"}
    try:
        kite_file_key = cloud_get_parameter(config["KITE"]["private_key"], config_cloud)
        kite_file_cer = cloud_get_parameter(config["KITE"]["certificate"], config_cloud)

        if kite_file_key["code"] == CODE_OK:
            if kite_file_cer["code"] == CODE_OK:

                isajson = is_json(udp_msg)
                icc = None
                if isajson:
                    json_udp_msg = json.loads(udp_msg)
                    if "icc" in json_udp_msg:
                        icc = json_udp_msg["icc"]

                logger.info("%s - GET information related to [ %s ] and APN [ %s ] in KITE Platform" % (id, ip, config["KITE"]["apn"]))
                kite_parameters = kite_get_parameters(ip, kite_file_cer["msg"], kite_file_key["msg"], icc, config)
                logger.info("%s - KITE Response status code [ %s ]" % (id, kite_parameters["code"]))

                if kite_parameters["code"] == CODE_OK:
                    logger.info("%s - Found device cloud name [ %s ] and topic [ %s ] in KITE Platform" % (id,
                                                                                                           kite_parameters[
                                                                                                               "thing_name"],
                                                                                                           kite_parameters[
                                                                                                               "thing_topic"]))

                    if kite_parameters["thing_name"] != '':

                        if request == "POST":
                            if isajson:
                                json_msg = {"raw": json_udp_msg}
                            else:
                                json_msg = {"raw": udp_msg}

                            if "location" in config and config["location"] and kite_parameters["location"]:
                                location = {"longitude": kite_parameters["longitude"],
                                            "latitude": kite_parameters["latitude"]}
                                json_msg["location"] = location

                            response = cloud_publish(id, kite_parameters["thing_name"], kite_parameters["thing_topic"],
                                                     json_msg, config_cloud)
                        elif request == "GET":
                            response = cloud_get(id, kite_parameters["thing_name"], config_cloud)

                    else:  # if kite_parameters["thing_name"] == '':
                        logger.warning("%s - Not Found device Cloud Name in KITE Platform", id)
                        response["code"] = 404
                        response["msg"] = "KITE Platform: Device Name Not Found"
                else:  # if kite_parameters["code"] != CODE_OK:
                    logger.error("%s - Not Connected to KITE Platform", id)
                    response["code"] = kite_parameters["code"]
                    response["msg"] = "KITE " + kite_parameters["msg"]

            else:  # if kite_file_cer["code"] != CODE_OK:
                logger.error("%s - Not Connected to Cloud Get Parameter [ %s ]", id, config["KITE"]["certificate"])
                response["code"] = kite_file_cer["code"]
                response["msg"] = kite_file_cer["msg"]
        else:  # if kite_file_key["code"] != CODE_OK:
            logger.error("%s - Not Connected to Cloud Get Parameter [ %s ]", id, config["KITE"]["private_key"])
            response["code"] = kite_file_key["code"]
            response["msg"] = kite_file_key["msg"]

    except Exception as e:
        logger.error('%s - exception bridge_POST()', id)
        logger.error('message:{}'.format(e.message))
        traceback.print_exc(file=sys.stdout)

    finally:
        return response
