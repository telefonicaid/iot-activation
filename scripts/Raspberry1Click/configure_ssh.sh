#!/bin/sh
clear
echo "################################################################################"
echo "SSH Configuration"
echo "################################################################################"

echo "Setting remote connection"

sudo systemctl enable ssh
sudo systemctl start ssh

echo "SSH enabled OK"

sudo echo "iface eth0 inet manual" >> /etc/network/interfaces
sudo echo "interface eth0" >> /etc/dhcpcd.conf
sudo echo "static ip_address=192.168.0.10/24" >> /etc/dhcpcd.conf

echo "Static IP in interface eth0 192.168.0.10/24"

echo "Choose a new password for your user pi [default password 'raspberry']"
passwd 

sleep .5
echo "SSH Configuration OK"
sleep .5

