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
from utils import *
import json
import boto3
import sys
import os


def is_a_thing(thing_name, config_cloud):
    """
    Search the Thing in IoT-Core
    :param thing_name:
    :param config_cloud:
    :return: Boolean (True/False)
    """
    found = False
    try:
        search = True
        next_token = ""
        iot = boto3.client('iot', region_name=config_cloud["region"])
        while search:
            response_list_things = iot.list_things(nextToken=next_token, maxResults=50)
            for thing in response_list_things["things"]:
                if thing_name == thing["thingName"]:
                    search = False
                    found = True

            if "nextToken" in response_list_things:
                next_token = response_list_things["nextToken"]
            else:
                search = False
    except Exception as e:
        found = False
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return found


def cloud_create_new_thing_aws(thing_name, config_cloud):
    """
    Function to create a new Thing in IoT-Core
    :param thing_name:
    :param config_cloud:
    :return: {"code": 200, "msg": "OK"}
    """
    ack_create = {"code": 501, "msg": ""}
    try:
        iot = boto3.client('iot', region_name=config_cloud["region"])
        try:
            response_create = iot.create_thing(thingName=thing_name)
            code = response_create["ResponseMetadata"]["HTTPStatusCode"]
            if code == CODE_OK:
                ack_create = {"code": code, "msg": "NEW Thing Created OK"}
            else:
                ack_create = {"code": code, "msg": "NEW Thing Created ERROR"}
        except Exception as e:
            ack_create = {"code": 401, "msg": "AWS-IoT - Thing Not Created"}
            logger.error("message:{}".format(e.message))
            traceback.print_exc(file=sys.stdout)
    except Exception as e:
        ack_create = {"code": 401, "msg": "AWS-IoT - Access Error"}
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return ack_create


def cloud_get_shadow_raw_aws(thing_name, config_cloud):
    """
    Function to get the Thing Shadow form from the IoT-Core
    :param thing_name:
    :param config_cloud:
    :return: {"code": 200, "msg": Shadow}
    """
    ack_shadow = {"code": 501, "msg": ""}
    try:
        region = config_cloud["region"]
        iot_data = boto3.client('iot-data', region_name=region)
        try:
            response_shadow = iot_data.get_thing_shadow(thingName=thing_name)
            code = response_shadow["ResponseMetadata"]["HTTPStatusCode"]
            if code == CODE_OK:
                json_response = json.loads(response_shadow["payload"].read())
                shadow = ""
                if "delta" in json_response["state"]:
                    if "raw" in json_response["state"]["delta"]:
                        shadow = json_response["state"]["delta"]["raw"]
                ack_shadow = {"code": code, "msg": shadow}
            else:
                ack_shadow = {"code": code, "msg": "Get Shadow Error"}
        except Exception as e:
            ack_shadow = {"code": 401, "msg": "AWS-IoT-data - Shadow Not Gotten"}
            logger.error("message:{}".format(e.message))
            traceback.print_exc(file=sys.stdout)
    except Exception as e:
        ack_shadow = {"code": 401, "msg": "AWS-IoT-data - Access Error"}
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return ack_shadow


def cloud_get_shadow_aws(thing_name, config_cloud):
    """
    Function to get the Thing Shadow form from the IoT-Core
    :param thing_name:
    :param config_cloud:
    :return: {"code": 200, "msg": Shadow}
    """
    ack_shadow = {"code": 501, "msg": ""}
    try:
        region = config_cloud["region"]
        iot_data = boto3.client('iot-data', region_name=region)
        try:
            response_shadow = iot_data.get_thing_shadow(thingName=thing_name)
            code = response_shadow["ResponseMetadata"]["HTTPStatusCode"]
            if code == CODE_OK:
                json_response_full = json.loads(response_shadow["payload"].read())
                json_response = json_response_full["state"]
                shadow = json.dumps(json_response)
                ack_shadow = {"code": code, "msg": shadow}
            else:
                ack_shadow = {"code": code, "msg": "Get Shadow Error"}
        except Exception as e:
            ack_shadow = {"code": 401, "msg": "AWS-IoT-data - Shadow Not Gotten"}
            logger.error("message:{}".format(e.message))
            traceback.print_exc(file=sys.stdout)
    except Exception as e:
        ack_shadow = {"code": 401, "msg": "AWS-IoT-data - Access Error"}
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return ack_shadow


