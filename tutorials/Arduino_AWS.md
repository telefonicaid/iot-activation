### Table of Contents

- [Arduino: MKR NB-1500 to AWS-IoT](#arduino-mkr-nb-1500-to-aws-iot)
  * [Getting started with the MKR NB-1500](#getting-started-with-the-mkr-nb-1500)
	- [What you will need](#what-you-will-need)
	- [What you will learn](#what-you-will-learn)
  * [Open an account at AWS-IoT](#open-an-account-at-aws-iot)
  * [Create Arduino thing in AWS-IoT](#create-arduino-thing-in-aws-iot)
  * [What is MQTT](#what-is-mqtt)
  * [Test your Certificates with MQTT.fx](#test-your-certificates-with-mqttfx)
  * [How to comunicate with AWS](#how-to-comunicate-with-aws)
- [How to Start with the project](#how-to-start-with-the-project)
  * [Arduino Board: Run a code file](#arduino-board-run-a-code-file)
  * [UDP data Bridge: Connecting using NB-IoT o LTE-M](#udp-data-bridge-connecting-using-nb-iot-o-lte-m)
  * [Check the Shadow](#check-the-shadow)
  * [Send a command](#send-a-command)

 
# Arduino: MKR NB-1500 to AWS-IoT

For this project, we will take different values from the Arduino board and publish them in AWS. 

<p align="center">      
	  <img  title="Project_ard" src="pictures/schematics/overview_arduino_AWS.png"
	  href="docs/Arduino_AWS.md" 
	  >	  
</p>

## Getting started with the MKR NB-1500

#### What you will need

- Finish successfully the Arduino Starterkit tutorial
- Arduino board MKR NB-1500
- Micro USB cable
- Arduino IDE
- AWS account

#### What you will learn

- Control Arduino board MKR NB-1500 using the Arduino IDE
- Register a device on AWS
- Generate credentials for AWS
- Build a bridge between UDP and MQTT with Python

If you have successfully completed the Arduino Starterkit tutorial, all the necessary software is already updated.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Open an account at AWS-IoT
(Soon)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Create Arduino thing in AWS-IoT

1. Sign in to the AWS Management Console, and then open the AWS IoT console at https://console.aws.amazon.com/iot
2. Go to the Monitor page. In the left navigation panel, choose Manage, and then choose Things.
![pic](pictures/AWS/AWS_Console.png)
3. You don't have a thing created yet page. Choose Register a thing.
![pic](pictures/AWS/AWS_Console_Manage_Register.png)
4. On the Creating AWS IoT things page, choose Create a single thing.
![pic](pictures/AWS/AWS_Console_Manage_Register_things.png)
5. Enter a name for the device, leave the default values for all the other fields, and then choose Next.
![pic](pictures/AWS/AWS_Console_Manage_Register_Device.png)
6. Now generates the certificates.
![pic](pictures/AWS/AWS_Console_Manage_Certificates.png)
7. Download your public and private keys, certificate, and root certificate authority (CA)on your PC. 
![pic](pictures/AWS/AWS_Console_Manage_Certificates_Download.png)
8. For download your root certificate authority a new window is open for select a CA to download
![pic](pictures/AWS/AWS_Console_Manage_Certificates_Download_CA.png)
9. Don't forget to save these files, you need them to set the connection
10. Returns to the previous window and **Activate** 
11. Select **Attach a policy**
![pic](pictures/AWS/AWS_Console_Manage_Certificates_Download.png)
12. Close this window, before you need to create and attach a new policy to the certificate
![pic](pictures/AWS/AWS_Console_Manage_Certificates_AttachPolicy.png)
13. Open the AWS IoT console again https://console.aws.amazon.com/iot
14. In the left navigation panel, choose **Secure**, and then choose **Policies**. 
15. Select **Create a Policy**
![pic](pictures/AWS/AWS_Console_Secure_Policies.png)
16. Enter a Name for the policy:
    - **Action**        enter **iot:***
    - **Resource ARN**  enter **\***
    - **Effect**        choose **Allow**
Select Create. This policy allows your Device to publish messages to AWS IoT.
![pic](pictures/AWS/AWS_Console_Secure_Policies_Create_Device.png)
17. In the AWS IoT console, choose **Manage**, **Things**. On the Things page, choose your Thing
![pic](pictures/AWS/AWS_Console_Manage_Things_Device.png)
18. On the thing's **Details** page, in the left navigation panel, choose **Interact**.
Make a note of the REST API endpoint. You need it to connect to your device shadow.
![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Interact_Device.png)
19. Now select **Security**, and choose the certificate that you created earlier. 
![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Security_Device.png)
20. In Actions, choose Attach policy
![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Security_Policy_Device.png)
21. Select your new policy and then choose Attach 
![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Security_Policy_Attach_Device.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## What is MQTT
MQTT is a machine-to-machine (M2M)/"Internet of Things" connectivity protocol. 
It was designed as an extremely lightweight publish/subscribe messaging transport.

The first concept is the publish and subscribe system. 
A device can publish a message on a topic, 
or it can be subscribed to a topic to receive messages

AWS use this system to communicate with your devices

If you access to AWS Management Console.In the left navigation panel, choose Manage, and then choose Things.
When choose a thing you can find out the different topic that you can subscribe/publish 
Select ***Interact* to copy they

![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Interact_MQTT_Device.png)

At the moment, you only need to know three topics:
- Update to this thing shadow
```
$aws/things/MyDevice/shadow/update
```
- Update to this thing shadow was accepted
```
$aws/things/MyDevice/shadow/update/accepted
```
- Update to this thing shadow was rejected
```
$aws/things/MyDevice/shadow/update/rejected
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Test your Certificates with MQTT.fx

One of the best ways to make sure that certificates have been created correctly is to try connecting via a 
MQTT client with graphical interface.

We recommend you download MQTT.fx from the following link https://mqttfx.jensd.de/

1. Open MQTT.fx and create a new connection.

![pic](pictures/MQTT/MQTTFX_open.png)

2. Configure the broker as shown in the image below.
Remember to use the files you downloaded in the previous step. And configure the broker address associated to your device.

![pic](pictures/MQTT/MQTTFX_Broker_Connect.png)

3. Now that you are connected to the broker, you need to subscribe to the topics to know the state of the shadow: 
accepted and rejected.

Every time a message is published in the topic to update the shadow, 
you can check in these topics if the message has been **accepted** or **rejected**.
```
$aws/things/MyDevice/shadow/update/accepted
$aws/things/MyDevice/shadow/update/rejected
```

![pic](pictures/MQTT/MQTTFX_Topic_Subscribe_Device.png)

4. To update your device's shadow, You should publish in the topic the following **json file**, 
you can use the following link to validate it https://jsonlint.com/

```
{
    "state": {
        "reported" : { 
            "voltage" : 22    
        }
    }
}
```
This file will simulate the publishing of a device to make voltage measurements.

![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Shadow_Device.png)

5. Choose the topic to update your shadow.
Be sure to select the service quality level as QoS 0, amazon doesn't allow a different police.
```
$aws/things/MyDevice/shadow/update
```

![pic](pictures/MQTT/MQTTFX_Topic_Publish_Device.png)

6. For delete the shadow's document publish the next **json file**
```
{
    "state": null
}
```

7. Play with this, sending different values until you understand how it works.
:thumbsup: Remember to check if your values has been accepted or rejected

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## How to comunicate with AWS

As you know, when you register a new device in AWS, several topics are created by default. Using them you can send data and receive information.

For the time being,  you only need to know a couple of them:

topic Update 
```
$aws/things/MyDevice/shadow/update
```
this topic is where you publish the status of the device,
in this tutorial this information is composed by the values of the sensors as the current color of the LED display.

topic Delta
```
$aws/things/MyDevice/shadow/update/delta
```
This is the channel that AWS uses to communicate the **desired** changes to the device.
In this case we use the MQTT.fx to communicate these changes to AWS and to report the change to the device.

All these changes are recorded in the **shadow** of the device. 
To see the current status just access the AWS core as you saw in the previous section.

![pic](pictures/AWS/AWS_Console_Manage_Things_Details_Shadow_Delta_Device.png)

```json
{
  "desired": {
    "command": "Warning"
  },
  "reported": {
    "command": "OK",
    "voltage": 22,
    "amperage": 15
  },
  "delta": {
    "command": "Warning"
  }
}
```
As you notice in the previous file, there are three main keys:
- "desired": Contains the desired state, sent from the MQTT.fx
- "reported": Contains the status information reported by the device
- "delta": contains the differences between the reported status and the desired status. 
This is the information that is published in the delta topic

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

# How to Start with the project

We will explain it to you later in detail how to play with it step by step, 
In this tutorial you need to be familiar with the following concepts

- Run a code file on your Arduino Board
- Run a python server with the credentials manager
- Upload the credentials files to a Server
- Use MQTT.fx to post messages in a topic
- Get the shadow from AWS core


Now you can connect to the internet and send your data through the UDP protocol.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Arduino Board: Run a code file

For this Arduino project, it is necessary that you include some of the classes we have prepared exclusively 
for this tutorial. To do this, be sure to open the **.ino** file from the following 
[folder](../scripts/Arduino/Connection_UDP). 
There are all the files you need.

In the following code you can see the main structure of the program:
1. Measuring
2. Modem connection to the network
3. Sending of the measures
4. Disconnection of the modem to reduce power consumption
5. Sampling timeout
```c
}

void loop() {
  // put your main code here, to run repeatedly:
    
  Serial.println("measuring...");
  data.measurement();
  Serial.print("- voltage: ");
  Serial.println(data.get_voltage());
  Serial.print("- amperage: "); 
  Serial.println(data.get_amperage());

  Serial.println("Sending... ");     
  nbAccess.noLowPowerMode();
  send_data_UDP(data.get_voltage(),data.get_amperage()); 
  nbAccess.lowPowerMode();
  
  delay(polling);
}
```
But first of all, don't forget to complete the configuration [file](../scripts/Arduino/Connection_UDP/configuration.h)

In the you have to complete the necessary information to complete the sending of information to the UDP server.
```c
//complete only if your SIM card has a PIN lock code
#define SECRET_PINNUMBER ""  

//Samples sent every 5 seconds 
#define POLL_TIME 5

//IP address and port of your UDP server
#define LOCAL_PORT 4114
#define IP_ADDRESS XXX,XXX,XXX,XXX

```
[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## UDP data Bridge: Connecting using NB-IoT o LTE-M

One of the advantages of an iot device, is to be able to stop the connection when it is not necessary 
to decrease the energy consumption.

From iot-activation we suggest you the mounting of a data bridge between the UDP sending of your Arduino and the 
AWS MQTT protocol.

This allows you to increase the intelligence of your devices by integrating the Kite Platform into this server,
and this add extra security in sending data over the network. 
By updating your Kite SIM information, the data bridge recognizes the SIM and automatically connects to 
the corresponding AWS MQTT broker. 

Solo tendrás que asegurarte de añadir el nombre de la cosa como uno de los campos propios de la SIM en Kite
[Kite](Movistar_Kite_Platform.md#sim-identification)

This [bridge](../scripts/Python/UDP_to_MQTT_Bridge)
is the easiest way to connect to AWS using only one UDP send

```python
	logger.info("###############################################################################")
	logger.info("############################### LOOP  listening ###############################")
	logger.info("###############################################################################")
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((config_file["UDP"]["ip"], (config_file["UDP"]["port"])))
	udp_msg, udp_ip = sock.recvfrom(1024)
	logger.info("Received message[ %s ] from [ %s ]" % (udp_msg, udp_ip[0]))
	sock.close()

	request = parser_info(udp_msg, udp_ip[0], config_cloud)

	ack_msg = request
	logger.info("Sending ACK [ %s ]" % ack_msg)
	sock_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock_send.sendto(ack_msg, (udp_ip[0], config_file["UDP"]["port"]))
	sock_send.close()
	logger.info("ACK sent")

```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Check the Shadow

Before starting the execution you will see how your shadow is empty. 
With this script you can send voltage and current values
This updated the shadow with each shipment of the device every few seconds.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Send a command

To send a command to the device you must use the MQTT as explained in the previous section through the json that we provide. 
You can change this instruction as many times as needed.

```json
{
	"state": {
		"desired": {
			"command": "Wait"
		}
	}
}
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

