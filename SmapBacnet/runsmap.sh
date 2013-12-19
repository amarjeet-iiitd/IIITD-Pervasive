#!/bin/bash

rm twistd.pid
rm nohup.out
nohup /usr/local/bin/twistd smap /home/pi/smap/iiitd_bms.conf &
nohup python /home/pi/bmspanel/manage.py runserver 0.0.0.0:8000 --noreload --nothreading &
nohup /usr/local/bin/twistd smap /home/pi/smap/iiitd_bms_meters.conf &
nohup python /home/pi/bmsmeterpanel/manage.py runserver 0.0.0.0:8001 --noreload --nothreading &

