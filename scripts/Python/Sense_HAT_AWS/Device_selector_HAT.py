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
from Util import *
import os
import json
from sense_hat import SenseHat

class Display:
    def __init__(self):
        self.val = ""
        self.R = 0
        self.G = 0
        self.B = 0

# RGB Colours
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Global
sense = SenseHat()
temperature = Display()  # type: Display
humidity = Display()
command = Display()
pressure = Display()
acceleration = Display()


"""
    PRIVATE: generates a json with colour and value structure
    name: device_task(status,config_scrt)
    param: valor text
    param: r,g,b colour
    return: json
"""
def get_struct(valor,r,g,b):
    col = {}
    col["r"] = r
    col["g"] = g
    col["b"] = b
    json = {}
    json["val"] = valor
    json["colour"] = col
    logger.info(json)
    return json


"""
    Access the configuration to initialize the Sense HAT
    name: device_task(status,config_scrt)
    param: config_scrt [yaml]
    return: 0 if OK
"""
def device_init_HAT(config_scrt):

    logger.info("DEVICE Sense HAT: Sense HAT initialised:")
    return 0


"""
    Access the configuration to read the Sense HAT status
    name: device_task(status,config_scrt)
    param: config_scrt [yaml]
    return: Sense HAT status status json
"""
def device_read_HAT(config_scrt):
    global temperature, humidity, command, pressure, acceleration#, sense

    logger.info("DEVICE Sense HAT: reading Sense_HAT:")

    status = {}
    logger.info(status)

    if "temperature" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["temperature"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - reading temperature:")
            temperature.val = sense.get_temperature()
            RGB = int((255 / (config_scrt["Sense_HAT"]["temperature"]["max"] - config_scrt["Sense_HAT"]["temperature"][
                "min"])) * ( temperature.val - config_scrt["Sense_HAT"]["temperature"]["min"]))
            temperature.R = RGB
            json_t = get_struct(temperature.val,temperature.R,temperature.G,temperature.B)
            status["temperature"] = json_t


    if "humidity" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["humidity"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - reading humidity:")
            humidity.val = sense.get_humidity()
            RGB = int((255 / (config_scrt["Sense_HAT"]["humidity"]["max"] - config_scrt["Sense_HAT"]["humidity"][
                "min"])) * ( humidity.val - config_scrt["Sense_HAT"]["humidity"]["min"]))
            humidity.B = RGB
            json_h = get_struct(humidity.val, humidity.R, humidity.G, humidity.B)
            status["humidity"] = json_h


    if "pressure" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["pressure"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - reading pressure:")
            pressure.val = sense.get_pressure()
            RGB = int((255.00 / (config_scrt["Sense_HAT"]["pressure"]["max"] - config_scrt["Sense_HAT"]["pressure"][
                "min"])) * ( pressure.val - config_scrt["Sense_HAT"]["pressure"]["min"]))
            pressure.G = RGB
            json_p = get_struct(pressure.val, pressure.R, pressure.G, pressure.B)
            status["pressure"] = json_p

    if "acceleration" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["acceleration"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - reading acceleration:")
            accel = sense.get_accelerometer_raw()
            acceleration.val = max((accel['x'],accel['y'],accel['z']))
            RGB = int((255 / (config_scrt["Sense_HAT"]["acceleration"]["max"] - config_scrt["Sense_HAT"]["acceleration"][
                "min"])) * ( acceleration.val - config_scrt["Sense_HAT"]["temperature"]["min"]))
            acceleration.G = RGB
            acceleration.B = RGB
            json_a = get_struct(acceleration.val, acceleration.R, acceleration.G, acceleration.B)
            status["acceleration"] = json_a


    if os.path.isfile('received.json'):
        with open('received.json') as file:
            json_delta = json.load(file)
        file.close()
        logger.info("DEVICE Sense HAT: - reading command:")
        logger.info(json_delta)
        if "val" in json_delta["state"]["command"]:
            command.val = json_delta["state"]["command"]["val"]
            logger.info("DEVICE Sense HAT:  - changed command")

        if "colour" in json_delta["state"]["command"]:
            if "r" in json_delta["state"]["command"]["colour"]:
                command.R = json_delta["state"]["command"]["colour"]["r"]
                logger.info("DEVICE Sense HAT:  - changed command colour Red")

            if "g" in json_delta["state"]["command"]["colour"]:
                command.G = json_delta["state"]["command"]["colour"]["g"]
                logger.info("DEVICE Sense HAT:  - changed command colour Green")

            if "b" in json_delta["state"]["command"]["colour"]:
                command.B = json_delta["state"]["command"]["colour"]["b"]
                logger.info("DEVICE Sense HAT:  - changed command colour Blue")

        json_c = get_struct(command.val, command.R, command.G, command.B)
        status["command"] = json_c
        logger.info("DEVICE Sense HAT: Received command:")

    logger.info(status)
    return status


"""
    Access the configuration to act on the Sense_HAT
    name: device_task_HAT(status, config_scrt)
    param: status json
    param: config_scrt [yaml]
    return: 0 if OK
"""
def device_task_HAT(status, config_scrt):

    if "temperature" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["temperature"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - display temperature:")
            sense.show_message(config_scrt["Sense_HAT"]["temperature"]["msg"] + str(int(temperature.val)) , text_colour=white , back_colour=(temperature.R , temperature.G , temperature.B))

    if "humidity" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["humidity"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - display humidity:")
            sense.show_message(config_scrt["Sense_HAT"]["humidity"]["msg"] + str(int(humidity.val)) , text_colour=white , back_colour=(humidity.R , humidity.G , humidity.B))

    if "pressure" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["pressure"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - display pressure:")
            sense.show_message(config_scrt["Sense_HAT"]["pressure"]["msg"] + str(int(pressure.val)) , text_colour=white , back_colour=(pressure.R , pressure.G , pressure.B))

    if "acceleration" in config_scrt["Sense_HAT"]:
        if config_scrt["Sense_HAT"]["acceleration"]["active"] == "ok":
            logger.info("DEVICE Sense HAT: - display acceleration:")
            sense.show_message(config_scrt["Sense_HAT"]["acceleration"]["msg"] + str(int(acceleration.val)) , text_colour=white , back_colour=(acceleration.R , acceleration.G , acceleration.B))

    logger.info("DEVICE Sense HAT: - display command:")
    sense.show_message(command.val, text_colour=white, back_colour=(command.R, command.G, command.B))

    return 0
