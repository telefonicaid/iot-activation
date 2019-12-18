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
from utils import *
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

KITE_API = "/services/REST/GlobalM2M/Inventory/v6/r12/sim?"  # type: str
KITE_API_IP = "ip=%s"
KITE_API_ICC = "icc=%s"
KITE_API_APN = "apn=%s"


def get_info_from_ip(url, certificate, key, ip_address, apn):
    """
    HTTPS request in Kite using the SIM IP and its APN.
    :param url: url of Kite to search using the ip
    :param certificate: certificate file for Kite connection
    :param key: private key file for Kite connection
    :param ip_address: SIM's IP Address
    :param apn: SIM APN
    :return: the https response from url find by the IP

    """
    url_api = url + KITE_API_IP
    url_api = url_api % ip_address
    url_api = url_api + "&" + KITE_API_APN
    url_api = url_api % apn
    kite_response = requests.get(url_api, cert=(certificate, key), verify=False)

    return kite_response


def get_info_from_icc(url, certificate, key, icc_number):
    """
     HTTPS request in Kite using the SIM ICC and its APN.
    :param url: url of Kite to search using the icc
    :param certificate: certificate file for Kite connection
    :param key: private key file for Kite connection
    :param icc_number: SIM's ICC Number
    :return: the https response from url find by the ICC
    """
    url_api = url + KITE_API_ICC
    url_api = url_api % icc_number

    kite_response = requests.get(url_api, cert=(certificate, key), verify=False)
    return kite_response


def kite_get_parameters(ip_address, certificate, private_key, icc, config_file):
    """
    Function for get the SIM parameter stored in Kite Platform
    :param ip_address:
    :param certificate:
    :param private_key:
    :param icc:
    :param config_file:
    :return: SIM parameter stored in Kite Platform
    """

    logger.debug("KITE: Reading config file")
    url_kite = config_file["KITE"]["url"]
    apn_kite = config_file["KITE"]["apn"]
    logger.debug("KITE: url [ %s ]", url_kite)
    logger.debug("KITE: APN [ %s ]", apn_kite)

    url_api = url_kite + KITE_API
    temp_path_cert = tmp_file(certificate)
    temp_path_key = tmp_file(private_key)

    kite_parameters = {"code": 500, "msg": "KITE - Internal Server Error"}

    try:
        if icc is None:
            kite_response = get_info_from_ip(url_api, temp_path_cert, temp_path_key, ip_address, apn_kite)
        else:
            kite_response = get_info_from_icc(url_api, temp_path_cert, temp_path_key, icc)

    except Exception as e:
        kite_parameters = {"code": 400, "msg": "KITE - Access Error"}
        logger.error("KITE - Access Error")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    else:
        os.remove(temp_path_cert)
        os.remove(temp_path_key)

        kite_parameters["code"] = kite_response.status_code
        kite_parameters["msg"] = ""

        logger.debug("KITE Response status code [ %s ]" % kite_parameters["code"])

        if kite_parameters["code"] == CODE_OK:
            json_kite_response = json.loads(kite_response.text)
            thing_name = json_kite_response["subscriptionData"][0]["customField1"]
            thing_topic = json_kite_response["subscriptionData"][0]["customField2"]
            logger.debug("KITE: Reading thing name [ %s ]" % thing_name)
            logger.debug("KITE: Reading thing topic [ %s ]" % thing_topic)

            kite_parameters["connected"] = True
            kite_parameters["thing_name"] = thing_name
            kite_parameters["thing_topic"] = thing_topic

            if json_kite_response["subscriptionData"][0]["supplServices"]["location"]:
                thing_latitude = json_kite_response["subscriptionData"][0]["automaticLocation"]["coordinates"]["latitude"]
                thing_longitude = json_kite_response["subscriptionData"][0]["manualLocation"]["coordinates"]["longitude"]
                logger.debug("KITE: Reading latitude [ %s ]" % thing_latitude)
                logger.debug("KITE: Reading longitude [ %s ]" % thing_longitude)
                kite_parameters["location"] = True
                kite_parameters["latitude"] = thing_latitude
                kite_parameters["longitude"] = thing_longitude
            else:
                kite_parameters["location"] = False
        else:
            kite_parameters["msg"] = kite_response.text
    finally:
        return kite_parameters


def kite_test_credentials(certificate, private_key, config_file):
    """
    Function for test the credentials files
    :param certificate:
    :param private_key:
    :param config_file:
    :return: Boolean (True/False)
    """
    logger.debug("KITE: Testing credentials files")
    url_base = config_file["KITE"]["url"]
    url = url_base + "/services/REST/GlobalM2M/ServicePacks/v2/r12/servicePack"

    temp_path_cert = tmp_file(certificate)
    temp_path_key = tmp_file(private_key)

    kite_response = requests.get(url, cert=(temp_path_cert, temp_path_key), verify=False)

    if kite_response.status_code == CODE_OK:
        status = True
    else:
        status = False

    return status
