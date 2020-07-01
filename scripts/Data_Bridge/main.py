#!/usr/bin/python
# ########################################################################################################################
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
from test import *
from server_coap import *
from server_udp import *
from health_check import *
import threading
import traceback

if __name__ == '__main__':

    try:
        config_file = read_config_file()
        logger.debug(config_file)
        config_cloud = cloud_configure(config_file)
        logger.debug(config_cloud)

        if config_file["cloudlog"]:
            cloud_log(config_cloud)

        if config_cloud["code"] == CODE_OK and test(config_file, config_cloud):

            if config_file["COAP"]["enable"]:
                thread_coap = threading.Thread(name='CoAPserver', target=coap_loop, args=(config_file, config_cloud))
                thread_coap.setDaemon(True)
                thread_coap.start()

            if config_file["UDP"]["enable"]:
                thread_udp = threading.Thread(name='UDP_socket', target=udp_loop, args=(config_file, config_cloud))
                thread_udp.setDaemon(True)
                thread_udp.start()

                thread_health = threading.Thread(name='healthtest', target=health_check)
                thread_health.start()
        else:
            logger.error("Failed tests")

    except Exception as e:
        logger.error("exception main()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    except (KeyboardInterrupt, SystemExit):
        logger.warning("KeyboardInterrupt main()")




