### Table of Contents
- [What is MQTT?](#what-is-mqtt)
  * [Overview](#overview)
  * [Broker](#broker)
  * [Topics](#topics)
  * [Quality of service (QoS)](#quality-of-service-qos)

# What is MQTT?

MQTT (Message Queuing Telemetry Transport) It is a publish/subscribe, extremely simple and lightweight messaging protocol,
designed for constrained devices and low-bandwidth, high-latency or unreliable networks.

The design principles are to minimise network bandwidth and device resource requirements whilst
also attempting to ensure reliability and some degree of assurance of delivery.
These principles also turn out to make the protocol ideal for Internet of Things.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Overview

An MQTT system consists of clients communicating with a server, often called a "broker".
A client may be either a publisher of information or a subscriber.

When a publisher has a new data, it sends the message to the broker in a specific topic (publish).
The broker then distributes the message to any clients registered to receive messages for that topic (subscribed).

The publisher does not need to have any data of subscribers, and subscribers don't need to know anything about the publishers.
Clients (publisher/subscribers) only interact with the broker.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Broker 

The broker is a service that enables the sending and receiving of messages

The message broker maintains a list of all client sessions and the subscriptions for each session. 
When a message is published on a topic, the broker checks for sessions with subscriptions that map to the topic. 
The broker then forwards the publish message to all sessions that have a currently connected client.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Topics

A topic is a tag that the broker uses to filter messages for each client.
They are organized in a hierarchy of one or more levels, separated by a forward slash "/".

The client does not need to create the desired topic before they publish or subscribe to it. The broker accepts each valid topic without any prior initialization.

for example:

```mqtt
	iotActivation
	iotActivation/thing1
	iotActivation/thing2
	iotActivation/thing1/sensor_1
	iotActivation/thing1/sensor_2
```

Topic ending in a slash is considered equivalent to the same topic without the slash.

### Publish in a topic

For send a new message, it is necessary that the client is connected to the broker and publish in a topic.

### Subscriber to a topic

To subscribe is to be registered in the broker to receive messages for that topic

- a subscription to A/# is a subscription to the topic A and all topics beneath A
- a subscription to A/+ is a subscription to the topics directly beneath, but not A itself
- a subscription to A/+/# is a subscription to all topics beneath A, but not A itself

for example:

**iotActivation/#** include:
```
	iotActivation/thing1
	iotActivation/thing2
	iotActivation/thing1/sensor_1
	iotActivation/thing1/sensor_2
```

**iotActivation/+/sensor_1** include:
```
	iotActivation/thing1/sensor_1
	iotActivation/thing2/sensor_1
```
			
**iotActivation/+/#** include:
```
	iotActivation/thing1/sensor_1
	iotActivation/thing1/sensor_2
	iotActivation/thing2/sensor_1
	iotActivation/thing2/sensor_2
```

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

## Quality of service (QoS)

Each connection to the broker can specify a "quality of service" measure.
This QoS level providers an agreement between the sender and the receiver.

### (QoS 0) - At most once
It is the minimal QoS level, the message is sent only once and the client and broker take no additional steps 
to acknowledge delivery (fire and forget).

### (QoS 1) - At least once
The message is re-tried by the sender multiple times until acknowledgement is received.
It is possible for a message to be sent or delivered multiple times. (acknowledged delivery)

### (QoS 2) - Exactly once
It is the highest level, the sender and receiver engage in a two-level handshake to ensure only one copy of the message is received (assured delivery).

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)
