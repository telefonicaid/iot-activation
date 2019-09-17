### Table of Contents

- [What is IPsec?](#what-is-ipsec)
- [How to make your own IPsec VPN!](#how-to-make-your-own-ipsec-vpn)

### Table of Contents IPsec in AWS
- [Configure IPsec in AWS one click](AWS_CF_IPsec.md)
- [Configure IPsec step by step in AWS](#configure-ipsec-step-by-step-in-aws)
  * [1. Create VPC](#1-create-vpc)
  * [2. Create VPG](#2-create-vpg)
  * [3. Enable propagation of routes from VPG](#3-enable-propagation-of-routes-from-vpg)
  * [4. Create two customer Gateway](#4-create-two-customer-gateway)
  * [5. Create two VPN Connection](#5-create-two-vpn-connection)
  * [6. Create an EC2 instance](#6-create-an-ec2-instance)


# What is IPsec?

IPsec is one of the most important security protocols. It was created to provide security in network and in transport layer.
It guarantees the security using both TCP and UDP protocols.

IPsec protects data flows between two security gateways. It allows two networks to be connected.
It also includes a series of protocols to establish authentication between networks.

Its main purpose is to create a Private Networks (VPN).

![pic](pictures/schematics/IPsec_diagram.png)


## What will you need?

- Telefónica SIM with private APN (IPsec)
- A Cloud machine with IPsec tunnel


## What does it do?

When you request your SIMs from Telefónica, you can ask for a private APN. This APN includes your SIMs in a new network.
The goal is to establish a direct connection between your network and the Cloud.

The IPsec guarantee that two networks work as one. It provides a secure connection between them.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# How to make your own IPsec VPN!

We believe in the importance of your data, for this reason we want to provide you a secure network.

Benefits:
- Enhanced security
- Integration cost and time reduction: customers don’t need to create ad-hoc VPN integration processes.


## Request a private APN to Telefónica

We assume that because you are following this tutorial with us, you are interested in connecting your devices 
through Telefónica's network.

It is important for you to know that when you request for new SIM's you can ask for the creation of 
your own APN (Access Point Name).

This new APN can be set to have its own IP's range. This range cannot correspond to your own network. 
An example of networks that you can request are the following:

- Class A: up to 16777215 devices xxx.0.0.0/8
- Class B: up to 65535 devices    xxx.xxx.0.0/16
- Class C: up to 255 devices      xxx.xxx.xxx.0/24

Where you can choose a desired range: **192.168.0.0/24** 

This range includes the IP address from 192.168.0.0 to 192.168.0.255.

In addition to the range you must provide to Telefónica the internet gateways configuration.

This setting will depend on your public cloud

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# Configure IPsec step by step in AWS

On Amazon, IPsec tunnels are created using VPN Connections. When a VPN connection is created between the Virtual Private Gateway
and the Customer Gateway (Telefónica Encrypter)
automatically assigns two public IPs to its VPG. This are de IPs on the Amazon side.

Amazon provide a redundant connection. In other words, you'll need create two gateways.

It is illustrated in the diagram below. 

![pic](pictures/IPsec/IPsec_AWS_00_Overview.png)

The following tutorial intends to be a simple guide to configure the IPsec between an EC2 machine and your pool of SIMs 
from the Telefónica's network.

Follow this tutorial to build an IPsec in AWS and learn how to do it step by step, but if you prefer, 
you can build it in [one click](AWS_CF_IPsec.md)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)


## 1. Create VPC

**What Is Amazon VPC?**

Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources into a virtual network.
This virtual network closely resembles a traditional network that you'd operate in your own data center.

Go to **VPC Dashboard / Virtual Private Cloud / Your VPCs /** Select: **Create VPC**

![pic](pictures/IPsec/IPsec_AWS_01_VPCdashboard_CreateVPC.png)

Fill in the fields:

- **Name tag:** Select a name for identifying your VPC in the next steps

- **IPv4 CIDR block:** Select your network range. It must not match the range of your SIM pool

![pic](pictures/IPsec/IPsec_AWS_01_VPCdashboard_CreateVPC_config.png)

Click on **create**.

Now you can see the new VPC

![pic](pictures/IPsec/IPsec_AWS_01_VPCdashboard_CreateVPC_config_end.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)


## 2. Create Virtual Private Gateway

The VPG provides a link between the VPC and an external environment.

Go to **VPC Dashboard / Virtual Private Network / Virtual Private Gateway /** Select: **Create Virtual Private Gateway**

![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG.png)

**Name tag:** Select a name for identifying your VPG in the next steps

![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG_config.png)

Click on **create**.

Now you can see the new VPG

![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG_config_done.png)

Now you can check the VPG status and read in red **detached**
The VPG is created, but you need to attach it to the VPC.


### 2.1. Attach VPG to VPC

On the previous screen 
**VPC Dashboard / Virtual Private Network / Virtual Private Gateway**

Select your VPG: 
**Actions** button / Select: **Attach to VPC**

Select your VPC **Name tag**

![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG_config_end_attach.png)

Click on **Yes, Attach**

Wait a moment until it appears **attached**

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)


## 3. Enable propagation of routes from VPG

To allow your VPC to reach other services. 
You must include the routes used by your VPN connection in the routing tables. They have to point to your VPG.


### 3.1. Edit Route Table

You can enable route propagation for your route table to automatically propagate it.

Go to **VPC Dashboard / Virtual Private Cloud / Route Tables**

Select the table with your VPC and in the bottom menu select the tab:

**Route Propagation / Edit route propagation**

![pic](pictures/IPsec/IPsec_AWS_03_VPCdashboard_RouteTables.png)

A new window opens to activate it

![pic](pictures/IPsec/IPsec_AWS_03_VPCdashboard_RouteTables_propagation.png)

Click on **Save**

Now you can see route propagate to **YES**

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)


## 4. Create two Customer Gateway

The customer gateway is the connection between your network and the VPC.
To be able to connect to the Telefónica network it is necessary to establish two Gateway with the two Telefónica's encrypters.

Go to **VPC Dashboard / Virtual Private Network (VPN) / Customer Gateway /** Select: **Create Customer Gateway**

![pic](pictures/IPsec/IPsec_AWS_04_VPCdashboard_CustomerGateway_CreateCG.png)

fill in the fields with the following information:

- **Encrypter3:**
  - Name: TEF_Cifra3
  - Routing: Dynamic
  - BGP ASN: 3352
  - IP Address: 213.0.185.6

- **Encrypter4:**
  - Name: TEF_Cifra4
  - Routing: Dynamic
  - BGP ASN: 3352
  - IP Address: 213.0.185.8

![pic](pictures/IPsec/IPsec_AWS_04_VPCdashboard_CustomerGateway_CreateCG_config.png)

Once the Customers Gateway corresponding to the Telefónica's encrypters have been created, they appear as shown below:

![pic](pictures/IPsec/IPsec_AWS_04_VPCdashboard_CustomerGateway_CreateCG_config_done.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

## 5. Create two VPN Connection

You must create a VPN connection for each of the two customer gateways corresponding to Telefónica's two encryption devices.

Go to **VPC Dashboard / Virtual Private Network (VPN) / Site-to-Site VPN /** Select: **Create VPN Connection**

![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc.png)

- **Name tag:** Select a name for identifying your VPC connection in the next steps

- **VPG** Select your VPN Gateway attached to your VPC

- **Customer Gateway** Existing

- **Customer Gateway ID** Select each of the two Customers Gateway created

- **Routing Options** Dynamic

**for the First VPN connection:**

- **Inside IP CIDR for Tunnel 1**  169.254.30.0/30

- **Inside IP CIDR for Tunnel 2**  169.254.30.4/30

**and for the Second VPN connection:**

- **Inside IP CIDR for Tunnel 1**  169.254.40.0/30

- **Inside IP CIDR for Tunnel 2**  169.254.40.4/30

![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config1.png)
![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config2.png)
![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config3.png)

Click on **Create VPN Connection**

![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config_done.png)

Now you can read in the tab **Tunnel Detail** the status in red **DOWN**

This will hold, until you contact to Telefónica and send them the configuration.

### 5.1. Download Configuration

Amazon offers you the possibility to download a configuration file for the Customer Gateway.
You will need provide this file to Telefónica.

Clicking on each encrypter, select the tab **Download Configuration** and fill like the following example

![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config_download.png)

You keep these two files that they are necessary to configure the other tunnel end.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)


## 6. Create an EC2 instance

Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud. 
It is designed to make web-scale cloud computing easier for developers.

In this case, we have decided to use a linux instance, but you can use others.
Just check that the image can execute Python code

### 6.1. Launch EC2 instance

Go to **EC2 Dashboard / Instances / Instances /** Select: **Launch Instance**

![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch.png)

**Step 1:** Choose the OS (AMI)

![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step1.png)

Click **Next**

**Step 2:** Choose the machine size

![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step2.png)

Click **Next**

**Step 3:** Configure the machine network connection

- **Network:** Select your VPC

- **Subnet:** Create a new Subnet (it will continue in the [step 6.2](#62-create-a-subnet))

- **Auto-assigns Public IP:** Enable

![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3.png)
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3a.png)

Click **Next** until Step 6

**Step 6:** Open a Port to test the connection 

- **Assign a security group:** Create a new security group

- **Security group name:** Select a name for identifying your Security group in the next steps

- **Add Rule:** Custom ICMP like the picture for enable the ping response

![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step6.png)

Now your machine is running, but it is connected to a virtual network. You must configurate an internet gateway to
enable the [internet connection](#63-enable-internet-connection-ec2-instance)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

### 6.2. Create a Subnet

A subnet is a range of IP addresses in your VPC. You need launch your EC2 instance into a specified subnet.

- **Name tag:** Select a name for identifying your Subnet in the next steps

- **VPC:** Select your VPC

- **IPv4 CIDR block:** use the same IP range but choose a smaller mask

![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3_subnet1.png)
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3_subnet2.png)

Click on **Create**

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

### 6.3. Enable Internet Connection EC2 instance

You have previously created a gateway to connect your network with the VPN of AWS. 
This is a similar step for connecting the VPN to an external network (Internet).

Go to VPC **Dashboard / Virtual Private Cloud / Internet Gateway /** Select: **Create internet gateway**

![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG.png)

- **Name tag:** Select a name for identifying the gateway in the next steps

![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG_config.png)

Click on **Create**

Now that you have created the VPG, connect it to the VPN

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

### 6.4. Attach to VPC

Now select the Internet Gateway and select **attach to VPC** on **Actions** button

![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG_config_attach.png)

- **VPC** Select the VPC

![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG_config_attach_VPC.png)

Click on **Attach**

Now you have access to an internet gateway, you only have to modify the rules of the gateway to allow traffic.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

### 6.5. Enable a new Route

Go to **VPC Dashboard / Virtual Private Cloud / Route Table /** Select the route table of the VPC

On the **Routes** tab, click on **Edit Routes** button

![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_RouteTables.png)

Add a new route with the interface 0.0.0.0/0
and select the internet gateway like target.

![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_RouteTables_editroute.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)
