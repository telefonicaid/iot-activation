---
layout: post
title:  "Data Bridge on Google Cloud"
date:   2019-02-06 12:00:00 +00:00
categories: tutorial
---
### Table of Contents

- [What does it do?](#what-does-it-do)
  * [Google Cloud Options](#google-cloud-options)
    + [GCP Option 1: publish in a default topic](#gcp-option-1-publish-in-a-default-topic)
- [Deploy and defend your Bridge!](#now-deploy-and-defend-your-bridge)
  * [What will you need?](#what-will-you-need)
  * [Data Bridge python code](#data-bridge-python-code)
  * [KITE Platform certificates](#kite-platform-certificates)
  * [IPsec tunnel configuration between Telefónica and AWS](#ipsec-tunnel-configuration-between-telefónica-and-aws)
  * [Google Cloud Platform Computing Services](#google-cloud-platform-computing-services)
- [How to run it](#how-to-run-it)
  * [Download it](#download-it)
  * [Configure it](#configure-it)
  * [Launch it](#launch-it)



# What does it do?

Each UDP message sent by a device, it is linked to several information such as source IP, destination IP and destination Port. 
The Bridge will use the device source IP to gather all the sim information stored at Kite platform. 

For the tutorial purpose you should pay attention to SIM's custom fields, 
that you can manage from your Kite Platform account. 

- Field 1 : Device Cloud Name (required) -> this is the name that will appear at the cloud (shadow name, twin name ...) 
- Field 2 : topic to publish (optional)

Depending on the content of the fields the Bridge will act differently. 

To choose between the different options you have to configure SIM information at the [Custom Field](Kite_Platform.md#edit-custom-field)

&#x1F4CD;
The device name is a mandatory field, otherwise an error code will be returned, because the bridge wouldn't know the virtual representation of the physical device.

As we said before, There are 1 way of working depending on the information provided as custom parameter in Kite. 

news options in process ...

## Google Cloud Options

- [GCP Option 1: publish in a default topic](#gcp-option-1-publish-in-a-default-topic)


#### GCP Option 1: Telemetry

You only have to provide a device cloud name at the first custom parameter in Kite. 
As a result all the messages sent by your device will be published at the device telemetry topic. 

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# Now, Deploy and defend your Bridge!

- Data Bridge [code](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge)
- KITE Platform [Certificates files](Kite_Platform.md#what-is-kite-platform-api)
- An IpSec Service provided by Telefónica [(IPsec)](BP_IPsec.md#what-is-ipsec)
- Google Cloud account:

&#x1F4CD;
For the time being, if you use a SIM from the Thinx testing network you will not have access to the Kite Platform.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Data Bridge python code

You can download it from our [repository](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## KITE Platform certificates

One of the Data Bridge strong points, is the integration with Kite.
Kite is the Telefónica's IoT Connectivity Platform, and Kite provides an API interface for management via HTTPS.

Ask your Telefonica's local contact for the certificates associated to your account. 

Once you receive this certificate, you will need to extract the keys that the Bridge will use to validate the connection.
If you want to learn how to do it, you can follow our 
[documentation](Kite_Platform.md#extract-your-credentials-files)

When you finish these steps, you should have a file with the certificate and another one with the access key:
- your_customer_certificate.cer
- your_customer_certificate.key

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## IPsec tunnel configuration between Telefónica and AWS

An IPsec tunnel is a direct connection between the mobile network of your SIM pool and the Data Bridge deployed in AWS.

This connection not only creates a new network (VPN) but also guarantees the security of your data 
by allowing communication only between the devices that belong to this network.

Although its functioning is quite complex to explain. The configuration is quite simple if you follow our 
[tutorial](BP_IPsec.md#how-to-make-your-own-ipsec-vpn)

When you finish this tutorial, you will also have created a EC2 machine. 
This is the machine you will use to deploy your Data Bridge.

Remember to keep both the private IP of your IPsec network and the public IP to remotely access the machine. 

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Google Cloud Platform Computing Services

If you are using this tutorial is because you have chosen Google as your cloud.

For this reason, we have tried that all the services provided in the Data Bridge are integrated at Google Cloud Platform platform.
In the following steps we will explain how to configure these services.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

in process ..

# How to run it

Now that you know how to configure AWS. You can run it in just 3 steps !!!

## Download it

You can choose between several options: 

- option 1: Download the Github repository on the instance

1. Install git on the instace
```shell
sudo apt-get upgrade
sudo apt-get install git
```
2. Clone the repository
```shell
git clone https://github.com/telefonicaid/iot-activation.git
```
3. Go to Bridge path: **scripts/Data_Bridge/**

- option 2: Upload the files from an FTP client

1. Download the Github repository
2. Open Filezilla client
3. Select the path scripts/Data_Bridge/
4. Upload all files and folders to the instance

Now that you have the code in the machine you just have to install the python libraries.

You can install them one by one. But the fastest way is to use the requirements file

```python
pip install -r requirements.txt
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Configure it

We have tried to make this as simple as possible.

So, you'll only need to fill in a few fields in the configuration file 
[Configuration.yaml](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge/config/Configuration.yaml)

```yaml
cloud: GCP

UDP:
  ip: "0.0.0.0"
  port: 4114

KITE:
  url: "https://m2m-api.telefonica.com"
  certificate: "cer_file"
  private_key: "key_file"

```


#### Configure the Cloud

This parameter is used to identify the cloud and select the configuration file. 
In this example you must select GCP

```yaml
cloud: GCP
```


#### Configure the UDP socket

Here you can choose the port through which you will receive the UDP messages and the allowed IP addresses

```yaml
UDP:
  ip: "0.0.0.0"
  port: 4114
```
allow any address

allowed values:
- ip: "0.0.0.0"    (allow any address)
- ip: "X.X.X.X"	   (restrict to a single address)


#### Configure the Kite Platform connection

This parameter allows you to select the files the certificates to access the Kite Platform.

```yaml
KITE:
  url: "https://m2m-api.telefonica.com"
  certificate: "cer_file"
  private_key: "key_file"
```

Do you remember the name of the parameters created?
Now is the time to use them.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


#### Configure the Google file

Here is an example of a configuration file for Google Cloud connection 
[Configuration_GCP.yaml](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge/config/Configuration_GCP.yaml)

```yaml
base_url: "https://cloudiotdevice.googleapis.com/v1"

project_id: "xxxxxxxxxx"
cloud_region: "xxxx-xxxx"
registry_id: "xxxxxxxx"
service_account_json: "service_account.json"

algorithm: "RS256"
path: "CA/"
ca_certs: "https://pki.google.com/roots.pem"
private_key_file: GCP_rsa_private.pem
public_key_file: GCP_rsa_public.pem
```

Currently the access keys must be configured via the configuration file and stored on the server.

##### Project configuration

```yaml
project_id: "xxxxxxxxxx"
cloud_region: "xxxx-xxxx"
registry_id: "xxxxxxxx"
service_account_json: "service_account.json"

```
- **service_account.json:** A file that establish the identity of the service account

```json
{
"type": "service_account",
"project_id": "[PROJECT-ID]",
"private_key_id": "[KEY-ID]",
"private_key": "-----BEGIN PRIVATE KEY-----\n[PRIVATE-KEY]\n-----END PRIVATE KEY-----\n",
"client_email": "[SERVICE-ACCOUNT-EMAIL]",
"client_id": "[CLIENT-ID]",
"auth_uri": "https://accounts.google.com/o/oauth2/auth",
"token_uri": "https://accounts.google.com/o/oauth2/token",
"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
"client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/[SERVICE-ACCOUNT-EMAIL]"
}
```

##### Certificates configuration

These are the parameters that will guarantee the security of your devices.
if you want to know how to generate them access the [tutorial](Arduino_GCP.md#-generate-your-devices-keys)

```yaml
algorithm: "RS256"
path: "CA/"
ca_certs: "https://pki.google.com/roots.pem"
private_key_file: GCP_rsa_private.pem
public_key_file: GCP_rsa_public.pem
```

- **GCP_rsa_private.pem:** The private key that must be securely stored on the device and used to sign the authentication.
- **GCP_rsa_public.pem:** The public key that must be stored in Cloud IoT Core and used to verify the signature of the authentication.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Launch it

Go to Bridge path and execute this command

```shell
sudo nohup python main.py &
```
- **sudo** Execute the instruction as if you were the administrator.
- **nohup** It'll keep running even when you close the session.
- **python main.py** will execute the code

When the Bridge is running, it will record all UDP messages he receives in a log file. 
You can monitor the last lines of the file with this command:

```sh
tail -f log/data_bridge.log
```

This is a log file example.

```log
INFO : ################################# waiting for a new message #################################
INFO : Message Received [ {"v":33,"a":28} ] from [ 10.5.0.5 ] : [ 4114 ]
INFO : KITE Response status code [ 200 ]
INFO : GET information related to [ 10.5.0.5 ] from  KITE Platform
INFO : Found device cloud name [ MyDevice ] and topic [  ] in KITE Platform
INFO : Select Option 1: DEVICE [ MyDevice ] and DEFAULT TOPIC
INFO : Publish message [ {"v":33,"a":28} ] into topic [ tlm/MyDevice/raw ]
INFO : Publish Accepted code [ 200 ]
INFO : Sent MESSAGE [ {"msg": "OK: msg published", "code": 200} ] to [ 10.5.0.5 ] : [ 4114 ]
INFO : ################################# waiting for a new message #################################
INFO : Message Received [ aaa ] from [ 00.00.00.00 ] : [ 4114 ]
INFO : KITE Response status code [ 204 ]
INFO : GET information related to [ 00.00.00.00 ] from  KITE Platform
INFO : Sent MESSAGE [{"msg":"ERROR:connection with Kite not established","code":404}] to [ 84.78.20.223 ]:[4114]
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)





















