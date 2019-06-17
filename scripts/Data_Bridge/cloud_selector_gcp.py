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
import datetime
import jwt
import requests
import json
import base64
import io
from googleapiclient import discovery
from google.oauth2 import service_account


def create_jwt(config_cloud):
    token = {
        # The time the token was issued.
        'iat': datetime.datetime.utcnow(),
        # Token expiration time.
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        # The audience field should always be set to the GCP project id.
        'aud': config_cloud["project_id"]
    }

    # Read the private key file.
    with open(config_cloud["path"]+config_cloud["private_key_file"], 'r') as f:
        private_key = f.read()

    return jwt.encode(token, private_key, algorithm=config_cloud["algorithm"]).decode('ascii')


def get_client(config_cloud):
    """Returns an authorized API client by discovering the IoT API and creating
    a service object using the service account credentials JSON."""
    api_scopes = ['https://www.googleapis.com/auth/cloud-platform']
    api_version = 'v1'
    discovery_api = 'https://cloudiot.googleapis.com/$discovery/rest'
    service_name = 'cloudiotcore'

    credentials = service_account.Credentials.from_service_account_file(
        config_cloud["path"]+config_cloud["service_account_json"])
    scoped_credentials = credentials.with_scopes(api_scopes)

    discovery_url = '{}?version={}'.format(
        discovery_api, api_version)

    return discovery.build(
        service_name,
        api_version,
        discoveryServiceUrl=discovery_url,
        credentials=scoped_credentials, cache_discovery=False)


def find_registry(registry_name, config_cloud):

    registry_path = 'projects/{}/locations/{}'.format(
        config_cloud["project_id"], config_cloud["cloud_region"])

    client = get_client(config_cloud)

    registries = client.projects().locations().registries().list(
        parent=registry_path).execute().get('deviceRegistries', [])

    found = False
    for registry in registries:
        if registry.get('id') == registry_name:
            found = True

    return found


def create_registry(registry_name, topic, config_cloud):
    client = get_client(config_cloud)
    registry_parent = 'projects/{}/locations/{}'.format(
        config_cloud["project_id"], config_cloud["cloud_region"])
    body = {
        'eventNotificationConfigs': [{
            'pubsubTopicName': "projects/{}/topics/{}".format(config_cloud["project_id"],topic)
        }],
        'id': registry_name
    }
    request = client.projects().locations().registries().create(
        parent=registry_parent, body=body)

    response = request.execute()

    return response


def find_thing(thing_name, config_cloud):
    registry_path = 'projects/{}/locations/{}/registries/{}'.format(
        config_cloud["project_id"], config_cloud["cloud_region"], config_cloud["registry_id"])

    client = get_client(config_cloud)

    devices = client.projects().locations().registries().devices().list(parent=registry_path).execute().get('devices', [])

    found = False
    for device in devices:
        if device["id"] == thing_name:
            found = True

    return found


def create_thing(thing_name,config_cloud):
    registry_name = 'projects/{}/locations/{}/registries/{}'.format(
        config_cloud["project_id"], config_cloud["cloud_region"], config_cloud["registry_id"])

    client = get_client(config_cloud)
    with io.open(config_cloud["path"]+config_cloud["public_key_file"]) as f:
        certificate = f.read()

    # Note: You can have multiple credentials associated with a device.
    device_template = {
        'id': thing_name,
        'credentials': [{
            'publicKey': {
                'format': 'RSA_PEM',
                'key': certificate
            }
        }]
    }

    devices = client.projects().locations().registries().devices()
    res = devices.create(parent=registry_name, body=device_template).execute()

    return res


def publish_message(thing_name, status, config_cloud, jwt_token):
    headers = {
        'authorization': 'Bearer {}'.format(jwt_token),
        'content-type': 'application/json',
        'cache-control': 'no-cache'
    }

    # Publish to the events or state topic based on the flag.
    url_suffix = 'publishEvent' if config_cloud["message_type"] == 'event' else 'setState'

    publish_url = (
        '{}/projects/{}/locations/{}/registries/{}/devices/{}:{}').format(
        config_cloud["base_url"], config_cloud["project_id"], config_cloud["cloud_region"], config_cloud["registry_id"], thing_name,
        url_suffix)

    msg_bytes = base64.urlsafe_b64encode(status.encode('utf-8'))

    body = None
    if config_cloud["message_type"] == 'event':
        body = {'binary_data': msg_bytes.decode('ascii')}
    else:
        body = {
            'state': {'binary_data': msg_bytes.decode('ascii')}
        }

    resp = requests.post(publish_url, data=json.dumps(body), headers=headers, verify=False)

    ack_gcp = {}
    ack_gcp["code"] = resp.status_code
    ack_gcp["msg"] = ""

    if resp.status_code != 200:
        print('Response came back {}, retrying'.format(resp.status_code))
        ack_gcp["msg"] = "Not OK GCP response: {}".format(resp.status_code)
        logger.error(ack_gcp["msg"])

    return ack_gcp


def get_config(thing_name, config_cloud, jwt_token):

    headers = {
            'authorization': 'Bearer {}'.format(jwt_token),
            'content-type': 'application/json',
            'cache-control': 'no-cache'
    }

    base_path = '{}/projects/{}/locations/{}/registries/{}/devices/{}/'
    template = base_path + 'config?local_version={}'
    config_url = template.format(
        config_cloud["base_url"], config_cloud["project_id"], config_cloud["cloud_region"], config_cloud["registry_id"], thing_name, 1)

    resp = requests.get(config_url, headers=headers, verify=False)

    return resp


def callback(message_future):
    # When timeout is unspecified, the exception method waits indefinitely.
    if message_future.exception(timeout=30):
        print('Publishing message on {} threw an Exception {}.'.format(
            "topic", message_future.exception()))
    else:
        print(message_future.result())


def cloud_publish_topic_default_gcp(thing_name, status, config_cloud):

    jwt_token = create_jwt(config_cloud)

    if not find_registry(config_cloud["registry_id"], config_cloud):
        logger.warning("Registry not found. Created a NEW REGISTRY [ %s ]" % config_cloud["registry_id"])
        create_registry(config_cloud["registry_id"], "prueba", config_cloud)

    if not find_thing(thing_name, config_cloud):

        create_thing(thing_name, config_cloud)
        logger.warning("Device not found. Created a NEW THING [ %s ]" % thing_name)

    response_publish = publish_message(thing_name, status, config_cloud, jwt_token)

    response_config = get_config(thing_name, config_cloud, jwt_token)

    msg = ""
    if response_config.status_code == 200:
        logger.debug("response_config OK")
        msg_text = response_config.text
        msg_json = json.loads(msg_text)
        if "binaryData" in msg_json:
            msg_binary = msg_json["binaryData"]
            msg = base64.decodestring(msg_binary)

    return {"code": response_publish["code"], "msg": msg}


def cloud_publish_gcp(thing_name, topic_name, status, config_cloud):
    """ Select type of Publishing,  update topic, default topic o custom topic

    :param thing_name: the name of the device in AWS
    :param topic: topic name where you want to publish
    :param status: status received from device
    :param config_cloud:
    :return:
    """
    logger.debug("Selecting a AWS Option")

    if thing_name != "":  # if the topic is not defined publish y a default topic
        logger.info("Select Option 1: DEVICE [ %s ] and DEFAULT TOPIC" % thing_name)
        response = cloud_publish_topic_default_gcp(thing_name, status, config_cloud)
    else:
        logger.info("Select INVALID Option DEVICE [ %s ] " % thing_name)
        response = {"code": 000, "msg": "xxxxx"}

    return response

