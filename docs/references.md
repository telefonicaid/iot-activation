### Table of Contents
- [OSI model](#osi-model)
- [HTTP](#http)
- [CoAP](#coap)
- [MQTT](#mqtt)
- [FTP](#ftp)
- [TLS](#tls)
- [SSH](#ssh)

# OSI model
The Open Systems Interconnection model is a reference model for network protocols (it is not a network architecture),
created in 1980 by the International Organization for Standardization (ISO).

a conceptual model that characterizes and standardizes the
communication functions of a telecommunication. 
The model partitions a communication system into abstraction layers

### 1: Physical Layer
The physical layer s the lowest layer, it is responsible for the transmission and reception of unstructured raw data between a 
device and a physical transmission medium. It converts the digital bits into electrical, radio, or optical signals.

**Example:** Microwaves, Optical fiber, Coaxial cable ...

### 2: Data Link Layer
The data link layer provides node-to-node data transfer—a link between two directly connected nodes. 
It detects and possibly corrects errors that may occur in the physical layer.

**Example:** PPP, Ethernet, Wi-fi ...

### 3: Network Layer
The network layer provides the functional and procedural means of transferring variable length data sequences (called packets) 
from one node to another connected in "different networks", every node has an address and which permits nodes connected to it
The goal of the network layer is to transfer data from the source to the destination, 
even if both are not directly connected but use intermediate devices.

**Example:**  IPv4, IPv6, ICMP ...

### 4: Transport Layer
The transport layer is the layer in charge of transporting the data (inside the packet) 
from the source machine to the destination machine, regardless of the type of physical network.

The information unit of layer 4 is called Segment or Datagram, depending on whether it corresponds to TCP or UDP, 
the first one oriented to connection (verified transmission, eventually retransmitted) 
and the other one without connection (some data can be lost by the way). 
They work with logical ports and together with the network layer they give form to the known as IP Sockets: Port.

**Example:** TCP, UDP ...

### 5: Session Layer
The session layer controls the dialogues (connections) between computers. It establishes, manages and terminates the connections 
between the local and remote application

**Example:** TLS, RPC ...

### 6: Presentation Layer
The presentation layer establishes context between application-layer entities, in which the application-layer entities 
may use different syntax and semantics if the presentation service provides a mapping between them.

This layer also allows data to be encrypted and compressed. Therefore, it could be said that this layer acts as a translator.

**Example:** ASN.1 ...

### 7: Application Layer
The application layer is the OSI layer closest to the end user, 
the layer gives applications the ability to access the services of other layers and defines the protocols used by applications 
to exchange data.

It should be noted that the user does not normally interact directly with the application level. 
It usually interacts with software that in turn interact with the application level but hiding the underlying complexity.

**Example:** FTP, SSH, HTTP, MQTT, CoAP ...

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# HTTP
Hyper Text Transfer Protocol is the communication protocol that enables information transfers on the World Wide Web.

Communication between clients and servers is done by requests and responses:

1. A client sends an HTTP request to the web
2. A server receives the request
3. The server runs an application to process the request
4. The server returns an HTTP response (output) to the client
5. The client receives the response

HTTP defines a predefined set of request methods that can be used:
 - **GET:** requests a representation of the specified resource.
 - **HEAD:** asks for a response identical to that of a GET request, but without the response body.
 - **POST:** Sends the data to be processed by the resource.
 - **PUT, DELETE, TRACE, OPTIONS ...**
The protocol has the flexibility to add new methods and functionalities.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# CoAP

**Constrained Application Protocol** is a service layer protocol that is intended for use in resource-constrained internet devices, 
such as wireless sensor network nodes.

It implements the HTTP REST model (with the primitives GET, POST, PUT and DELETE), 
uses reduced headers, and limits the exchange of messages, adding UDP support and other modifications
as specific security mechanisms.

Multicast, low overhead, and simplicity are extremely important for Internet of Things devices

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# MQTT

**Message Queuing Telemetry Transport** is a publish/subscribe, extremely simple and lightweight messaging protocol,
designed for constrained devices and low-bandwidth, high-latency or unreliable networks.

The design principles are to minimise network bandwidth and device resource requirements whilst
also attempting to ensure reliability and some degree of assurance of delivery.
These principles also turn out to make the protocol ideal for Internet of Things.

[read more](references_mqtt.md)

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# FTP

**File Transfer Protocol** is a standard network protocol used for the transfer of files between a client and server 
on a TCP network.

The FTP service is provided by the application layer of the TCP/IP network layer model to the user, 
typically using network Port 20 and 21. 

A basic problem with FTP is that it is designed to offer maximum connection speed, but not maximum security.
To solve this problem, new applications allow encrypting traffic.

- **SFTP** included in the SSH package
- **FTPS** often secured with SSL/TLS

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# TLS

**Transport Layer Security** and its now-deprecated predecessor, Secure Sockets Layer (SSL) are cryptographic protocols 
designed to provide communications security over a computer network.

Before a client and server can begin exchanging information protected by TLS, they must securely exchange 
an encryption key (private key) and a decryption key (public key).

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# SSH 

**Secure Shell** is a cryptographic network protocol whose main function is remote access to a server via a secure channel. 
Typical applications include remote command execution.

It was designed as a replacement for Telnet and for unsecured remote shell protocols, typically using network Port 22.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

