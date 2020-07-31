### Table of Contents

- [Data Bridge behind the scenes](#data-bridge-behind-the-scenes)
  * [Data Bridge python code](#data-bridge-python-code)
  * [Amazon Web Services Cloud Computing Services](#amazon-web-services-cloud-computing-services)
    + [AWS Identity and Access Management (IAM)](#aws-identity-and-access-management-iam)
    + [AWS Systems Manager Parameter Store](#aws-systems-manager-parameter-store)
    + [AWS IoT Core](#aws-iot-core)
    + [Amazon Elastic Compute Cloud (EC2)](#amazon-elastic-compute-cloud-ec2)
    + [Amazon Elastic Load Balancing](#amazon-elastic-load-balancing)
- [How to run it](#how-to-run-it)
  * [Download it](#download-it)
  * [Configure it](#configure-it)
  * [Launch it](#launch-it)
  

# Data Bridge behind the scenes
Adapting the Bridge to your needs may be necessary. 
In this case you will need to know each one of the elements that compose it.

## Data Bridge python code

The Data Bridge Python code is Open Source, Adapt it to your needs!

Review our public repository in [Github](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge)

Or use the command `wget` to download a zip file with the code

```
wget https://raw.githubusercontent.com/telefonicaid/iot-activation/master/scripts/Data_Bridge/Data_Bridge.zip
```

Unzip the new file

```
unzip Data_Bridge.zip
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Amazon Web Services Cloud Computing Services

If you are using this tutorial is because you have chosen Amazon as your cloud.

For this reason, we have tried that all the services provided in the Data Bridge are integrated at AWS platform.
In the following steps we will explain how to configure these services.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


### AWS Identity and Access Management (IAM)

IAM is a service that allows you to manage access to AWS services and resources securely.
This service will allow you to control users and their permissions. 
But it will also allow you to manage access policies between the different Amazon services.

You will need it in this tutorial because it is necessary to assign an access policy to the EC2 machine 
that allows access to the other services. 

Your EC2 needs the following policies:
- Access to IoT Core
- Access to AWS Systems Manager Parameter store

To attach an IAM role to an instance ...

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.
2. In the navigation pane, choose Instances.
3. Select the instance, choose Actions, Instance Settings, Attach/Replace IAM role.
4. Select the IAM role to attach to your instance and choose Apply.


[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


### AWS Systems Manager Parameter Store

AWS Systems Manager is a service that gives you visibility and control of your infrastructure.

Among its resources, there is the Parameter Store. 
This parameter storage allows the secure storage of certificates and passwords.

For this example, we will use this service to store the content of the Kite certificates files.

In the AWS Console.

Go to Systems Manager / Parameter Store / Select: Create parameter 

![pic](pictures/AWS/AWS_Console_SystemsManager_ParameterStore_create.png)

Select a name for the parameter. And copy the contents of the file in the **value** field.

Do this for each of the files:
- your_customer_certificate.cer
- your_customer_certificate.key

![pic](pictures/AWS/AWS_Console_SystemsManager_ParameterStore_create_config1.png)
![pic](pictures/AWS/AWS_Console_SystemsManager_ParameterStore_create_config2.png)

And click on the **Create parameter** button at the bottom of the page.

Save the names of the parameters, they are necessary to configure the Bridge.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


### AWS IoT Core

AWS IoT Core is a managed cloud service that lets connected devices easily and 
securely interact with cloud applications and other devices.

If you have not previously worked with IoT Core, we recommend that you familiarize with the environment. 
And make sure you understand concepts like MQTT, Broker and Shadow.

As for configuring a new device, you can do so by following these 
[steps](AWS_create_new_thing.md#create-device-thing-in-aws-iot)

but if you're too lazy for it. "No problemo" The Bridge will create it for you.

Auto provisioning of new devices!!

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


### Amazon Elastic Compute Cloud (EC2)

Amazon EC2 is a web service that provides secure, resizable compute capacity in the cloud.

If you have carefully followed the steps to create the IPsec tunnel, you should already have created an instance.

We have chosen an instance with linux, but if you prefer any other, 
just make sure that the instance can execute code in python.


To attach an IAM role to an instance that has no role, the instance can be in the stopped or running state.

1. Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.
2. In the navigation pane, choose Instances.
3. Select the instance, choose Actions, Instance Settings, Attach/Replace IAM role.
4. Select the IAM role to attach to your instance, and choose Apply.

Requirements to connect to your EC2 instance with SSH

- SSH **file.pem** provided by Amazon when you launch the instance
- **IP-address** assigned to your ec2 instance
- The **username** on the instance distro

On linux

1. Open a terminal
2. Type the SSH command 
```
ssh -i file.pem username@IP-address
```
3. Now you’re connected

On Windows

1. Install Putty https://www.putty.org/
2. Open PuttyGen
3. Select checkbox “RSA”
4. Click load and select your **file.pem**
5. A message will prompt, click ok.
6. Click on save private key. 
7. Then a message will prompt, select yes
8. Type a name for your key **file.ppk**
9. Now close PuttyGen program and open Putty
10. Go to Connection/SSH section and double-click it.
11. Go to Auth section and select your **file.ppk**
12. Go back at the top in the Session section. Fill the field Hostname **IP-address** and click open
13. A warning will prompt. Click yes.
14. Type your **username**
15. Now you’re connected

Upload files using FTP Client

You can download Filezilla using the next link (https://filezilla-project.org/download.php)

1. Go to Edit/Settings/Connection/SFTP, Click "Add key file”
2. Browse to the location and select your **file.pem**
3. A message box will appear to convert the file into .ppk. Click **Yes**, and store it.
4. If the new file is shown in the list of Keyfiles, then continue to the next step. If not, then click "Add keyfile..." and select the converted file.
5. Go to File/Site Manager/Add a new site with the following parameters:

- Protocol: SFTP
- Host: **IP-address**
- Logon Type: Key File
- User: **username**

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


### Amazon Elastic Load Balancing

Elastic Load Balancing distributes incoming application or network traffic across multiple targets as Amazon EC2 instances.
You can configure health checks, which monitor the health of the instances, 
so that the load balancer sends requests only to the healthy ones

Go to **EC2 Dashboard / Load Balancing / Load Balancers /** Select: **Create Load Balancer**

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create.png)

Select the option **Network Load Balancer**

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_udp.png)

Configure the listener port for the UDP connections, select the VPC and the Subnet where your instances are located.

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_udp_config1.png)
![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_udp_config2.png)

You will need to configure the first target. In the following steps you will set up additional targets

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_udp_config_target.png)

To configure the destination instance, you can only select those that are within the subnet chosen in the configuration.

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_udp_config_target_ec2.png)

Review it and Click **Create**

Now, you have two listening ports, but you have only configured 1 target. 
For this reason, it is necessary to add a new target for the Bridge to function properly.

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_udp_config_end.png)

Go to **EC2 Dashboard / Load Balancing / Target Groups /** Select: **Create Target group**

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_target.png)

Configure the new target for UDP port:

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_target_config.png)

In the last step add the instance as in the previous step

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_target_config_end.png)

Return to your Listener for update with the new target.

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_target_edit.png)

Delete the Default action and add the new target 

![pic](pictures/AWS/AWS_Console_EC2_LoadBalancer_create_target_edit_configure.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# How to run it

Now that you know how to configure AWS. You can run it in just 3 steps !!!

## Download it

You can choose between several options: 

- Option 1: Download the Github repository on the instance

1. Install git on the instance
```shell
sudo yum upgrade
sudo yum install git
```
2. Clone the repository
```shell
git clone https://github.com/telefonicaid/iot-activation.git
```
3. Go to Bridge path: **scripts/Data_Bridge/**

- Option 2: Download the Data Bridge Code

1. Download the Code with the command: `wget`
```
wget https://raw.githubusercontent.com/telefonicaid/iot-activation/master/scripts/Data_Bridge/Data_Bridge.zip
```
2. Unzip the new file
```
unzip Data_Bridge.zip
```

Now that you have the code in the machine you just have to install the python libraries.


If you are using an instance of EC2, run the following command. It will allow you to install python libraries

```shell
sudo yum install python-pip
```

You can install them one by one from the Bridge folder.

```python
sudo pip install -r requirements.txt
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Configure it

We have tried to make this as simple as possible.

So, you'll only need to fill in a few fields in the configuration file 
[Configuration.yaml](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge/config/Configuration.yaml)

```yaml
cloud: AWS

UDP:
  ip: "0.0.0.0"
  port: 4114

COAP:
  ip: "0.0.0.0"
  port: 5683

KITE:
  url: "https://m2m-api.telefonica.com"
  certificate: "cer_file"
  private_key: "key_file"

```


#### Configure the Cloud

This parameter is used to identify the cloud and select the configuration file. 
In this example you must select AWS

```yaml
cloud: AWS
```


#### Configure the UDP socket

Here you can choose the port through which you will receive the UDP messages and the allowed IP addresses

```yaml
UDP:
  ip: "0.0.0.0"
  port: 4114
```

allowed values:
- ip: "0.0.0.0"    (allow any address)
- ip: "X.X.X.X"	   (restrict to a single address)

If you don't want to configure the connection through UDP, remove this section from the file.

#### Configure the COAP proxy

Here you can choose the port through which you will receive the UDP messages and the allowed IP addresses

```yaml
COAP:
  ip: "0.0.0.0"
  port: 5683
```

allowed values:
- ip: "0.0.0.0"    (allow any address)
- ip: "X.X.X.X"	   (restrict to a single address)

If you don't want to configure the COAP proxy, remove this section from the file.

#### Configure the Kite Platform connection

This parameter allows you to select the files the certificates to access the Kite Platform.

```yaml
KITE:
  url: "https://m2m-api.telefonica.com"
  certificate: "cer_file"
  private_key: "key_file"
```

Do you remember the name of the parameters created in AWS?
Now is the time to use them.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


#### Configure the AWS file

Here is an example of a configuration file for AWS connection 
[Configuration_AWS.yaml](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge/config/Configuration_AWS.yaml)

```yaml
cloud: AWS
region: "xx-xxxx-x"
MQTT:
  topic:
    update: "$aws/things/<DEVICE_NAME>/shadow/update"
    default: "tlm/<DEVICE_NAME>/raw"
    log_device: "log/device/provision/new"
    reserved: "$aws"
```

The file is quite intuitive, however here you can see carefully how to configure each section

##### Region configuration

Configure the region of your devices

```yaml
cloud: AWS
region: "xx-xxxx-x"
```

##### Topic configuration

At the moment you only have to keep the fields as is

```yaml
MQTT:
  topic:
    default: "tlm/<DEVICE_NAME>/raw"
    log_device: "log/device/provision/new"
```

- **default**: configure this field to select the default topic name.
- **log_device**: topic name in which the new things creations are reported.

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

