### Table of Contents

- [What is Data Bridge?](#what-is-the-data-bridge)
  * [Data Bridge Code](#data-bridge-code)
  * [Benefits of using it](#benefits-of-using-the-data-bridge)
  * [Benefits of using the Data Bridge](#benefits-of-using-the-data-bridge)
  * [Upcoming features](#upcoming-features)
  * [What will you need?](#what-will-you-need)
  * [Cloud Deployment](#cloud-deployment)

# What is The Data Bridge?

Data Bridge is a tool Open Source that allows your devices connect with the public clouds using a UDP message.
It also provides additional services that ensure both the security and management of the device.

And most important of all. You can deploy it in just one Click!

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Data Bridge Code

The Data Bridge Python code is Open Source, Adapt it to your needs!

Review our public repository in [Github](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge)

1. Download the Code with the command: `wget`
```
wget https://raw.githubusercontent.com/telefonicaid/iot-activation/master/scripts/Data_Bridge/Data_Bridge.zip
```
2. Unzip the new file
```
unzip Data_Bridge.zip
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)



## Benefits of using the Data Bridge

#### Secure Connection

UDP uses a simple model with a minimum of protocol mechanisms. For this reason, it is not a secure protocol.
At this point, the Data Bridge is designed to work using a Private Networks [(IPsec)](BP_IPsec.md)

The SIM cards of your devices will be directly connected to the Data Bridge network! Identify them univocally through their IP.

#### Energy saving

Among the communication protocols, MQTT is well known due to it is really easy to use and it secures the communication through a TLS context, 
although from the energetic perspective it is quite aggressive. You shouldn't choose between security and battery... 
so the Data Bridge will make your day.

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
			(30 times less without TLS)</div></th>
	<th><div align="center">
			Security provided by Telefónica's network <br>
			(50 times less than MQTT+TLS)</div></th>
  </tr>
</table>

#### Device Management

Use [Kite Platform](Kite_Platform.md) to retrieve your custom information (the device name and topic)
The Data Bridge access to the IoT connectivity platform, taking control of the devices. 
When you replace an old device and use the same SIM card, the configuration will be maintained.

#### Device self-provisioning

If the device is not registered in the cloud, the first time the device receives a message 
it will register it using the information of Kite

#### Easy integration

Communicate easily with your device. It sends a UDP frame and receives the status stored in the cloud.
Report the message to the cloud and receive instructions!!

in addition, Data Bridge allows you to interact with it from the application layer using the API CoAP
**GET** a status device
**PUT** a new state

#### Deploy it in One-Click

Don't worry about your installation, use our template!

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Upcoming features

- Compatibility with other clouds
- new utilities

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## What will you need?

- KITE Platform [Certificates files](Kite_Platform.md#what-is-kite-platform-api)
- IPSec Service provided by Telefónica [(IPsec)](BP_IPsec.md#what-is-ipsec)
- Public Cloud account

&#x1F4CD;
For the time being, if you use a SIM from the Thinx, you will not have access to the Kite Platform.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Cloud Deployment

To continue with the installation, select your Public Cloud

- [Amazon Web Services](BP_DataBridge_AWS.md)

- [Google Cloud](BP_DataBridge_GoogleCloud.md)  in the near future!!

<table>
  <tr>
	<th>
		<a href="#/BP_DataBridge_AWS.md" align="center">
			<img src="pictures/AWS/AWS_logo.png"
			width="350" height="225">
		</a>
	</th>
	<th>
		<img src="pictures/portfolio/portfolio_white.png" width="75" height="1">
	</th>
	<th>
		<a href="#/BP_DataBridge_GoogleCloud.md" align="center">
			<img src="pictures/GCP/GCP_logo.png"
			width="350" height="225">
		</a>
	</th>
  </tr>
</table>

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
