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
########################################################################################################################
from __future__ import print_function
from Log import *
from Util import *
from Cloud_selector import *
from Device_selector import *
import sys
import time

if __name__ == '__main__':

    try:
        logger.info("Reading configuration")
        config_scrt = read_config ('config/Config_HAT.yaml')
        logger.info("Readed Script configuration")
        logger.info(config_scrt)
        config_cloud = read_config('config/Config_Cloud.yaml')
        logger.info("Readed Cloud configuration")
        logger.info(config_cloud)

        logger.info("Starting connection")
        connection = cloud_connector(config_cloud, config_scrt)
        logger.info("Started connection")

        device_init(config_scrt)

        logger.info("Starting Main LOOP")
        sec = config_scrt["sample"]
        logger.info(sec)
        logger.info("seconds")
        while True:

            #read status
            logger.info("LOOP reading device")
            status = device_read(config_scrt)
            logger.info("LOOP readed device")

            #act
            logger.info("LOOP tasking device")
            device_task(status,config_scrt)
            logger.info("LOOP end task device")

            #publis_status
            logger.info("LOOP publishing device")
            cloud_publish(connection, status, config_cloud, config_scrt)
            logger.info("LOOP published device")
            time.sleep(sec)

    except Exception as e:
        logger.error("exception main()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
		
		