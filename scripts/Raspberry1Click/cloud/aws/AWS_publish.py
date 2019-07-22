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
from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import sys, traceback
import json
import ssl
import yaml
import time

def on_message(mqttc, userdata, message):
    data_delta = str(message.payload.decode("utf-8"))
    json_delta = json.loads(data_delta)
    print("Received message:")
    print(data_delta)
    return 0

def ssl_alpn_AWS(config_cloud):
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols(["x-amzn-mqtt-ca"])
        ca = "cert/AmazonRootCA1.pem"
        cert = "cert/certificate_pem.pem.crt"
        private = "cert/PrivateKey.pem.key"
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)
        print("ssl context created:")
        return ssl_context

    except Exception as e:
        traceback.print_exc(file=sys.stdout)


def cloud_connector_AWS(config_cloud):
    try:
        mqttc = mqtt.Client()
        ssl_context = ssl_alpn_AWS(config_cloud)
        mqttc.tls_set_context(context=ssl_context)
        broker = config_cloud["broker"]
        mqttc.connect(broker, port=8883)

        # Assign event callbacks
        mqttc.on_message = on_message

        # Subscribe to topic


        # Start
        mqttc.loop_start()
        print("MQTT broker connected:")

        return mqttc

    except Exception as e:
        traceback.print_exc(file=sys.stdout)

if __name__== "__main__":
    try:

        with open('AWS_configuration.yaml', 'r') as f:
            config_cloud = yaml.load(f)
        f.close()
        sense = SenseHat()
        connection = cloud_connector_AWS(config_cloud)

        json_reported = {"state": {"reported": {}}}
        json_reported["state"]["reported"] = {}

        while True:

            json_reported["state"]["reported"]["temperature"] = sense.get_temperature()
            json_reported["state"]["reported"]["humidity"] = sense.get_humidity()
            json_reported["state"]["reported"]["pressure"] = sense.get_pressure()
            json_reported["state"]["reported"]["accelerometer"] = sense.get_accelerometer_raw()
            json_reported["state"]["reported"]["orientation"] = sense.get_orientation()
            json_reported["state"]["reported"]["compass"] = sense.get_compass()

            msg_reported = json.dumps(json_reported)
            topic = "$aws/things/" + config_cloud["thing"] + "/shadow/update"
            connection.publish(topic, msg_reported)
            print("msg published:")
            time.sleep(20)

    except Exception as e:
        traceback.print_exc(file=sys.stdout)

