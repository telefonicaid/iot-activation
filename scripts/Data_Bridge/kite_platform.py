########################################################################################################################
#                                                                                                                      #
# MIT License                                                                                                          #
#                                                                                                                      #
# Copyright (c) 2018 Telefonica R&D                                                                                    #
#                                                                                                                      #
# Permission is hereby granted, free of charge, to any person obtaining a copy  of this software and associated        #
# documentation files (the 'Software'), to deal in the Software without restriction, including without limitation the  #
# rights in the Software without restriction, including without limitation the rights o use, copy, modify, merge,      #
# publish,  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and      #
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:                   #
#                                                                                                                      #
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO     #
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.#
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN   #
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER #
# DEALINGS IN THE SOFTWARE.                                                                                            #
#                                                                                                                      #
########################################################################################################################

from __future__ import print_function
from log import *
from utils import *
from os import remove
import requests
import json


KITE_API = ":8010/services/REST/GlobalM2M/Inventory/v6/r12/sim?"
KITE_API_IP = "ip=%s"
KITE_API_ICC = "icc=%s"
KITE_API_ALIAS = "alias=%s"

def get_info_from_ip(url, certificate, key, ipAddress):
    """HTTPS request in Kite using the IP Address.

    :param url: url of Kite to search using the ip
    :param certificate: certificate file for Kite connection
    :param key: private key file for Kite connection
    :param ipAddress: SIM's IP Address
    :return: the https response from url find by the IP

    """
    url_api = url + KITE_API_IP
    kite_response = requests.get(url_api % ipAddress,cert=(certificate, key), verify=False)

    return kite_response


def get_info_from_icc(url, certificate, key, iccNumber):
    """ HTTPS request in Kite using the ICC Number.

    :param url: url of Kite to search using the icc
    :param certificate: certificate file for Kite connection
    :param key: private key file for Kite connection
    :param iccNumber: SIM's ICC Number
    :return: the https response from url find by the ICC

    """
    url_api = url + KITE_API_ICC
    kite_response = requests.get(url_api % iccNumber, cert=(certificate, key), verify=False)

    return kite_response


def get_info_from_alias(url, certificate, key, alias_name):
    """HTTPS request in Kite using the IP Address.

    :param url: url of Kite to search using the ip
    :param certificate: certificate file for Kite connection
    :param key: private key file for Kite connection
    :param ipAddress: SIM's IP Address
    :return: the https response from url find by the IP

    """
    url_api = url + KITE_API_ALIAS
    kite_response = requests.get(url_api % alias_name, cert=(certificate, key), verify=False)

    return kite_response


def kite_get_custom_parameters(url, certificate, key, ipAddress):
    """Get de Custom Fields from Kite Platform

    :param url: dictionary with Kite urls
    :param certificate: certificate file for Kite connection
    :param key: private key file for Kite connection
    :param ipAddress:
    :return: status of the connection[0], Thing name [1] and default topic [2]

    """
    url_api = url + KITE_API
    kite_response = get_info_from_ip(url_api, certificate, key, ipAddress)

    thing_name = ""
    thing_topic = ""
    thing_latitude = ""
    thing_longitude = ""

    logger.info("KITE Response status code [ %s ]" % kite_response.status_code )

    if kite_response.status_code == 200:
        connected = True
        json_kite_response = json.loads(kite_response.text)
        thing_name = json_kite_response["subscriptionData"][0]["customField1"]
        thing_topic = json_kite_response["subscriptionData"][0]["customField2"]
        logger.debug("KITE: Reading thing name [ %s ]" % thing_name)
        logger.debug("KITE: Reading thing topic [ %s ]" % thing_topic)

        if json_kite_response["subscriptionData"][0]["supplServices"]["location"]:
            thing_latitude = json_kite_response["subscriptionData"][0]["automaticLocation"]["coordinates"]["latitude"]
            thing_longitude = json_kite_response["subscriptionData"][0]["manualLocation"]["coordinates"]["longitude"]
            logger.debug("KITE: Reading latitude [ %s ]" % thing_latitude)
            logger.debug("KITE: Reading longitude [ %s ]" % thing_longitude)


    else:
        connected = False

    return connected, thing_name, thing_topic, kite_response.status_code, thing_latitude, thing_longitude

class Kite:
    """ Contains the information of the SIM in Kite.

    """
    status_ok = False
    ip = ''
    device_name = ''
    cloud_topic = ''
    latitude = ''
    longitude = ''
    code = 0

    def __init__(self, ip_address, certificate, private_key):
        """ Class Kite Constructor.

        :param ipAddress: SIM's IP Address

        """
        logger.debug("KITE: Reading config file")
        config_file = read_config('config/Configuration.yaml')
        url = config_file["KITE"]["url"]

        '''fd_cert, temp_path_cert = tempfile.mkstemp()
        temp_file_cert = open(temp_path_cert, 'w')
        temp_file_cert.write(certificate)
        temp_file_cert.close()

        fd_key, temp_path_key = tempfile.mkstemp()
        temp_file_key = open(temp_path_key, 'w')
        temp_file_key.write(private_key)
        temp_file_key.close()'''

        temp_path_cert = tmp_file(certificate)
        temp_path_key = tmp_file(private_key)

        try:

            self.ip = ip_address
            self.status_ok, self.device_name, self.cloud_topic, self.code, self.latitude, self.longitude = \
                kite_get_custom_parameters(url, temp_path_cert, temp_path_key, ip_address)

            os.remove(temp_path_cert)
            os.remove(temp_path_key)

        except Exception as e:
            os.remove(temp_path_cert)
            os.remove(temp_path_key)

        logger.debug("KITE: Readed ")


