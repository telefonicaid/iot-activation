#!/bin/sh
clear
echo "################################################################################"
echo "3G Configuration"
echo "################################################################################"


var_dongle=$(lsusb | grep "Huawei Technologies Co., Ltd. Modem/Networkcard")
while [ ! -z "$var_dongle" ] 
do
    echo "Please Unplug the USB 3G Dongle to Start"
    sleep 3
    var_dongle=$(lsusb | grep "Huawei Technologies Co., Ltd. Modem/Networkcard")
done

echo "Installing libraries..."
sudo dpkg -i deb/*.deb

echo "Setting the Telefonica 3G connection"

echo "Type your Telefonica APN - Access Point Name"
echo "Press Enter for default APN ['m2m.movistar.es']"
read var_apn

if [ -z "$my_var" ]
then
    var_apn="m2m.movistar.es"
fi

echo $var_apn

sudo nmcli con add type gsm ifname "*" con-name USBStick apn $var_apn user telefonica password telefonica

clear
echo  "Plug the USB 3G Dongle in the Raspberry"
sleep 5

var_ppp0=$(ifconfig ppp0 | grep inet)

cont_reboot=0
while [ -z "$var_ppp0" ] 
do
    echo "Waiting for interface connection"
    sleep 10
    var_ppp0=$(ifconfig ppp0 | grep inet)
    cont_reboot=$((cont_reboot + 10))
    
    if [ $cont_reboot -gt 110 ]
    then
        echo "Rebooting the Raspberry"
        echo "Please unplug the USB 3G Dongle and Try Again"
        read -p "Press Enter to continue"
        sudo reboot
    fi
done

echo "Trying connect to Internet"

var_ping=$(ping -q -c1 8.8.8.8 | grep 100%)

while [ ! -z "$var_ping" ] 
do
    echo "Waiting for Internet connection"
    sleep 5
    var_ping=$(ping -q -c1 8.8.8.8 | grep 100%)
done

echo "Connected to Internet"

sleep .5
echo "3G Configuration OK"
sleep .5
