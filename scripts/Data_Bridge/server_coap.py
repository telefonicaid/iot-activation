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
from bridge import *
from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from coapthon.defines import Codes
import uuid


def uri_query_parse(uri_query):
    """
    Parse an uri query.
    :param uri_query: the string to parse
    :return: the dict with the results
    """
    dict_query = {}
    query = uri_query.split("&")
    for parameter in query:
        param = parameter.split("=")
        if len(param) > 1:
            dict_query[param[0]] = param[1]
    return json.dumps(dict_query)


class AdvancedResource(Resource):
    def __init__(self, name="Advanced", coap_server=None, config_file=None, config_cloud=None):
        super(AdvancedResource, self).__init__(name, coap_server, visible=True,
                                               observable=True, allow_children=True)
        self.payload = "Data Bridge"
        self.config_file = config_file
        self.config_cloud = config_cloud

    def render_GET_advanced(self, request, response):
        uuid_get = uuid.uuid4().hex
        logger.info("%s CoAP GET request from [ %s ]", uuid_get, request.source[0])
        response_bridge = bridge(uuid_get, uri_query_parse(request.uri_query), request.source[0], self.config_file, self.config_cloud, "GET")
        response.payload = response_bridge
        response.code = to_coap_code(response_bridge["code"])
        logger.info("%s - Sent MESSAGE [ %s ] to [ %s ] id [ %s ]" % (uuid_get, response_bridge, request.source[0], uuid_get))

        return self, response

    def render_POST_advanced(self, request, response):
        uuid_post = uuid.uuid4().hex
        logger.info("%s - CoAP POST request from [ %s ]", uuid_post, request.source[0])
        logger.info("%s - POST request payload [ %s ]", uuid_post, request.payload)
        response_bridge = bridge(uuid_post, request.payload, request.source[0], self.config_file, self.config_cloud, "POST")
        response.payload = response_bridge
        response.code = to_coap_code(response_bridge["code"])
        logger.info("%s - Sent MESSAGE [ %s ] to [ %s ]" % (uuid_post, response_bridge, request.source[0]))
        return self, response


class CoAPServer(CoAP):
    def __init__(self, host, port, config_file, config_cloud):
        CoAP.__init__(self, (host, port))

        self.config_file = config_file
        self.config_cloud = config_cloud

        self.add_resource('shadow', AdvancedResource("DataBridge", None, config_file, config_cloud))


def coap_loop(config_file, config_cloud):
    """
    Listening loop,
    Open a socket to receive a UDP message and send the ACK
    :param config_file:
    :param config_cloud:
    :return:
    """
    try:
        logger.info("CoAP server listening in: [ %s:%s ]" % (config_file["COAP"]["ip"],config_file["COAP"]["port"]))
        loop_text = "######################## CoAP Port [ %s ]: waiting for a message ########################"
        logger.info(loop_text, config_file["COAP"]["port"])

        server = CoAPServer(config_file["COAP"]["ip"], config_file["COAP"]["port"], config_file, config_cloud)
        server.listen(10)

    except Exception as e:
        logger.error("exception udp_loop()")
        logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)

    finally:
        return 0


def to_coap_code(http_code):
    # 4xx Client errors
    if http_code in [400, 405, 409, 414, 431]:
        return Codes.BAD_REQUEST.number
    elif http_code == 404:
        return Codes.NOT_FOUND.number
    elif http_code in [401, 403]:
        return Codes.FORBIDDEN.number
    elif http_code == 406:
        return Codes.NOT_ACCEPTABLE.number
    elif http_code == 412:
        return Codes.PRECONDITION_FAILED.number
    elif http_code == 413:
        return Codes.REQUEST_ENTITY_TOO_LARGE.number
    elif http_code == 415:
        return Codes.UNSUPPORTED_CONTENT_FORMAT.number
    # 5xx Server errors
    elif http_code == 500:
        return Codes.INTERNAL_SERVER_ERROR.number
    elif http_code == 501:
        return Codes.NOT_IMPLEMENTED.number
    elif http_code == 502:
        return Codes.BAD_GATEWAY.number
    elif http_code == 503:
        return Codes.SERVICE_UNAVAILABLE.number
    elif http_code == 504:
        return Codes.GATEWAY_TIMEOUT.number
    # 2xx Success
    elif http_code == 200 and Codes.GET.number:
        return Codes.CONTENT.number
    elif http_code == 201:
        return Codes.CREATED.number
    elif http_code == 204:  # returned by Kite
        return Codes.NOT_FOUND.number
    # 3xx Redirection
    elif http_code == 304:
        return Codes.VALID.number
    # 1xx Informational response
    elif http_code == 100:
        return Codes.CONTINUE.number
    # ELSE
    return Codes.EMPTY.number
