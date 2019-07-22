#!/bin/sh
clear
echo "################################################################################"
echo "AWS Cloud Selected"
echo "################################################################################"

echo "Installing Python libraries"
sudo pip install lib/PyYAML-5.1.1.tar.gz
sudo pip install lib/paho-mqtt-1.4.0.tar.gz
sudo pip install lib/boto3-1.9.175.tar.gz -t ./
echo "Python libraries installed"

echo "Running Self-Provisioning in AWS"
python AWS_Selfprovisioning.py
echo "Self-Provisioning END"

read -r -p "Do you want to publish in AWS every time you turn on the device? [y/N] " response
case "$response" in
    [yY][eE][sS]|[yY])
        echo "Editing CRONTAB"
        var_crontab=$(crontab -l | grep AWS_publish)
        if [ -z "$var_crontab" ] 
        then
            path=$(pwd) 
            line="@reboot (sleep 60;cd $path; python AWS_publish.py >> $path/log.log)"
            (crontab -u pi -l; echo "$line" ) | crontab -u pi -
        fi
        ;;
    *)
        echo ""
        ;;
esac

echo "Publishing in IoT Core"
python AWS_publish.py

