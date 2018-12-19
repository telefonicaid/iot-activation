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
import json
import ssl
import paho.mqtt.client as mqtt


"""
    Generate a file with the message from subscribed topic
    name: on_message(mqttc, userdata, message):
    return: 0
"""
def on_message(mqttc, userdata, message):
    data_delta = str(message.payload.decode("utf-8"))
    json_delta = json.loads(data_delta)
    logger.info("CLOUD AWS: Received message:")
    logger.info(data_delta)
    # save the in a file ????????????????????????????
    f = open('received.json', 'wb')
    f.write(data_delta)

    return 0


"""
    Access the configuration to connect with AWS and create a mwtt client
    name: cloud_connector_AWS(config_cloud)
    param: config_cloud [yaml]
    return: mqtt for publish in it
"""
def ssl_alpn_AWS(config_cloud):
    try:
        # debug print opne ssl version
        logger.info("CLOUD AWS: open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ca = config_cloud["Certificate"]["path"] + config_cloud["Certificate"]["ca"]
        cert = config_cloud["Certificate"]["path"] + config_cloud["Certificate"]["certificate"]
        private = config_cloud["Certificate"]["path"] + config_cloud["Certificate"]["private_key"]
        logger.info("CLOUD AWS: Using Files:")
        logger.info(ca)
        logger.info(cert)
        logger.info(private)
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)
        logger.info("CLOUD AWS: Created SSL context SUCCESS")

        return ssl_context

    except Exception as e:
        logger.error("exception ssl_alpn()")
        raise e



"""
    Access the configuration to connect with AWS and create a mwtt client
    name: cloud_connector_AWS(config_cloud)
    param: config_cloud [yaml]
    return: mqtt for publish in it
"""
def cloud_connector_AWS(config_cloud):
    try:
        logger.info("CLOUD AWS: Connecting with AWS")
        mqttc = mqtt.Client()
        ssl_context = ssl_alpn_AWS(config_cloud)
        mqttc.tls_set_context(context=ssl_context)
        logger.info("CLOUD AWS: Connected with SSL SUCCESS")
        mqttc.connect(config_cloud["broker"], port=config_cloud["port"])
        logger.info("CLOUD AWS: Connected to MQTT SUCCESS")

        # Assign event callbacks
        mqttc.on_message = on_message

        # Subscribe to topic
        mqttc.subscribe(config_cloud["topic"]["delta"])
        logger.info("CLOUD AWS: Subscribed topic: Delta")

        # Start
        mqttc.loop_start()

        logger.info("CLOUD AWS: connected to AWS SUCCESS")
        return mqttc

    except Exception as e:
        logger.error("exception connector_AWS()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)



"""
    Access the configuration to publish the status device in AWS
    name: cloud_publish_AWS(connection,status,config_cloud)
    param: connection to publish
    param: status to publish
    param: config_cloud [yaml]
    return: 0 if OK
"""
def cloud_publish_AWS(connection, status, config_cloud):
    try:
        logger.info("CLOUD AWS: publishing in AWS")
        json_reported = {"state": {"reported": {}}}
        logger.info(json_reported)
        json_reported["state"]["reported"] = status
        msg_reported = json.dumps(json_reported)
        logger.info(msg_reported)
        logger.info(config_cloud["connection"]["topic"]["update"])

        connection.publish(config_cloud["connection"]["topic"]["update"], msg_reported)

        logger.info("CLOUD AWS: Publish reported in AWS")
        logger.info(msg_reported)

        return 0

    except Exception as e:
        logger.error("exception cloud_publish_AWS()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))

		