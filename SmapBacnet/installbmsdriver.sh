#!/bin/bash

apt-get update
apt-get install python-pip -y
apt-get install python-dev -y
apt-get install python-numpy -y
apt-get install python-scipy -y
pip install smap
pip install pyOpenSSL
apt-get install libcurl4-gnutls-dev librtmp-dev -y
pip install pycURL
pip install bacpypes
sudo cp ./smap/iiitd_bms.py /usr/local/lib/python2.7/dist-packages/smap/drivers
sudo cp ./smap/iiitd_bms_meters.py /usr/local/lib/python2.7/dist-packages/smap/drivers
python ./bmsmeterpanel/manage.py syncdb
python ./bmspanel/manage.py syncdb
sudo head -n -2 /etc/rc.local > temp.local
sudo mv temp.local /etc/rc.local
sudo (echo /home/pi/runsmap.sh; echo exit 0) >> /etc/rc.local
echo "Installation done! Make sure the bmspanel, bmsmeterpanel and smap folders are in /home/pi/. Remember to configure the IP addresses and filepaths in /smap/iiitd_bms.conf, /smap/iiitd_bms_meters.conf, /bmsmeterpanel/SmapBacnetUtils.py and /bmspanel/SmapBacnetUtils.py"