def cloud_publish_topic_aws(id, topic, status, config_cloud):
    """
    Function to publish in a topic
    :param topic:
    :param status:
    :param config_cloud:
    :return:  {"code": 200, "msg": "OK"}
    """
    ack_publish = {"code": 501, "msg": ""}
    try:
        iot_data = boto3.client('iot-data', region_name=config_cloud["region"])
        try:
            msg_reported = json.dumps(status)
            response_publish = iot_data.publish(topic=topic, qos=0, payload=msg_reported)
            code = response_publish["ResponseMetadata"]["HTTPStatusCode"]
            logger.info("%s - Publish Accepted code [ %s ]", id, code)
            if code == CODE_OK:
                ack_publish = {"code": code, "msg": "Publish Accepted"}
            else:
                ack_publish = {"code": code, "msg": "Publish Not Accepted "}
        except Exception as e:
            ack_publish = {"code": 401, "msg": "AWS IoT - Not Publish in topic: " + topic}
            logger.error("message:{}".format(e.message))
            traceback.print_exc(file=sys.stdout)
    except Exception as e:
        ack_publish = {"code": 401, "msg": "AWS IoT - Access Error"}
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    finally:
        return ack_publish


def cloud_publish_in_shadow_aws(id, thing_name, status, config_cloud):
    """
    Funtion for update a Thing Shadow in IoT-Core
    :param thing_name:
    :param status:
    :param config_cloud:
    :return: {"code": 200, "msg": Shadow}
    """
    json_reported = {"state": {"reported": status}}
    msg_reported = json.dumps(json_reported)
    region = config_cloud["region"]

    ack_publish = {"code": 501, "msg": "Publish in Shadow AWS - Internal Server Error"}
    try:
        iot_data = boto3.client('iot-data', region_name=region)
    except Exception as e:
        ack_publish = {"code": 401, "msg": "AWS-IoT-data - Access Error"}
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    else:
        if is_a_thing(thing_name, config_cloud):
            logger.info("%s - Get thing Shadow[ %s ] from AWS", id,  thing_name)
            shadow = cloud_get_shadow_raw_aws(thing_name, config_cloud)
            logger.info("%s - Thing Shadow received [ %s ] status code [ %s ]" % (id, shadow["msg"], shadow["code"]))
            if shadow["code"] == CODE_OK:
                try:
                    response_update = iot_data.update_thing_shadow(thingName=thing_name, payload=msg_reported)
                    code = response_update["ResponseMetadata"]["HTTPStatusCode"]
                    if code == CODE_OK:
                        ack_publish = {"code": code, "msg": shadow["msg"]}
                    else:
                        ack_publish = {"code": code, "msg": shadow["msg"]}
                except Exception as e:
                    ack_publish = {"code": 401, "msg": "AWS-IoT-data - Update Thing Access Error"}
                    logger.error("message:{}".format(e.message))
                    traceback.print_exc(file=sys.stdout)
            else:
                ack_publish = shadow
        else:  # is_a_thing(thing_name, config_cloud):
            try:  # Create New Thing
                logger.warning("%s - Thing not found. Created a NEW THING [ %s ]", id, thing_name)
                create_thing = cloud_create_new_thing_aws(thing_name, config_cloud)
                if create_thing["code"] == CODE_OK:
                    logger.info("%s - NEW Thing Created [ %s ] OK", id, thing_name)
                    topic_log = config_cloud["MQTT"]["topic"]["log_device"]
                    cloud_publish_topic_aws(id, topic_log, "Thing created: " + thing_name, config_cloud)

                    response_publish = iot_data.update_thing_shadow(thingName=thing_name, payload=msg_reported)
                    logger.debug("Publish in log topic [ %s ]", config_cloud["MQTT"]["topic"]["log_device"])

                    code = response_publish["ResponseMetadata"]["HTTPStatusCode"]
                    ack_publish = {"code": code, "msg": ""}
                else:
                    logger.error("%s - NEW Thing Created [ %s ] OK", id, thing_name)
                    ack_publish = create_thing

            except Exception as e:
                ack_publish = {"code": 401, "msg": "AWS IoT - Access Error"}
                logger.error("message:{}".format(e.message))
                traceback.print_exc(file=sys.stdout)

    finally:
        logger.info("%s - Update reported [ %s ] into shadow code [ %s ]" % (id, msg_reported, ack_publish["code"]))
        return ack_publish


