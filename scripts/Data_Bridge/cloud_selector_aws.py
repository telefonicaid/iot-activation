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
import json
import ssl
import time
import httplib
import requests
import paho.mqtt.client as mqtt
import boto3

import sys, os, base64, datetime, hashlib, hmac, urllib

CONST_TIME = 10

whait_ack = True
whait_cont = 0
ack_aws = {}


def on_message(mqttc, userdata, message):
    """ Callback default

    :param mqttc:
    :param userdata:
    :param message:
    :return: zero
    """
    global whait_ack
    logger.debug("CLOUD AWS: Received message:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!****")
    whait_ack = False
    return 0


def on_message_delta(mqttc, userdata, message):
    """ Callback for delta topic

    :param mqttc:
    :param userdata:
    :param message:
    :return: zero
    """
    logger.debug("CLOUD AWS: Received msg::!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Delta")
    return 0


def on_message_accepted(mqttc, userdata, message):
    """ Callback for accepted topic

    load the error code and msg in the ack global variable
    ack_aws["code"] = CODE_MQTT_ACCEPTED
    CODE_MQTT_ACCEPTED = '200'

    :param mqttc:
    :param userdata:
    :param message:
    :return: zero
    """
    global whait_ack, ack_aws
    logger.debug("CLOUD AWS: Received msg: Update Accepted:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Accepted")
    whait_ack = False
    ack_aws["code"] = CODE_MQTT_ACCEPTED
    ack_aws["msg"] = MSG_MQTT_ACCEPTED

    return 0


def on_message_rejected(mqttc, userdata, message):
    """ Callback for rejected topic

    load the error code and msg in the ack global variable
    ack_aws["code"] = CODE_MQTT_REJECTED
    CODE_MQTT_REJECTED = '400'
    ack_aws["val"] = msg error from AWS broker

    :param mqttc:
    :param userdata:
    :param message:
    :return: zero
    """
    global whait_ack, ack_aws
    logger.debug("CLOUD AWS: Received msg: Update Rejected:!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!Rejected")
    msg_topic = str(message.payload.decode("utf-8"))
    data_topic = json.loads(msg_topic)
    whait_ack = False
    ack_aws["code"] = CODE_MQTT_REJECTED  # data_topic["code"]
    ack_aws["msg"] = data_topic["message"]
    return 0


def ssl_alpn_aws(config_cloud):
    """ create a ssl context for AWS

    :param config_cloud: dictionary with the cloud configuracion (Configuration_AWS.yaml)
    :return: ssl context
    """
    try:
        # debug print opne ssl version
        logger.debug("CLOUD AWS: open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ca = config_cloud["SSL"]["path"] + config_cloud["SSL"]["ca"]
        cert = config_cloud["SSL"]["path"] + config_cloud["SSL"]["certificate"]
        private = config_cloud["SSL"]["path"] + config_cloud["SSL"]["private_key"]
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)
        logger.debug("CLOUD AWS: Created SSL context SUCCESS")

        return ssl_context

    except Exception as e:
        logger.error("exception ssl_alpn()")
        raise e


