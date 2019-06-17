<p align="center">
      <img  title="Telefonica" src="pictures/miscellaneous/Telefonica_logo.png">
</p>

### Table of Contents

- [Welcome to IoT Activation of Telefónica](#welcome-to-iot-activation-of-telefónica)
  * [Raspberry Starter-kit](#what-can-you-find-in-the-raspberry-starter-kit)
  * [Arduino Starter-kit](#and-in-the-arduino-kit)
- [What do you need to know?](#before-starting-with-the-iot-activation-program-what-do-you-need-to-know)
  * [What is NB-IoT or LTE-M?](#what-is-nb-iot-or-lte-m)
  * [Connectivity 2G and 3G](#connectivity-2g-and-3g)
  * [TCP and UDP](#tcp-and-udp)
  * [Public Cloud](#public-cloud)
- [Why are we different? Kite Platform](#why-are-we-different-kite-platform)

# Welcome to IoT Activation of Telefónica


## What can you find in the Raspberry Starter-kit?

- Raspberry Pi 3 B+
- Case for Raspberry
- MicroSD with pre-installer NOOBS (Raspberry-pi SO)
- Raspberry Pi universal Power Supply 2.5A 5.1V
- Raspberry Pi Camera V2
- Raspberry Pi Sense HAT
- Huawei USB Stick
- Telefónica SIM Card
	
To learn how to configure your device and start developing your applications check out the following tutorial 
[Raspberry Pi StarterKit guide](RaspberryPi_StarterKit.md)

<p align="center">
	<a href="RaspberryPi_StarterKit.md" lign="center">
		<img src="pictures/Raspberry/Raspi_logol.png"
		width="250" height="75">
	</a>
</p>


## And in the Arduino kit? 

In your Arduino Starter-kit you can find the next components:

- Arduino MKR NB-1500
- Arduino Antenna GSM
- Power Supply 
- Telefónica SIM Card

To learn how to configure your device and start developing your applications check out the following tutorial 
[Arduino StarterKit guide](Arduino_StarterKit.md)

<p align="center">
	<a href="Arduino_StarterKit.md" lign="center">
		<img src="pictures/Arduino/Arduino_Logo.png"
		width="150" height="100">
	</a>
</p>

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# Before starting with the IoT-Activation program... What do you need to know?

## What is NB-IoT or LTE-M?

Surely you are already wondering how to connect these devices to internet, 
and if there is a specific technology for it. The answer to these questions is yes. 

In the last few years, different radio communication technologies have been developed 
by different organizations. 

Amongst these new technologies developed for communication in the world of IoT 
we can highlight NB-IoT and LTE-M as the most entrenched for this purpose.


### Narrowband IoT (NB-IoT)

Narrowband IoT is a radio technology standard.
It enables a wide range of simultaneous connections of a low power devices.

NB-IoT does not need a high-speed connection on the other hand it needs a stable connection. 
It focuses specifically on indoor coverage.
 
low power consumption enables a battery life of several years.

Likewise, it preserves all characteristic of security and privacy of a mobile net.

<p align="center">
	<a href="README.md">
		<img src="pictures/miscellaneous/nbiot_logo.png"
		width="250" height="75">
	</a>
</p>

### Long Term Evolution for Machines (LTE-M)

LTE is a standard for high-speed wireless communication for mobile devices.

It allows bigger rate of data enable a real-time communication voice included.

<p align="center">
	<a href="README.md">
		<img src="pictures/miscellaneous/ltem_logo.png"
		width="250" height="75">
	</a>
</p>

### NB-IoT vs LTE-M

Both standards are focus in wireless communication between devices.
They are good connectivity options to take advantage of Low Power Wide Area Network 

Deciding between LTE-M and NB-IoT requires an understanding of the key differences between these two technologies.
After analysing the similarities and differences between LTE-M and NB-IoT, you should be able to make a correct decision.

| **NB-IoT**  | **LTE-M** |
| :---:  | :---:  |
| high connection density | mobile devices |
| limited bandwidth | high-speed |
| long battery life | long battery life |
| focus in indoor coverage | focus in real-time communication |
| low cost | low cost |

If you have any doubt about what type of connection, you should use for your devices we can clarify that 
the choice between LTE-M and NB-IoT depends on the amount of data and the frequency your application needs. 

Choose LTE-M if you need real-time communication, on the other hand if you need many devices or sensors and do not need  
a precision tracking data, you should choose NB-IoT. 

But when dealing with moving devices you can use a multi-technology NBIoT/LTE-M solution to guarantee the services.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Connectivity 2G and 3G

Surely more than once you have read acronyms such as 2G, 3G, 4G, GPRS, HDSPA or LTE among others 
on the screen of your mobile.
If you don't know exactly what they mean, we'll explain the differences between 2G and 3G 
so you don't get stuck with the doubt.

#### 2G Networks (GPRS, GSM) 
They are the second generation networks and therefore lower speed networks.

#### 3G Networks (HSPA, UMTS) 
They are third-generation networks. The main difference between 3G and 2G networks
is that 3G offers a higher transmission speed.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## TCP and UDP

As you know, when two devices need to communicate with each other, it's logical that they do it over the Internet.
What you may not know is that in establishing this data exchange,
there is a set of rules and regulations known as Internet Protocols (IP).
Although there is a diversity of them, which in turn are included within other protocols,
he most common protocols used in data transmission are TCP and UDP.

At first glance it may not seem important to use them indistinctly,
but in the next section you will see the advantages and weaknesses of each protocol.


### How does TCP works?

TCP is the main protocol on Internet and is a connection-based protocol. This means that before starting a transmission, 
a device needs to connect to the receiver and confirm that the receiver is listening to them.

Then the device divides the information into packets and sends them in order after confirming 
that they have been received correctly.

Each time the addressee receives one of the packets, it has the task of verifying if the content is correct
and make the decision whether to request the shipment again or request the next packet until the shipment is complete.

Although it is a slow process, TCP guarantees that all data has been received correctly.

### How does UDP works?

UDP is one of the simplest and fastest protocols used for communication between devices over the Internet. 
Unlike other protocols, UDP only divides the information into packets and sends them to the destination.

For this reason, it is not necessary to wait for a confirmation. 
UDP is limited to sending the packets no matter what happens.

Although simple and fast, this protocol doesn't guarantee that the data will be received correctly.
 
### What is the difference between TCP and UDP?

| **Transmission Control Protocol (TCP)**  | **User Datagram Protocol (UDP)** |
| :---:  | :---:  |
| Protocol oriented to connections and it guarantees receive all the packets in order  | Easier and does not need to establish a connection |
| Hight reliability and slow transmission time  | Fast transmission time for a large number of clients |
| Error checking and quality guarantee for shipment  | Error checking without recovery |

For these reasons when choosing one of the protocols, it is necessary to assess the needs of the application.
If we need the data transmission to be reliable, we will choose TCP, 
however, if we need a fast data transmission and we can afford the loss of some of this, UDP is our best option.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Public Cloud

The public cloud is defined as computing services offered by third-party providers over the public Internet, 
making them available to anyone who wants to use or purchase them. They may be free or sold on-demand, 
allowing customers to pay only per usage for the CPU cycles, storage, or bandwidth they consume.

### Amazon Web Services and AWS-IoT 

Today Amazon Web Services is one of the largest providers of cloud computing services,
and some of its products focus exclusively on the development of IoT technologies.

AWS-IoT provides secure, two-way communication between multiple devices connected to the Internet.
This allows you to collect and process telemetry from Internet-connected devices and control them remotely.
You can create rules that define an action to be performed based on the message received.

### Google Cloud Platform and IoT-Core

Google Cloud Internet of Things (IoT) Core is a fully managed service for securely connecting and managing IoT devices,
from a few to millions. Ingest data from connected devices and build rich applications that integrate 
with the other big data services of Google Cloud Platform.

### Azure IoT

The Azure Internet of Things (IoT) is a collection of Microsoft-managed cloud services that connect, 
monitor, and control billions of IoT assets.
In simpler terms, an IoT solution is made up of one or more IoT devices and one or more back-end services 
running in the cloud that communicate with each other.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# Why are we different? Kite Platform

Connectivity management functionalities like inventory, real time expenses control, alarms, 
automatic business rules or reporting.

Remote management of devices that allow features like APN configuration, remote firmware updates, 
remote device resets and remote diagnostics.

Cloud connectors that eases integration amongst the main public cloud platforms and apps.

Discover [Kite Platform](Kite_Platform.md)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

# References

[MQTT](references_mqtt.md)