def cloud_publish_aws(id, thing_name, topic, status, config_cloud):
    """
    Select the Option of Publishing:  Update Shadow, publish in a default o custom topic
    :param thing_name: the name of the device in AWS
    :param topic: topic name where you want to publish
    :param status: status received from device
    :param config_cloud:
    :return:
    """
    logger.debug("Selecting a AWS Option:")

    config_cloud["MQTT"]["topic"]["update"] = "$aws/things/<DEVICE_NAME>/shadow/update"
    config_cloud["MQTT"]["topic"]["reserved"] = "$aws"

    if topic == "":  # if the topic is not defined publish in a default topic
        logger.info("%s - Select Option 1: DEVICE [ %s ] and DEFAULT TOPIC", id, thing_name)
        topic_default = config_cloud["MQTT"]["topic"]["default"].replace('<DEVICE_NAME>', thing_name)
        logger.info("%s - Publish message [ %s ] into topic [ %s ] " % (id, status, topic_default))
        response = cloud_publish_topic_aws(id, topic_default, status, config_cloud)

    elif topic == config_cloud["MQTT"]["topic"]["update"].replace('<DEVICE_NAME>', thing_name):
        logger.info("%s - Select Option 3: DEVICE [ %s ] and CLOUD TOPIC", id, thing_name)
        logger.info("%s - Publish message [ %s ] into topic [ %s ] " % (id, status, topic))
        response = cloud_publish_in_shadow_aws(id, thing_name, status, config_cloud)

    elif topic[0:len(config_cloud["MQTT"]["topic"]["reserved"])] != config_cloud["MQTT"]["topic"]["reserved"]:
        logger.info("%s - Select Option 2: DEVICE [ %s ] CUSTOM TOPIC", id, thing_name)
        logger.info("%s - Publish message [ %s ] into topic [ %s ] " % (id, status, topic))
        response = cloud_publish_topic_aws(id, topic, status, config_cloud)

    else:
        logger.info("%s - Select INVALID Option DEVICE [ %s ] CUSTOM TOPIC", id, thing_name)
        logger.warning("%s - Try to publish in a AWS RESERVED TOPIC [ %s ]", id, topic)
        response = {"code": 401, "msg": 'ERROR: Try to publish in an unauthorized topic ' + topic}

    return response


def cloud_get_aws(id, thing_name, config_cloud):
    """
    Get the Shadow
    :param thing_name:
    :param config_cloud:
    :return: {"code": 200, "msg": Shadow}
    """
    ack_publish = {"code": 501, "msg": "Publish in Shadow AWS - Internal Server Error"}

    if is_a_thing(thing_name, config_cloud):
        logger.info("%s - Get thing Shadow[ %s ] from AWS", id, thing_name)
        shadow = cloud_get_shadow_aws(thing_name, config_cloud)
        logger.info("%s - Thing Shadow received [ %s ] status code [ %s ]", id, shadow["msg"], shadow["code"])
        ack_publish = shadow
    else:  # is_a_thing(thing_name, config_cloud):
        logger.warning("%s - Thing not found [ %s ]", id, thing_name)
        ack_publish = {"code": 404, "msg": "Thing not found."}

    return ack_publish


def cloud_get_parameter_aws(parameter_name, config_cloud):
    """
    Function for get parameters stored in SSM
    :param parameter_name:
    :param config_cloud:
    :return:
    """
    ack_parameter = {"code": 501, "msg": "Get parameter AWS - Internal Server Error"}
    try:
        ssm = boto3.client(service_name='ssm', region_name=config_cloud["region"])
    except Exception as e:
        ack_parameter = {"code": 500, "msg": "AWS-SSM: Error"}
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
    else:
        try:
            json_parameter = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
            ack_parameter = {"code": 200, "msg": json_parameter["Parameter"]["Value"]}
        except Exception as e:
            ack_parameter = {"code": 400, "msg": "AWS-SSM Parameter Denied: " + parameter_name}
            logger.error("AWS-SSM Parameter Denied: " + parameter_name)
            logger.error("message:{}".format(e.message))
            traceback.print_exc(file=sys.stdout)
    finally:
        return ack_parameter


