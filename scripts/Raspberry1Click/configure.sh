#!/bin/sh
clear
echo "################################################################################"
echo "Raspberry Pi configuration fo IoT Activation"
echo "################################################################################"

sudo sh configure_ssh.sh | tee log/RaspberryPi_1Click_shh.log
sudo sh configure_3g.sh  | tee log/RaspberryPi_1Click_3g.log
sh configure_cloud.sh
