---
layout: post
title:  "IPsec"
date:   2019-02-06 12:00:00 +00:00
categories: tutorial
---
### Table of Contents

- [What is IPsec?](#what-is-ipsec)
  * [Why do we need IPsec?](#why-do-we-need-ipsec)
  * [What will you need?](#what-will-you-need)
  * [What does it do?](#what-does-it-do)
- [How to make your own IPsec VPN!](#how-to-make-your-own-ipsec-vpn)
  * [Request private APN to Telefónica](#request-private-apn-to-telefonica)
  * [IPsec step by step in AWS](#table-of-contents-ipsec-in-aws)


# What is IPsec?

IPsec is one of the most important security protocols, being created to provide security in network and transport layer. 
I in both TCP and UDP protocols

IPsec protects data flows between two security gateways allowing two networks to connect to each other.
It also includes a series of protocols to establish authentication between networks.

It's main use is to create Private Networks (VPN).

![pic](pictures/schematics/IPsec_diagram.png)

## Why do we need IPsec?

As you know every device connected to the internet needs an IP address, being necessary that this IP is unique for each device. 
And without many accounts it is easy to conclude that if this were true there would not be enough addresses for all devices in the world.

with a 32-bit for each address only 4,294,967,296 devices could be connected. A ridiculous number for the current size of the internet.
The NAT protocol (Network Address Translation) was created to find a solution.

**How NAT works?**

When a packet leaves your device for the internet it has an IP address that belongs to a smaller network. 
So, this address is translated to an IP valid for the Internet.

When the next machine receives this packet, it identifies the new IP as the packet origin.

**How to solve it?**

The solution is to create a virtual network to which both the source and destination machines belong, 
so that both machines can identify each other using their IP address.
And as you have deduced this is possible thanks to the IPsec protocol.

## What will you need?

- Telefónica SIM with private APN (IPsec)
- A Cloud IPsec: AWS

## What does it do?

When you request your SIMs from Telefónica, you can request a private APN, which includes your SIMs in your own new network.
The goal is to establish a direct connection between this new network and the Cloud network. 

The IPsec provides a secure connection that will function as if the devices of both networks are on the same network.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

# How to make your own IPsec VPN!

We believe in the importance of your data and the need to provide a safe network.
For this reason, we provide all the necessary steps for you to create your own network

## Request private APN to Telefónica

As we will assume if you are following this tutorial with us is because you have decided to make your connection through Telefónica coverage.

It is important for you to know that when you apply for new SIMS you can request the creation of your own APN (Access Point Name).

This new APN can be requested to have its own range of IP's that will correspond to your own network. 
An example of networks that you can request are the following:

- Class A: up to 16777215 devices xxx.0.0.0/8
- Class B: up to 65535 devices    xxx.xxx.0.0/16
- Class C: up to 255 devices      xxx.xxx.xxx.0/24

where you can choose the desired range **192.164.0.0/24** from 192.164.0.0 to 192.164.0.255 IP address.

In addition to the range you must facilitate the configuration of the 2 gateways of the Cloud network you are using.
Although this already depends on the Cloud. For AWS you can follow the tutorial

  * [IPsec step by step in AWS](#table-of-contents-ipsec-in-aws)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

other clouds tutorials under development ...

## IPsec step by step in AWS

### Table of Contents IPsec in AWS
- [Configure IPsec step by step in AWS](#configure-ipsec-step-by-step-in-aws)
  * [1. Create VPC](#1-create-vpc)
  * [2. Create VPG](#2-create-vpg)
    + [2.1. Attach VPG to VPC](#21-attach-vpg-to-vpc)
  * [3. Enable propagation of routes from VPG](#3-enable-propagation-of-routes-from-vpg)
    + [3.1. Edit Route Table](#31-edit-route-table)
  * [4. Create 2 Custom Gateway](#4-create-2-custom-gateway)
  * [5. Create 2 VPN Connection](#5-create-2-vpn-connection)
    + [5.1. Download Configuration](#51-download-configuration)
  * [6. Create an EC2 instance](#6-create-an-ec2-instance)
    + [6.1. Launch EC2 instance](#61-launch-ec2-instance)
    + [6.2. Enable Internet Connection EC2 instance](#62-enable-internet-connection-ec2-instance)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

# Configure IPsec step by step in AWS

In the Amazon nomenclature the client servers are located in the virtual machines of the client's Virtual Private Cloud, 
while Telefónica's network will act as "Local Network". 

In other words, the IP pools of the IoT mobile devices belong to the Address Space of the client's Local Network.

On Amazon, IPsec tunnels are created using VPN Connections. When a VPN connection is created between the Virtual Private Gateway 
in the cloud and the Customer Gateway (Telefónica Encrypter), Amazon, to provide redundancy on its side, 
automatically assigns two public IPs to its Virtual Private Gateway which will be the peer IPsec on the Amazon side.

For more details see the following diagram

![pic](pictures/IPsec/IPsec_AWS_00_Overview.png)

The following tutorial intends to be a simple guide to configure the IPsec between an EC2 machine and your pool of SIMs 
from the Telefónica's network.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

## 1. Create VPC

**What Is Amazon VPC?**

Amazon Virtual Private Cloud (Amazon VPC) enables you to launch AWS resources into a virtual network that you've defined. 
This virtual network closely resembles a traditional network that you'd operate in your own data center. 

Go to **VPC Dashboard / Virtual Private Cloud / Your VPCs /** Select: **Create VPC**
![pic](pictures/IPsec/IPsec_AWS_01_VPCdashboard_CreateVPC.png)

Complete the next fields:

**Name tag:** Select a name for identify your VPC in the next steps

**IPv4 CIDR block:** Select your network range. It must not match the range of your SIM pool

![pic](pictures/IPsec/IPsec_AWS_01_VPCdashboard_CreateVPC_config.png)

Click on create.

Now you can see the new VPC
![pic](pictures/IPsec/IPsec_AWS_01_VPCdashboard_CreateVPC_config_end.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

## 2. Create VPG

Go to **VPC Dashboard / Virtual Private Network / Virtual Private Gateway /** Select: **Create Virtual Private Gateway**
![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG.png)

**Name tag:** Select a name for identify your VPG in the next steps
![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG_config.png)

Click on create.

Now you can see the new VP Gateway
![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG_config_done.png)

Now you can see the new VPG and read in red **detached**

### 2.1. Attach VPG to VPC

In the last page
**VPC Dashboard / Virtual Private Network / Virtual Private Gateway **

Select your VPG: 
** Actions button /** Select: **Attach to VPC**

Select your VPC Name tag
![pic](pictures/IPsec/IPsec_AWS_02_VPCdashboard_CreateVPG_config_end_attach.png)

Click on **Yes, Attach**

wait a moment until it appears **attached**

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

## 3. Enable propagation of routes from VPG

This means that in our VPC the routes to our local network automatically point to the Virtual Private Gateway:

### 3.1. Edit Route Table

To enable instances in your VPC to reach your customer gateway, you must configure your route table to include 
the routes used by your VPN connection and point them to your virtual private gateway. 
You can enable route propagation for your route table to automatically propagate 
those routes to the table for you. 

Go to **VPC Dashboard / Virtual Private Cloud / Route Tables**

Select the table with your VPC and in the bottom menu select the tab:

**Route Propagation / Edit route propagation**
![pic](pictures/IPsec/IPsec_AWS_03_VPCdashboard_RouteTables.png)

a new window opens to activate it
![pic](pictures/IPsec/IPsec_AWS_03_VPCdashboard_RouteTables_propagation.png)

Click on **Save**
Now you can see route propagate to **YES**

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

## 4. Create 2 Custom Gateway

To be able to connect to the Telefónica network it is necessary to establish 2 Gateway with the 2 Telefónica's Encrypters.

Go to **VPC Dashboard / Virtual Private Network (VPN) / Customer Gateway /** Select: **Create Customer Gateway**
![pic](pictures/IPsec/IPsec_AWS_04_VPCdashboard_CustomerGateway_CreateCG.png)

complete the fields with the following information:

- **Encrypter3:**
  -Name: TEF_Cifra3
  -Routing: Dynamic
  -BGP ASN: 3352
  -IP Address: 213.0.185.6

- **Encrypter4:**
  -Name: TEF_Cifra4
  -Routing: Dynamic
  -BGP ASN: 3352
  -IP Address: 213.0.185.8

![pic](pictures/IPsec/IPsec_AWS_04_VPCdashboard_CustomerGateway_CreateCG_config.png)

Once the Customers Gateway corresponding to the Telefónica's Encrypters have been created, they appear as shown below:

![pic](pictures/IPsec/IPsec_AWS_04_VPCdashboard_CustomerGateway_CreateCG_config_done.png)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

## 5. Create 2 VPN Connection

You must create a VPN connection for each of the two customer gateways corresponding to Telefónica's two encryption devices.

Go to **VPC Dashboard / Virtual Private Network (VPN) / Site-to-Site VPN /** Select: **Create VPN Connection**

![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc.png)

**Name tag:** Select a name for identify your VPC connection in the next steps

**VPG** Select your VPN Gateway attached to your VPC

**Customer Gateway** Existing

**Customer Gateway ID** Select each of the two Customers Gateway created

**Routing Options** Dynamic

for the **first** VPN connection:

**Inside IP CIDR for Tunnel 1**  169.254.30.0/30

**Inside IP CIDR for Tunnel 2**  169.254.30.4/30

and for the **second** VPN connection:

**Inside IP CIDR for Tunnel 1**  169.254.40.0/30

**Inside IP CIDR for Tunnel 2**  169.254.40.4/30

![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config1.png)
![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config2.png)
![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config3.png)

Click on **Create VPN Connection**

![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config_done.png)

Now you can read in the tab **Tunnel Detail** the status in red **DOWN**

This will hold, until you talk to Telefónica and send them the configuration.

### 5.1. Download Configuration

Amazon offers the possibility of downloading a configuration file from the Customer Gateway, 
as it is necessary to facilitate configuration to Telefónica.

Clicking on each encrypter, select the tab **Download Configuration** and complete like the following example
![pic](pictures/IPsec/IPsec_AWS_05_VPCdashboard_VPNconnection_createVPNc_config_download.png)

you keep these two files that they are necessary to configure the other end of the tunnel

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

## 6. Create an EC2 instance

Amazon Elastic Compute Cloud (Amazon EC2) is a web service that provides secure, resizable compute capacity in the cloud. 
It is designed to make web-scale cloud computing easier for developers.

### 6.1. Launch EC2 instance

Go to EC2 Dashboard / Instances / Instances / Select: **Launch Instance**
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch.png)

**Step 1:** Choose the SO
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step1.png)
Click **Next**

**Step 2:** Choose the machine size
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step2.png)
Click **Next**

**Step 3:** Configure the machine connection

**Network** Select your VPC

**Subnet** Create a new Subnet (look like y the next step 6.1)

**Auto-assigns Public IP** Enable
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3.png)
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3a.png)

Click **Next** until Step 6

**Step 6:** Open a Port to test the connection 

**Assign a security group** Create a new security group
**Security group name** Select a name for identify your Security group in the next steps

**Add Rule** Custom ICMP like the picture for enable the ping response
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step6.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

### 6.1.a Create Subnet

**Name tag** Select a name for identify your Subnet in the next steps

**VPC** Select your VPC

**IPv4 CIDR block** use the same IP range but choose a smaller mask
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3_subnet1.png)
![pic](pictures/IPsec/IPsec_AWS_06_EC2dashboard_Instance_launch_step3_subnet2.png)

Click on **Create**

Now your machine is running, but it is connected to a virtual network. You must configurate an internet gateway

[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)

### 6.2. Enable Internet Connection EC2 instance

Go to VPC **Dashboard / Virtual Private Cloud / Internet Gateway /** Select: **Create internet gateway**
![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG.png)

**Name tag** Select a name for identify your Subnet in the next steps
![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG_config.png)

Click on **Create**

Now select the Internet Gateway and select **attach to VPC** on Actions tab
![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG_config_attach.png)

**VPC** Select the VPC
![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_InternetGateway_CreateIG_config_attach_VPC.png)
Click on **Attach**

Now you have access to an internet gateway, you only have to modify the rules of the gateway to allow traffic.

Go to **VPC Dashboard / Virtual Private Cloud / Route Table /** Select the route table of the VPC

on the tab **Routes** click on **Edit Routes**
![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_RouteTables.png)

add a new route with the interface 0.0.0.0/0
and select the internet gateway like target.
![pic](pictures/IPsec/IPsec_AWS_06_VirtualPrivateCloud_RouteTables_editroute.png)


[![pic](pictures/utils/arrow_up.png)](#table-of-contents-ipsec-in-aws)