def cloud_test_credentials_aws(config_file, config_cloud):
    """
    Function for test the credentials access
    :param config_file:
    :param config_cloud:
    :return: Boolean (True/False)
    """
    logger.info("Testing Cloud Credentials for AWS")
    test_ssm_ok = False
    status = True
    try:
        ssm = boto3.client(service_name='ssm', region_name=config_cloud["region"])
        ssm.get_parameter(Name=config_file["KITE"]["certificate"], WithDecryption=True)
        logger.info("Permissions required for: Get SSM Parameter [ %s ] OK", config_file["KITE"]["certificate"])
        ssm.get_parameter(Name=config_file["KITE"]["private_key"], WithDecryption=True)
        logger.info("Permissions required for: Get SSM Parameter [ %s ] OK", config_file["KITE"]["private_key"])
        test_ssm_ok = True

        iot = boto3.client('iot', region_name=config_cloud["region"])

        test_thing_name = "test_data_bridge_credentials"
        response_create = iot.create_thing(thingName=test_thing_name)
        if response_create["ResponseMetadata"]["HTTPStatusCode"] == CODE_OK:
            logger.info("Permissions required for: CREATE thing OK")
        else:
            status = False
            logger.error("Permissions required for: CREATE thing KO")

        iot_data = boto3.client('iot-data', region_name=config_cloud["region"])

        test_msg = "test message"
        test_json_reported = {"state": {"reported": {"msg": test_msg}}}
        test_msg_reported = json.dumps(test_json_reported)
        response_publish_shadow = iot_data.update_thing_shadow(thingName=test_thing_name, payload=test_msg_reported)
        if response_publish_shadow["ResponseMetadata"]["HTTPStatusCode"] == CODE_OK:
            logger.info("Permissions required for: Publish in SHADOW OK")
        else:
            status = False
            logger.error("Permissions required for: Publish in SHADOW KO")

        response_get_shadow = iot_data.get_thing_shadow(thingName=test_thing_name)
        # test_msg_shadow = response_get_shadow["payload"].read().decode("utf-8")
        if response_get_shadow["ResponseMetadata"]["HTTPStatusCode"] == CODE_OK:
            logger.info("Permissions required for: Get the SHADOW OK")
        else:
            status = False
            logger.error("Permissions required for: Get the SHADOW KO")

        test_topic = "databridge/test"
        response_publish = iot_data.publish(topic=test_topic, qos=0, payload=test_msg)
        if response_publish["ResponseMetadata"]["HTTPStatusCode"] == CODE_OK:
            logger.info("Permissions required for: Publish in a TOPIC OK")
        else:
            status = False
            logger.error("Permissions required for: Publish in a TOPIC KO")

        response_delete = iot.delete_thing(thingName=test_thing_name)
        if response_delete["ResponseMetadata"]["HTTPStatusCode"] == CODE_OK:
            logger.info("Permissions required for: DELETE thing OK")
        else:
            status = False
            logger.info("Permissions required for: DELETE thing KO")

    except Exception as e:
        if not test_ssm_ok:
            logger.error("Insufficient permissions in AWS for SSM")
        else:
            logger.error("Insufficient permissions in AWS for IoT-Core")

        logger.error("CLOUD: exception cloud_test_credentials_aws()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
        status = False

    finally:
        return status


def cloud_test_credentials_environment_aws():
    """
    Function for check the AWS credentials as environment variables
    :return: Boolean (True/False)
    """
    if "AWS_ACCESS_KEY_ID" in os.environ:
        logger.debug("Found 'AWS_ACCESS_KEY_ID' in environment variable")
        flag_test_cloud_id = True
    else:
        logger.debug("Not found 'AWS_ACCESS_KEY_ID' in environment variable")
        os.environ["AWS_ACCESS_KEY_ID"] = raw_input("What is your AWS Access key ID? ")
        flag_test_cloud_id = True

    if "AWS_SECRET_ACCESS_KEY" in os.environ:
        logger.debug("Found 'AWS_SECRET_ACCESS_KEY' in environment variable")
        flag_test_cloud_key = True
    else:
        logger.debug("Not found 'AWS_SECRET_ACCESS_KEY' in environment variable")
        os.environ["AWS_SECRET_ACCESS_KEY"] = raw_input("What is your AWS Secret access key? ")
        flag_test_cloud_key = True

    return flag_test_cloud_id and flag_test_cloud_key


def cloud_test_credentials_file_aws():
    aws_access_key_id = raw_input("What is your AWS Access key ID? ")
    aws_secret_access_key = raw_input("What is your AWS Secret access key? ")

    if "HOME" in os.environ:
        path = os.environ["HOME"]
    else:
        path = "/home/ec2-user"

    file_name = path + "/.aws/credentials"
    flag_file = False

    with open(file_name, "w") as f:
        f.writelines("[default]\n")
        f.writelines("aws_access_key_id = " + aws_access_key_id + "\n")
        f.writelines("aws_secret_access_key = " + aws_secret_access_key + "\n")
        flag_file = True

    return flag_file


def cloud_test_aws(config_file, config_cloud):

    test = cloud_test_credentials_aws(config_file, config_cloud)

    while not test:
        logger.error("credentials tested in AWS")
        test = cloud_test_credentials_file_aws()

    return test

