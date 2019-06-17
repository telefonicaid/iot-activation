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
import time
import boto3
import sys, os, base64, datetime, hashlib, hmac, urllib

CONST_TIME = 10

whait_ack = True
whait_cont = 0
ack_aws = {}


def cloud_publish_topic_default_aws(topic, status, config_cloud):

    region = config_cloud["region"]

    iot_data = boto3.client('iot-data',  region_name=region)
    response_publish = iot_data.publish(topic=topic,qos=0  ,payload=status)
    code = response_publish["ResponseMetadata"]["HTTPStatusCode"]

    logger.info("Publish Accepted code [ %s ]", code)

    ack_aws["code"] = CODE_MQTT_MSG_SENT
    ack_aws["msg"] = MSG_MQTT_MSG_SENT

    return ack_aws


def cloud_publish_in_shadow_aws(thing_name, status, config_cloud):

    region = config_cloud["region"]

    json_status = {}
    json_status['raw'] = status
    json_reported = {"state": {"reported": {}}}
    json_reported["state"]["reported"] = json_status
    msg_reported = json.dumps(json_reported)

    iot_data = boto3.client('iot-data', region_name=region)

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
        iot = boto3.client('iot', region_name=region)
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
    region = config_cloud["region"]

    iot_data = boto3.client('iot-data', region_name=region)
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
    region = config_cloud["region"]

    iot = boto3.client('iot', region_name=region)
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
    logger.debug("Selecting a AWS Option")

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
        logger.info("Select INVALID Option DEVICE [ %s ] CUSTOM TOPIC" % thing_name)
        logger.warning("try to publish in a AWS RESERVED TOPIC [ %s ]" % topic)
        response = {}
        response["code"] = CODE_ERROR_AWS_TOPIC_RESERVED
        response["msg"] = MSG_ERROR_AWS_TOPIC_RESERVED + topic

    return response


def cloud_get_parameter_aws(parameter_name, config_cloud):

    ssm = boto3.client(service_name='ssm', region_name=config_cloud["region"])
    json_parameter = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    parameter = json_parameter["Parameter"]["Value"]

    return parameter