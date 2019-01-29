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

import time
import socket
import json
import logging
import sys


# Setting log
import traceback

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)
logger.info("Setting log")


config_ip='0.0.0.0'
config_port= 4114

if __name__ == '__main__':

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((config_ip,config_port))
        ack = {"ack": "OK"}

        while True:

            logger.info("#############################################################################################")
            logger.info("###################################### LOOP  listening ######################################")
            logger.info("#############################################################################################")

            udp_msg, udp_ip = sock.recvfrom(1024)
            logger.info("Received message[ %s ] from [ %s ]" % (udp_msg, udp_ip[0]))


            ack_msg = json.dumps(ack)
            logger.info("Sending ACK [ %s ]" % ack_msg)


            logger.info("Sending message[ %s ] to [ %s:%s ]" % (ack_msg, udp_ip[0], udp_ip[1]))
            sock.sendto(ack_msg,udp_ip)

            logger.info("ACK sent.")

    except Exception as e:
        logger.error("exception main()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)


