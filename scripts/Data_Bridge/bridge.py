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
import socket
from kite_platform import *
from cloud_selector import *


def bridge_routine(udp_msg, ip, config, config_cloud):
    """ this function receive the ip, the UDP message and the configuration.
    It do the magic!

            response["code"] = 000
            response["msg"] = "xxxxxxxxxxxxxxxxxx"

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

        if kite_file_key["code"] == 200:
            if kite_file_cer["code"] == 200:

                logger.debug("Kite credentials extracted:")
                kite_parameters = kite_get_parameters(ip, kite_file_cer["msg"], kite_file_key["msg"])
                # kite = Kite(ip, kite_file_cer["msg"], kite_file_key["msg"])
                logger.info("GET information related to [ %s ] from  KITE Platform" % ip)

                if kite_parameters["code"] == 200:
                    logger.info("Found device cloud name [ %s ] and topic [ %s ] in KITE Platform" % (
                        kite_parameters["thing_name"], kite_parameters["thing_topic"]))

                    if kite_parameters["thing_name"] != '':
                        logger.debug("Kite parameter extracted")
                        logger.debug("Publishing in the Cloud")

                        if is_json(udp_msg):
                            json_udp_msg = json.loads(udp_msg)
                            json_msg = {"raw": json_udp_msg}
                        else:
                            json_msg = {"raw": udp_msg}

                        if "location" in config and config["location"] and kite_parameters["location"]:
                            location = {"longitude": kite_parameters["longitude"],
                                        "latitude": kite_parameters["latitude"]}
                            json_msg["location"] = location

                        response = cloud_publish(kite_parameters["thing_name"], kite_parameters["thing_topic"],
                                                 json_msg, config_cloud)

                    else:  # if kite_parameters["thing_name"] != '':
                        logger.warning("Not Found device Cloud Name in KITE Platform")
                        response["code"] = 404
                        response["msg"] = "KITE Platform: Device Name Not Found"
                else:  # if kite_parameters["code"] == 200:
                    logger.error("Not Connected to KITE Platform")
                    response["code"] = kite_parameters["code"]
                    response["msg"] = "KITE " + kite_parameters["msg"]

            else:  # if kite_file_cer["code"] == 200:
                logger.error("Not Connected to Cloud Get Parameter [ %s ]", config["KITE"]["certificate"])
                response["code"] = kite_file_cer["code"]
                response["msg"] = kite_file_cer["msg"]
        else:  # if kite_file_key["code"] == 200:
            logger.error("Not Connected to Cloud Get Parameter [ %s ]", config["KITE"]["private_key"])
            response["code"] = kite_file_key["code"]
            response["msg"] = kite_file_key["msg"]

    except Exception as e:
        logger.error('exception bridge_routine()')
        logger.error('message:{}'.format(e.message))
        traceback.print_exc(file=sys.stdout)

    finally:
        return response


def bridge_loop(config_file, config_cloud):
    """
    Listening loop,
    Open a socket to receive a UDP message and send the ACK
    :param config_file:
    :param config_cloud:
    :return:
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((config_file["UDP"]["ip"], (config_file["UDP"]["port"])))
        logger.debug("UDP port listener: [ %s ]", (config_file["UDP"]["port"]))
        loop_text = "######################## UDP Port [ %s ]: waiting for a message ########################"

        while True:
            logger.info(loop_text, config_file["UDP"]["port"])

            udp_msg, udp_ip = sock.recvfrom(1024)
            logger.info("Message Received [ %s ] from [ %s ] : [ %s ]" % (udp_msg, udp_ip[0], udp_ip[1]))

            response = bridge_routine(udp_msg, udp_ip[0], config_file, config_cloud)
            ack_msg = json.dumps(response)
            logger.debug("Generate ACK payload [ %s ]" % response)

            logger.info("Sent MESSAGE [ %s ] to [ %s ] : [ %s ]" % (ack_msg, udp_ip[0], udp_ip[1]))
            sock.sendto(ack_msg, udp_ip)

    except Exception as e:
        logger.error("exception bridge_loop()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    finally:
        return 0
