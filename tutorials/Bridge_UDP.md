### Table of Contents

- [Data Bridge](#data-bridge)
    + [What our bridge is already doing](#what-our-bridge-is-already-doing)
    + [What's it gonna do next?](#whats-it-gonna-do-next)
	+ [Requirements](#requirements)	
- [What is this?](#what-is-this)
- [What it does?](#what-it-does) 
  * [AWS Options](#aws-options)
  * [Responses codes](#responses-codes)
- [How to configure it](#how-to-configure-it)
    + [How to configure the Cloud](#how-to-configure-the-cloud)
    + [How to configure the UDP socket](#how-to-configure-the-udp-socket)
    + [How to configure the Kite Platform connection](#how-to-configure-the-kite-platform-connection)
  * [AWS Configuration file](#aws-configuration-file)
    + [Server configuration](#server-configuration)
    + [IAM user](#iam-user)
    + [MQTT connection](#mqtt-connection)
- [Deploy and defend your Bridge!](#now-deploy-and-defend-your-bridge)

# Data Bridge

From Iot-Activation we want to make your way easier.

For this reason we don't just want to show you how to develop applications for your devices or how to connect to the cloud.
We put at your disposal a powerful tool that will facilitate and improve the performance of your things connected to the Internet.

Now you have the possibility to connect directly to the Cloud only sending a UDP message.

Wonderful!!! isn't it?

### What our bridge is already doing

- It accesses Kite Platform to retrieve your custom information (the device name and topic)
- It uses the IP address device to connect to the Cloud
- It publishes in AWS the message received through UDP message
- It returns an answer with the result of the publication
- It receives commands from the cloud
- A Telefonica network and your own security VPN

### What's it gonna do next?

- Compatibility with other clouds
- It will have more versatility in identifying problems.
- Better integration with Kite Platform 

### Requirements

- Server with Python 2.7 and Static IP (We've used an Amazon EC2 Instance)
- Python libraries:
  - socket
  - json
  - yaml
  - paho.mqtt.client
  - ssl
  - requests
  - boto3 (AWS)
- [KITE Platform](Movistar_Kite_Platform.md#access-step-by-step-using-the-curl-command) Certificates files
- A Telefonica Internet Protocol security [(IPsec)](IPsec.md)

If you use a SIM from the Thinx laboratory you will not have access to the Kite Platform.

# What is this?

The bridge is a code written in python that can be executed in any machine as a server. 
So all you have to do is run it on a machine with a known IP address.

When the Bridge starts running, it will establish a UDP socket and will keep listening continuously 
for any UDP messages sent to this IP address using a configured port.
Using the same connection to return a response with the result of the procedure.

The result of this procedure will be determined on the content provided in the Kite Platform and the configuration file.

But if you continue reading you will appreciate all the work that the Bridge can do for you.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

# What it does?

You can review the following flow chart, but you will understand it better if you read our comments we have written for you.

![pic](pictures/Bridge/Bridge_overview_AWS.png)

Each time you receive a UDP datagrams , it will be accompanied by the sender ip address of. 

The Bridge uses this ip to identify the SIM from which the information comes and retrieves the information provided in Kite.
To do this you must inform the Custom Field of the SIM:
- Field 1 : Device Name (required)
- Field 2 : name of the topic in which you want to publish (optional)

Depending on the content of the fields the Bridge will act differently. 

To choose between the different options you just have to configure the information of the SIM in the [Custom Field](Movistar_Kite_Platform.md#sim-identification)

:heavy_exclamation_mark: The device name must always be. If it is not given, an error code will be returned, 
because in this way we do not know the device of the Cloud in which we want to publish.

Here you have a list with the different options to configure the information in Kite Platform:

## AWS Options:

- [AWS Option 1: publish in a default topic](#aws-option-1-publish-in-a-default-topic)
- [AWS Option 2: publish in a custom topic](#aws-option-2-publish-in-a-custom-topic)
- [AWS Option 3: publish in the shadow](#aws-option-3-publish-in-the-shadow)

#### AWS Option 1: publish in a default topic

This option is the easiest to configure. Just leave the second fields empty, and the Bridge will do all the work.

The default topic has this structure:  **tlm/<DEVICE_NAME_IN_KITE>/raw**

![pic](pictures/Bridge/Bridge_overview_AWS_option1.png)


#### AWS Option 2: publish in a custom topic

Use the second field to write in the topic in which you want to publish the information.

![pic](pictures/Bridge/Bridge_overview_AWS_option2.png)


#### AWS Option 3: publish in the shadow

If you are using AWS as a cloud to connect your devices and you want to use shadow systems, this is undoubtedly your choice.

The configuration is quite simple, just identify the topic update of your device and copy it into the second custom field.
The structure will be similar to that of the next topic: **$aws/things/<DEVICE_NAME_IN_KITE>/shadow/update**

The bridge will quickly detect that this is an AWS reserved topic and will implement the appropriate logic for the connection. 

The data sent will be published in the shadow in the **raw** field as shown in the following example.

```json
{  
  "reported": {
    "raw": "<MESSAGE SENT HERE>",
  }
}
```

In addition to the connection, the Bridge will subscribe to the Accepted and Rejected topics. 
In this way you will be able to control if the publication has been done correctly or has been rejected by the broker.

Another advantage of using the AWS shadow is the interaction with the device, 
as it allows to retrieve shadow information, allowing the reception of commands.
because next to the response code, the contents of the field **delta**  in the shadow will be returned in json format.

![pic](pictures/Bridge/Bridge_overview_AWS_option3.png)

### What happens if we publish in a thing that doesn't exist?

Absolutely nothing! The Bridge will create it before publishing so you don't have to.
It will create a new thing from the given name of high the Kite.

But if you still tell them to create it manually you can follow these [steps](AWS_create_new_thing.md)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Responses codes

Whenever a message is received the Bridge will return a code indicating the status.

By means of the following list of codes we try to reflect all the possible situations that could happen.

| **CODE**  | **MSG** |
| :---:  | :---  |
| 200 | OK: msg published accepted |
| 401 | ERROR: Try to publish in an unauthorized topic |
| 404 | ERROR: connection with Kite not established |

# How to configure it

We have tried to make this as simple as possible.

So you'll only need to fill in a few fields in the configuration file  [Configuration.yaml](../scripts/Data_Bridge/config/Configuration.yaml)


### How to configure the Cloud

This parameter is used to identify the cloud and select the configuration file. 
At the moment only the AWS connection is available, but we cannot predict the future...

```yaml
cloud: AWS
```

allowed values:
- AWS

### How to configure the UDP socket

Here you can choose the port through which you will receive the UDP frames and the ip of the source device.

```yaml
UDP:
  ip: "0.0.0.0"
  port: 4114
```
allow any address

allowed values:
- ip: "0.0.0.0"    (allow any address)
- ip: "X.X.X.X"	   (restrict to a single address)

### How to configure the Kite Platform connection

This parameter allows you to select the files the certificates to access the Kite Platform.

```yaml
KITE:
  url: "https://m2m-api.telefonica.com"
  path: "CA/"
  certificate: "your_customer_certificate.cer"
  private_key: "your_customer_certificate.key"

```
Make sure both the path and file name are correct.

Also verify that the address of the urls matches the one of your access to Kite

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## AWS Configuration file

Even if it is possible to modify all the parameters, this is not necessary, since some of them are predefined for AWS.

Here is an example of a configuration file for Amazon Web Services connection 
[Configuration_AWS.yaml](../scripts/Data_Bridge/config/Configuration_AWS.yaml)

```yaml
cloud: AWS
region: "xx-xxxx-x"
IAM_user:
  access_key: "XXXXXXXXXXXXXXXXXXXX"
  secret_key: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
MQTT:
  topic:
    update: "$aws/things/<DEVICE_NAME>/shadow/update"
    default: "tlm/<DEVICE_NAME>/raw"
    log_device: "log/device/provision/new"
    reserved: "$aws"
```

The file is quite intuitive, however here you can see carefully how to configure each section

### Server configuration

```yaml
cloud: AWS
region: "xx-xxxx-x"
``` 
the cloud only assists the developer, in case it was completed incorrectly, the Bridge would correct it.  
However, you must indicate the location of the server you are using in AWS.

### IAM user

AWS Identity and Access Management (IAM) enables you to manage access to AWS services and resources securely.

You can create a user with access to the shadow to publish and get its content. 
Currently the access method we are using, so you will need to set up a user.

```yaml
IAM_user:
  access_key: "XXXXXXXXXXXXXXXXXXXX"
  secret_key: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```
Be sure to copy your user's credentials with permissions


### MQTT connection 

Optionally as part of the code library is included the publication in the shadow using the protocol MQTT. 
Since to simplify access to the cloud has been used AWS development library for python.

So if you want you can modify the source code to make the access through MQTT.

At the moment you only have to keep the fields as is

```yaml
MQTT:
  topic:
    update: "$aws/things/<DEVICE_NAME>/shadow/update"
    default: "tlm/<DEVICE_NAME>/raw"
    log_device: "log/device/provision/new"
    reserved: "$aws"
```
- update: this topic is the specific of AWS. It doesn't make any sense to modify it. 
- default: configure this field to select the default topic name
- log_device: topic name in which the new things creations are reported
- reserved: this parameter indicates that the name is a AWS standard topic.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

# Now, Deploy and defend your Bridge!

Now that you know how to configure the parameters, use it !!!.

Prepare a server capable of executing code in Python and upload the following code.

run the next command 

```
sudo nohup python main.py >>[YOUR_PATH]/bridge.log &
```
- **sudo** Execute the instruction as if you were the administrator.
- **nohup** It'll keep running even when you close the session.
- **python main.py** will execute the code
- **>>[YOUR_PATH]/bridge.log** You can use a file to store the logs

Download the [Bridge code](../scripts/Data_Bridge)


Example of the contents of a log file
```
2019-01-28 17:25:32,803 - INFO : ################################# waiting for a new message #################################
2019-01-28 17:26:38,640 - INFO : Message Received [ {"v":33,"a":28} ] from [ 10.5.0.5 ] : [ 4114 ]
2019-01-28 17:26:39,065 - INFO : KITE Response status code [ 200 ]
2019-01-28 17:26:39,066 - INFO : GET information related to [ 10.5.0.5 ] from  KITE Platform
2019-01-28 17:26:39,066 - INFO : Found device cloud name [ MyDevice ] and topic [  ] in KITE Platform
2019-01-28 17:26:39,066 - INFO : Select Option 1: DEVICE [ MyDevice ] and DEFAULT TOPIC
2019-01-28 17:26:39,066 - INFO : Publish message [ {"v":33,"a":28} ] into topic [ tlm/MyDevice/raw ]
2019-01-28 17:26:39,468 - INFO : Publish Accepted code [ 200 ]
2019-01-28 17:26:39,468 - INFO : Sent MESSAGE [ {"msg": "OK: msg published", "code": 200} ] to [ 10.5.0.5 ] : [ 4114 ]
2019-01-28 17:26:39,468 - INFO : ################################# waiting for a new message #################################
2019-01-28 17:39:29,432 - INFO : Message Received [ aaa ] from [ 84.78.20.223 ] : [ 19117 ]
2019-01-28 17:39:29,910 - INFO : KITE Response status code [ 204 ]
2019-01-28 17:39:29,910 - INFO : GET information related to [ 84.78.20.223 ] from  KITE Platform
2019-01-28 17:39:29,910 - INFO : Sent MESSAGE [ {"msg": "ERROR: connection with Kite not established", "code": 404} ] to [ 84.78.20.223 ] : [ 19117 ]

```


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
