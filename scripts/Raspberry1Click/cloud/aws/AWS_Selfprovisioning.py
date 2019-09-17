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
import os
import boto3
import yaml
import time
import uuid
import logging


if __name__ == "__main__":

    os.system("clear")
    filename = "log/AWS_Self_provisioning.log"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info("Starting Self-Provision in AWS")
    logger.info("log file[ %s ]", filename)

    ans_null = True
    while ans_null:
        print("""
     1. US East (Ohio)
     2. US East (N. Virginia)
     3. US West (Oregon)
     4. Asia Pacific (Mumbai)
     5. Asia Pacific (Seoul)
     6. Asia Pacific (Singapore)
     7. Asia Pacific (Sydney)
     8. Asia Pacific (Tokyo)
     9. China (Beijing)
    10. EU (Frankfurt)
    11. EU (Ireland)
    12. EU (London)
    """)
        ans_null = False
        ans = raw_input("What is your region in the AWS cloud? ")
        aws_region = "eu-west-1"
        if ans == "1":
            aws_region = "us-east-2"
        elif ans == "2":
            aws_region = "us-east-1"
        elif ans == "3":
            aws_region = "us-west-2"
        elif ans == "4":
            aws_region = "ap-south-1"
        elif ans == "5":
            aws_region = "ap-northeast-2"
        elif ans == "6":
            aws_region = "ap-southeast-1"
        elif ans == "7":
            aws_region = "ap-southeast-2"
        elif ans == "8":
            aws_region = "ap-northeast-1"
        elif ans == "9":
            aws_region = "cn-north-1"
        elif ans == "10":
            aws_region = "eu-central-1"
        elif ans == "11":
            aws_region = "eu-west-1"
        elif ans == "12":
            aws_region = "eu-west-2"
        elif ans != "":
            logger.info("\n Not Valid Choice Try again")
            ans_null = True

    logger.info("AWS Region[ %s ] ", aws_region)

    url_iam = "https://console.aws.amazon.com/iam/home#/users"
    os.system("chromium-browser " + url_iam + " 2> log/url_iam.log &")

    time.sleep(5)

    url_tutorial = "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html#id_users_create_console"
    os.system("chromium-browser " + url_tutorial + " 2> log/url_tuto.log &")

    time.sleep(5)

    aws_key_id = raw_input("Copy your Access key ID: ")
    aws_secret_key = raw_input("Copy your Secret access key: ")

    url_broker = "https://console.aws.amazon.com/iot/home?region=" + aws_region + "#/settings"
    os.system("chromium-browser " + url_broker + " 2> log/url_broker.log &")
    time.sleep(5)
    aws_broker = raw_input("Copy your AWS broker from the web: ")

    aws_thing_name = "MyRaspberry_IoT_Activation"
    # aws_thing_name = raw_input("Select your Thing Name: ")

    config_cloud = {"region": aws_region, "broker": aws_broker, "thing": aws_thing_name}

    with open('AWS_configuration.yaml', 'w') as outfile:
        yaml.dump(config_cloud, outfile, default_flow_style=False)

    client = boto3.client('iot', region_name=aws_region, aws_access_key_id=aws_key_id,
                          aws_secret_access_key=aws_secret_key)

    response_cert = client.create_keys_and_certificate(setAsActive=True)
    cert_id = response_cert["certificateArn"]

    logger.info(cert_id)
    f = open('cert/cert_id.txt', 'w')
    f.write(cert_id)
    f.close()

    certificate_pem = response_cert["certificatePem"]
    certificate_PublicKey = response_cert["keyPair"]["PublicKey"]
    certificate_PrivateKey = response_cert["keyPair"]["PrivateKey"]

    f = open('cert/certificate_pem.pem.crt', 'w')
    f.write(certificate_pem)
    f.close()

    f = open('cert/PublicKey.pem.key', 'w')
    f.write(certificate_PublicKey)
    f.close()

    f = open('cert/PrivateKey.pem.key', 'w')
    f.write(certificate_PrivateKey)
    f.close()

    policy_file = open("src/policy.json", "r")

    search = True
    nextMarker = ""
    new_policy = True
    while search:
        response_list_policies = client.list_policies(marker=nextMarker, pageSize=10, ascendingOrder=True)
        for policy in response_list_policies["policies"]:
            if aws_thing_name == policy["policyName"]:
                search = False
                new_policy = False
        if "nextMarker" in response_list_policies:
            nextMarker = response_list_policies["nextMarker"]
        else:
            search = False

    if new_policy:
        response_policy = client.create_policy(policyName=aws_thing_name, policyDocument=policy_file.read())

    response_cert_policy = client.attach_policy(policyName=aws_thing_name, target=cert_id)
    response_thing = client.create_thing(thingName=aws_thing_name)
    response_cert_thing = client.attach_thing_principal(thingName=aws_thing_name, principal=cert_id)

    if aws_region == "eu-west-1":
        ans_dashboard = raw_input("Would you like to create a New Dashboard? [y/N] ")
        if len(ans_dashboard) > 0 and ans_dashboard[0].lower() in 'y':
            id_stack = str(uuid.uuid1()).replace('-', '')
            name_base = "raspberry1click"
            name_stack = name_base + id_stack
            url = 'https://s3-eu-west-1.amazonaws.com/lambda-for-deploy/cloud_formartion_freeboard.txt'
            parameters = [
                {
                    'ParameterKey': 'BucketNameDesired',
                    'ParameterValue': name_stack,
                    'UsePreviousValue': False
                }]
            capabilities = ['CAPABILITY_AUTO_EXPAND', 'CAPABILITY_IAM']
            client = boto3.client('cloudformation', region_name=aws_region, aws_access_key_id=aws_key_id, aws_secret_access_key=aws_secret_key)
            response_stack = client.create_stack(StackName=name_stack, TemplateURL=url, Parameters=parameters, Capabilities=capabilities)

            logger.info("Copy the next URL for display your dashboard")
            url_dashboard = "http://" + name_stack + ".s3-website-" + aws_region + ".amazonaws.com"
            logger.info(url_dashboard)
            logger.info("Attention, this may take a few minutes.")

            logger.info("Dashboard created")
        else:
            logger.info("Dashboard not created")
