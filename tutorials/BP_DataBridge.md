---
layout: post
title:  "Data Bridge"
date:   2019-02-06 12:00:00 +00:00
categories: tutorial
---
### Table of Contents

- [What is Data Bridge?](#what-is-the-data-bridge)
  * [Why do we need Data Bridge?](#why-do-we-need-the-data-bridge)
  * [What our bridge is already doing](#what-our-bridge-is-already-doing)
  * [What's it gonna do next?](#whats-it-gonna-do-next)
  * [What will you need?](#what-will-you-need)


# What is The Data Bridge?

Data Bridge is a Python script. It can be deployed in any machine as a server.
It enables the connection between public clouds IoT Core services and UDP messages.
As a result, It will send back a message to the device with the publish code.


## Why do we need the Data Bridge?

Among the communication protocols, MQTT is well known due to it is really easy to use and it secures the communication through a TLS context, although from the energetic perspective it is quite aggressive. You shouldn't choose between security and battery... so the Data Bridge will make your day :). 

We wanna show you a energy consumption comparison: We sent 300 bytes packet with the same device and the result looks as follows ...

<table>
  <tr>
	<th><div align="center">Consumption MQTT with TLS</div></th>
	<th><div align="center">Consumption MQTT</div></th>
	<th><div align="center">Consumption UDP</div></th>
  </tr>
  <tr>
	<th>
		<img src="pictures/miscellaneous/consumption_chart_NB_MQTTTLS.png" width="300" height="200">
	</th>
	<th>
		<img src="pictures/miscellaneous/consumption_chart_NB_MQTT.png" width="300" height="200">
	</th>
	<th>
		<img src="pictures/miscellaneous/consumption_chart_NB_UDP.png" width="300" height="200">
	</th>
  </tr>
	<tr>
	<th><div align="center">
			Secure data transfer <br>
			with high power consumption</div></th>
	<th><div align="center">
			Unsecured data transfer <br>
			(30% savings compared to TLS)</div></th>
	<th><div align="center">
			Security provided by Telefónica's network <br>
			(50% savings compared to MQTT + TLS)</div></th>
  </tr>
</table>

## What our bridge is already doing

- It accesses to Kite Platform to retrieve your custom information (the device name and topic)
- It received a UDP message and it publishes in the Cloud.
- It returns a message with the process result and commands

## What's it gonna do next?

- Compatibility with other clouds
- Deploy your Bridge in One Click

## What will you need?

- A Linux instance on a Public Cloud
- Python Interpreter
- [KITE Platform](Kite_Platform.md#access-step-by-step-using-the-curl-command) Certificates files
- IpSec Service provided by Telefonica [(IPsec)](BP_IPsec.md)

&#x1F4CD;
For the time being, If you use a SIM from the Thinx, you will not have access to the Kite Platform.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

### To continue with the installation select your Public Cloud

<table>
  <tr>
	<th>
		<a href="BP_DataBridge_AWS.md" align="center">
			<img src="pictures/AWS/AWS_logo.png"
			width="350" height="225">
		</a>
	</th>
	<th>
		<img src="pictures/portfolio/portfolio_white.png" width="75" height="1">
	</th>
	<th>
		<a href="BP_DataBridge_GoogleCloud.md" align="center">
			<img src="pictures/GCP/GCP_logo.png"
			width="350" height="225">
		</a>
	</th>
  </tr>
</table>

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
