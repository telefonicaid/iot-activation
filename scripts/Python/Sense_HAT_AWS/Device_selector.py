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
from Device_selector_HAT import *


"""
    Access the configuration to initialize the devices
    name: device_init(config_scrt)
    param: config_scrt [yaml]
    return: 0
"""
def device_init(config_scrt):

    if "Sense_HAT" in config_scrt:
        logger.info("DEVICE: selected Sense_HAT")
        device_init_HAT(config_scrt)

    return 0


"""
    Access the configuration to read the devices status
    name: device_read(config_scrt)
    param: config_scrt [yaml]
    return: status json
"""
def device_read(config_scrt):

    if "Sense_HAT" in config_scrt:
        logger.info("DEVICE: selected Sense_HAT")
        status = device_read_HAT(config_scrt)

    return status


"""
    Access the configuration to act on the devices
    name: device_task(status,config_scrt)
    param: status json
    param: config_scrt [yaml]
    return: 0 if OK
"""
def  device_task(status,config_scrt):

    task = 0

    if "Sense_HAT" in config_scrt:
        logger.info("DEVICE: selected Sense_HAT")
        task = device_task_HAT(status, config_scrt)

    return task

	