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
import uuid
from log import *
from bridge import *



def udp_loop(config_file, config_cloud):
    """
    Listening loop,
    Open a socket to receive a UDP message and send the ACK
    :param config_file:
    :param config_cloud:
    :return:
    """
    try:

        logger.info("UDP  socket listening in: [ %s:%s ]" % (config_file["UDP"]["ip"], config_file["UDP"]["port"]))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((config_file["UDP"]["ip"], (config_file["UDP"]["port"])))

        loop_text = "######################## UDP Port [ %s ]: waiting for a message ########################"
        logger.info(loop_text, config_file["UDP"]["port"])

        while True:
            udp_msg, udp_ip = sock.recvfrom(1024)
            uuid_udp = uuid.uuid4().hex
            logger.info("%s - Message Received [ %s ] from [ %s ] : [ %s ]" % (uuid_udp, udp_msg, udp_ip[0], udp_ip[1]))

            response = bridge(uuid_udp, udp_msg, udp_ip[0], config_file, config_cloud, "POST")
            ack_msg = json.dumps(response)
            logger.debug("%s - Generate ACK payload [ %s ]" % (uuid_udp, response))

            logger.info("%s - Sent MESSAGE [ %s ] to [ %s ] : [ %s ]" % (uuid_udp, ack_msg, udp_ip[0], udp_ip[1]))
            sock.sendto(ack_msg, udp_ip)

    except Exception as e:
        logger.error("exception udp_loop()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    finally:
        return 0

