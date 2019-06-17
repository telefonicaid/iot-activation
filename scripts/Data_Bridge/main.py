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
from bridge import *
import time
import socket
import threading
import json
import random
import string

if __name__ == '__main__':

    try:

        logger.info("Reading configuration files")
        config_file = read_config('config/Configuration.yaml')
        logger.debug(config_file)
        config_cloud = cloud_configure(config_file)
        logger.debug(config_cloud)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((config_file["UDP"]["ip"], (config_file["UDP"]["port"])))

        while True:

            logger.info("################################# Waiting for a New Message #################################")

            udp_msg, udp_ip = sock.recvfrom(1024)
            logger.info("Message Received [ %s ] from [ %s ] : [ %s ]" % (udp_msg, udp_ip[0],udp_ip[1] ))

            response = bridge_routine(udp_msg, udp_ip[0],config_file, config_cloud)
            ack_msg = json.dumps(response)
            logger.info("Generate ACK payload [ %s ]" % response)

            logger.info("Sent MESSAGE [ %s ] to [ %s ] : [ %s ]" % (ack_msg, udp_ip[0], udp_ip[1]))
            sock.sendto(ack_msg, udp_ip)

    except Exception as e:
        logger.error("exception main()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