def cloud_connector_MQTT_aws(config_cloud):
    """ Connect to AWS via MQTT and subscribe to topics.

    :param config_cloud: configuration cloud
    :return:
    """
    try:
        logger.debug("CLOUD AWS: Connecting with AWS")
        mqttc = mqtt.Client()
        ssl_context = ssl_alpn_aws(config_cloud)
        mqttc.tls_set_context(context=ssl_context)
        logger.debug("CLOUD AWS: Context SSL SUCCESS")
        mqttc.connect(config_cloud["MQTT"]["broker"], port=config_cloud["MQTT"]["port"])
        logger.debug("CLOUD AWS: Connected to MQTT SUCCESS")

        logger.debug("CLOUD AWS: connected to AWS SUCCESS")
        return mqttc

    except Exception as e:
        logger.error("exception connector_AWS()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))


def cloud_publish_topic_update_MQTT_aws(thing_name, topic, status, config_cloud):
    """ Access AWS to publish in the update topic.

    :param thing: thing name
    :param topic: topic name
    :param status: device status
    :param config_cloud: configuration cloud
    :return: ack with the output
    """
    try:
        global whait_ack, whait_cont, ack_aws
        whait_ack = True
        whait_cont = 0
        ack_aws = {}

        logger.debug("CLOUD AWS: publishing in AWS")
        json_reported = {"state": {"reported": {}}}
        # json_status = json.loads(status)
        json_status = {}
        json_status['raw'] = status
        json_reported["state"]["reported"] = json_status
        msg_reported = json.dumps(json_reported)
        logger.debug("CLOUD AWS: Publish in topic: [ %s ]" % topic)
        logger.debug("CLOUD AWS: - msg: [%s]" % msg_reported)

        connection = cloud_connector_MQTT_aws(config_cloud)

        # Assign event callbacks
        connection.message_callback_add(config_cloud["MQTT"]["topic"]["accepted"].replace('<DEVICE_NAME>', thing_name),
                                        on_message_accepted)
        connection.message_callback_add(config_cloud["MQTT"]["topic"]["rejected"].replace('<DEVICE_NAME>', thing_name),
                                        on_message_rejected)
        connection.message_callback_add(config_cloud["MQTT"]["topic"]["delta"].replace('<DEVICE_NAME>', thing_name),
                                        on_message_delta)
        connection.on_message = on_message

        # subscribe to topic
        connection.subscribe(config_cloud["MQTT"]["topic"]["accepted"].replace('<DEVICE_NAME>', thing_name))
        connection.subscribe(config_cloud["MQTT"]["topic"]["rejected"].replace('<DEVICE_NAME>', thing_name))
        connection.subscribe(config_cloud["MQTT"]["topic"]["delta"].replace('<DEVICE_NAME>', thing_name))
        logger.debug("CLOUD AWS: Subscribed topic: accepted")
        logger.debug("CLOUD AWS: Subscribed topic: rejected")

        # Start
        connection.loop_start()

        time.sleep(1)  # you need to wait for the subscription. If not, the first subscription callback fails.
        connection.publish(topic, msg_reported)

        logger.debug("CLOUD AWS: Published in AWS")

        while whait_ack and whait_cont < CONST_TIME:
            logger.debug(whait_cont)
            time.sleep(1)
            whait_cont += 1

        if whait_cont == CONST_TIME:
            ack_aws["code"] = CODE_MQTT_TIME_OUT
            ack_aws["msg"] = CODE_MQTT_TIME_OUT

        shadow = cloud_get_shadow_aws(thing_name, config_cloud)

        if shadow["code"] == 200:
            ack_aws["msg"] = shadow["msg"]

        connection.disconnect()
        whait_cont = 0
        whait_ack = True

        return ack_aws

    except Exception as e:
        logger.error("exception cloud_publish_update_aws()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)


def cloud_publish_topic_default_MQTT_aws(topic, status, config_cloud):
    """ Access AWS to publish in a topic.

    :param thing_name: thing name
    :param topic: topic name
    :param status: device status
    :param config_cloud: configuration cloud
    :return:
    """

    try:
        logger.debug("CLOUD AWS: publishing in a topic")
        logger.debug("CLOUD AWS: Publish in topic: [ %s ]" % topic)
        logger.debug("CLOUD AWS: - msg: [%s]" % status)

        connection = cloud_connector_MQTT_aws(config_cloud)
        # Start
        connection.loop_start()
        time.sleep(1)
        connection.publish(topic, status)

        logger.debug("CLOUD AWS: Published in AWS")
        connection.disconnect()

        ack_aws["code"] = CODE_MQTT_MSG_SENT
        ack_aws["msg"] = MSG_MQTT_MSG_SENT

        return ack_aws

    except Exception as e:
        logger.error("exception cloud_publish_default_aws()")
        logger.error("e obj:{}".format(vars(e)))
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    return 0


def cloud_publish_topic_default_aws(topic, status, config_cloud):
    access_key = config_cloud["IAM_user"]["access_key"]
    secret_key = config_cloud["IAM_user"]["secret_key"]
    region = config_cloud["region"]

    iot_data = boto3.client('iot-data', aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key, region_name=region)

    response_publish = iot_data.publish(topic=topic,qos=0  ,payload=status)

    code = response_publish["ResponseMetadata"]["HTTPStatusCode"]

    logger.info("Publish Accepted code [ %s ]", code)

    ack_aws["code"] = CODE_MQTT_MSG_SENT
    ack_aws["msg"] = MSG_MQTT_MSG_SENT

    return ack_aws


def cloud_publish_in_shadow_aws(thing_name, status, config_cloud):
    access_key = config_cloud["IAM_user"]["access_key"]
    secret_key = config_cloud["IAM_user"]["secret_key"]
    region = config_cloud["region"]

    json_status = {}
    json_status['raw'] = status
    json_reported = {"state": {"reported": {}}}
    json_reported["state"]["reported"] = json_status
    msg_reported = json.dumps(json_reported)

    iot_data = boto3.client('iot-data', aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key, region_name=region)


    try:
        shadow_desired = ""
        logger.info("Get thing [ %s ] from AWS" % thing_name)
        response_shadow = iot_data.get_thing_shadow(thingName=thing_name)
        msg_shadow = response_shadow["payload"].read().decode("utf-8")
        json_shadow = json.loads(msg_shadow)
        if "desired" in json_shadow["state"]:
            if "raw" in json_shadow["state"]["desired"]:
                shadow_desired = json_shadow["state"]["desired"]["raw"]
        code = response_shadow["ResponseMetadata"]["HTTPStatusCode"]

    except:
        logger.warning("Shadow not found. Created a NEW THING [ %s ]" % thing_name)
        iot = boto3.client('iot', aws_access_key_id=access_key,
                           aws_secret_access_key=secret_key, region_name=region)
        response_create = iot.create_thing(thingName=thing_name)
        code = response_create["ResponseMetadata"]["HTTPStatusCode"]

        cloud_publish_topic_default_aws(config_cloud["MQTT"]["topic"]["log_device"], "Thing created "+thing_name, config_cloud)

    logger.info("Thing Shadow received [ %s ] status code [ %s ]" % (shadow_desired, code))

    response_publish = iot_data.update_thing_shadow(thingName=thing_name, payload=msg_reported)

    update = {}
    update["code"] = response_publish["ResponseMetadata"]["HTTPStatusCode"]

    logger.info("Update reported [ %s ] into shadow cod [ %s ]" % (msg_reported, update["code"]))

    logger.debug("Update Accepted code [ %s ]" % update["code"])
    update["msg"] = shadow_desired

    return update


def cloud_get_shadow_aws(thing_name, config_cloud):
    """ Access AWS to get the thing's shadow.

    :param broker:
    :param thing_name:
    :param config_cloud:
    :return: shadow
    """
    access_key = config_cloud["IAM_user"]["access_key"]
    secret_key = config_cloud["IAM_user"]["secret_key"]
    region = config_cloud["region"]

    iot_data = boto3.client('iot-data', aws_access_key_id=access_key,
                            aws_secret_access_key=secret_key, region_name=region)

    response = iot_data.get_thing_shadow(thingName=thing_name);

    shadow = {}
    shadow["code"] = response["ResponseMetadata"]["HTTPStatusCode"]
    logger.debug("CLOUD AWS: get Shadow code [ %s ]" % shadow["code"])

    if shadow["code"] == 200:
        json_response = json.loads(response["payload"].read())
        if "delta" in json_response["state"]:
            if "raw" in json_response["state"]["delta"]:
                shadow["msg"] = json_response["state"]["delta"]["raw"]
            else:
                shadow["msg"] = ""
        else:
            shadow["msg"] = ""
        logger.debug("CLOUD AWS: Shadow in AWS [ %s ]" % shadow["msg"])
    else:
        shadow["msg"] = "ERROR: no get Shadow"
        logger.debug("CLOUD AWS: Shadow in AWS [ %s ]" % shadow["msg"])

    return shadow


def cloud_create_new_thing_aws(thing_name, config_cloud):
    """ coming soon..

    :param thing_name:
    :param config_cloud:
    :return:
    """

    access_key = config_cloud["IAM_user"]["access_key"]
    secret_key = config_cloud["IAM_user"]["secret_key"]
    region = config_cloud["region"]

    iot = boto3.client('iot', aws_access_key_id=access_key,
                       aws_secret_access_key=secret_key, region_name=region)

    response = iot.create_thing(thingName=thing_name)

    return True


def cloud_publish_aws(thing_name, topic, status, config_cloud):
    """ Select type of Publishing,  update topic, default topic o custom topic

    :param thing_name: the name of the device in AWS
    :param topic: topic name where you want to publish
    :param status: status received from device
    :param config_cloud:
    :return:
    """
    if topic == "":  # if the topic is not defined publish y a default topic
        logger.info("Select Option 1: DEVICE [ %s ] and DEFAULT TOPIC" % thing_name)
        topic_default = config_cloud["MQTT"]["topic"]["default"].replace('<DEVICE_NAME>', thing_name)
        logger.info("Publish message [ %s ] into topic [ %s ] " % (status, topic_default))
        response = cloud_publish_topic_default_aws(topic_default, status, config_cloud)

    elif topic == config_cloud["MQTT"]["topic"]["update"].replace('<DEVICE_NAME>', thing_name):
        logger.info("Select Option 3: DEVICE [ %s ] and CLOUD TOPIC" % thing_name)
        logger.info("Publish message [ %s ] into topic [ %s ] " % (status, topic))
        response = cloud_publish_in_shadow_aws(thing_name, status, config_cloud)

    elif topic[0:len(config_cloud["MQTT"]["topic"]["reserved"])] != config_cloud["MQTT"]["topic"]["reserved"]:
        logger.info("Select Option 2: DEVICE [ %s ] CUSTOM TOPIC" % thing_name)
        logger.info("Publish message [ %s ] into topic [ %s ] " % (status, topic))
        response = cloud_publish_topic_default_aws(topic, status, config_cloud)

    else:
        logger.info("Select Option 2: DEVICE [ %s ] CUSTOM TOPIC" % thing_name)
        logger.error("try to publish in a AWS RESERVED TOPIC [ %s ]" % topic)
        response = {}
        response["code"] = CODE_ERROR_AWS_TOPIC_RESERVED
        response["msg"] = MSG_ERROR_AWS_TOPIC_RESERVED + topic

    return response

