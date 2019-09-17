### Table of Contents

- [What does it do?](#what-does-it-do)
  * [Google Cloud Options](#google-cloud-options)
    + [GCP Option 1: Telemetry](#gcp-option-1-telemetry)
- [Deploy and defend your Bridge!](#now-deploy-and-defend-your-bridge)
  * [What will you need?](#what-will-you-need)
  * [Google Cloud Platform Computing Services](#google-cloud-platform-computing-services)


&#x1F4CD;

Google Cloud is one of the main public clouds, but we've only been testing using the IoT core for the time being.
At the moment we are working so that you can deploy the Bridge in GCP.


# What does it do?

Each UDP message or CoAP request sent by a device, it is linked to several information such as source IP, destination IP and destination Port. 
The Bridge will use the device source IP to gather all the sim information stored at Kite platform. 

For the tutorial purpose you should pay attention to SIM's custom fields, 
that you can manage from your Kite Platform account. 

- **Field 1** : Device Cloud Name (required) -> this is the name that will appear at the cloud (shadow name, twin name ...) 
- **Field 2** : topic to publish (optional)

Depending on the content of the fields, the Bridge will act differently. 

To choose between the different options you have to configure SIM information at the [Custom Field](Kite_Platform.md#edit-custom-field)

&#x1F4CD;
The device name is a mandatory field, otherwise an error code will be returned, because the bridge wouldn't know the virtual representation of the physical device.

As we said before, There are 1 way of working depending on the information provided as custom parameter in Kite. 

news options in process ...

## Google Cloud Options

- [GCP Option 1: publish in a default topic](#gcp-option-1-publish-in-a-default-topic)


### GCP Option 1: Telemetry

You only have to provide a device cloud name at the first custom parameter in Kite. 
As a result all the messages sent by your device will be published at the device telemetry topic. 

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


# Now, Deploy and defend your Bridge!

## What will you need?

- Data Bridge [code](https://github.com/telefonicaid/iot-activation/tree/master/scripts/Data_Bridge)
- KITE Platform [Certificates files](Kite_Platform.md#what-is-kite-platform-api)
- An IpSec Service provided by Telefónica [(IPsec)](BP_IPsec.md#what-is-ipsec)
- Google Cloud account:

&#x1F4CD;
For the time being, if you use a SIM from the Thinx testing network you will not have access to the Kite Platform.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)


## Google Cloud Platform Computing Services

If you are using this tutorial is because you have chosen Google as your cloud.

For this reason, we have tried that all the services provided in the Data Bridge are integrated at Google Cloud Platform platform.
In the following steps we will explain how to configure these services.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

### GCP IoT Core

Cloud IoT Core is a fully managed service that allows you to easily and securely connect, manage, 
and ingest data from millions of globally dispersed devices.

[![pic](pictures/utils/arrow_up.png)](#table-of-contents)

in process ...

