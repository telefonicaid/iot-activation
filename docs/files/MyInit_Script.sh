#! /bin/sh
# /etc/init.d/miScript
echo Start_Python_Script 
python /home/pi/Desktop/main.py 

exit 0

sudo update-rc.d MyInit_Script.sh defaults

setsid /usr/bin/python /home/pi/Desktop/main.py &


sudo nano /etc/profile
sudo nano /etc/profile


sudo python /home/pi/Desktop/main.py


crontab -e
@reboot ( sleep 15 ; /usr/bin/python2.7 /home/pi/Desktop/main.py )

@reboot /usr/bin/python2.7 /home/pi/Desktop/main.py > /home/pi/Desktop/TEST.log


@reboot ( sleep 60  ; /usr/bin/python2.7 /home/pi/Desktop/main.py > /home/pi/Desktop/iot_cam.log )
