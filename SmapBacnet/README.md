SmapBacnet
===============

This is a BACnet protocol driver for smap written using BACpypes. It consists of two drivers and their respective configuration utilities written in Django, one for generic BACnet Points and the other for Electricity meters communicating over BACnet.

The generic driver utility can be accessed at http://127.0.0.1:8000.
The electricity meter driver utility can be accessed at http://127.0.0.1:8001.

Login/Password by default is admin/bms@iiitd. During installation, you may be prompted to enter a new admin login and password.

Installation:
1) Setup a Raspberry Pi with the latest distribution of Raspbian.
2) Put bmspanel, bmsmeterpanel and smap folders and installbmsdriver.sh and runsmap.sh in /home/pi/
3) Run chmod +x installbmsdriver.sh; ./installbmsdriver.sh
4) Configure the IP addresses and filepaths in /smap/iiitd_bms.conf, /smap/iiitd_bms_meters.conf, /bmsmeterpanel/SmapBacnetUtils.py and /bmspanel/SmapBacnetUtils.py"
5) Reboot
