---
layout: post
title:  "Control your Raspberry with a Network cable"
date:   2018-12-19 22:37:00 +05:30
categories: Raspberry
---

# Control your Raspberry with a Network cable

If you want to connect your Raspberry to your computer via a network cable, 
you must ensure that both devices are configured for the same network.

The easiest way is to set up a static IP. In order to do this, 
we will assign an IP of our choice to the configuration that you assign for the configuration.

Open a terminal windows use the next command 'sudo ifconfig -a'

If you are connected by cable you will see an IP address assigned.
This IP has been assigned automatically and will change whenever you establish a new connection.

To set a default IP address edit the file **/etc/dhcpcd.conf**
use the command `sudo nano /etc/dhcpcd.conf` at the command prompt.
Scroll to the bottom of the script, and add the following lines

```
	interface eth0

	static ip_address=192.168.0.2/24
	static routers=192.168.0.1
	static domain_name_servers=192.168.0.1
```
Save the file with **Ctrl+O**  and close it with **Ctrl+X**
review the changes whit the command `cat /etc/dhcpcd.conf`

