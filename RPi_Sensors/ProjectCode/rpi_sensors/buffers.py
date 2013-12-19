# Buffers File
# Author: Rishav Jain
#
# This file contains functions to get the readings, and the post packet
#

# importing variables from other files from the project
import variables
from profile import profile
from logger import log

# import files for sensors
import sensors.PIR as PIR
import sensors.interfacei2clightsensor as Light
import sensors.ds1820_final_1 as Temp

num = 0		# TESTING

'''
 Returns a tuple containing the readings from the sensors
 in order - (TEMP, LIGHT, PIR)
'''
def getReadings():
	ret = ()
	
	#~ # TESTING			#
	#~ global num			#
	#~ if num==10:			#
		#~ num=0			#
	#~ ret = (num,num,num)	#
	#~ num+=1				#
	
	tmp = Temp.read_temp()
	ret += (tmp,)
	
	Light.APDS_init()
	tmp = Light.APDS_read()
	ret += (tmp,)
	
	tmp = PIR.PIR_Read()
	ret += (tmp,)
	
	log('readings', 'Temp : ' + str(ret[0]) \
					+ ', Light : ' + str(ret[1]) \
					+ ', PIR : ' + str(ret[2]))

	return ret

'''
 Returns the post packet
 Arguments -
   Sensor : name of the sensor
   timestamp : timestamp to be put into the packet
   readings : the readings to be posted
'''
def makePacket(Sensor, timestamp, readings):
	sensorID = 1
	channelName = 'channel1'
	sensorName = ''
	unit = ''
	sReadings = ''

	if Sensor == variables.Sensors['Temp']:
		sensorName = 'TemperatureSensor'
		unit = 'celcius'

	elif Sensor == variables.Sensors['Light']:
		sensorName = 'LightSensor'
		unit = 'none'

	elif Sensor == variables.Sensors['PIR']:
		sensorName = 'PIRSensor'
		unit = 'none'

	JSON = '{"secretkey":"' + str(profile.APIkey) + '",' \
		+ '"data":{"loc":"' + profile.DeviceLocation + '",' \
		+ '"dname":"' + profile.DeviceName + '",' \
		+ '"sname":"' + sensorName + '","sid":' + str(sensorID) + ',' \
		+ '"timestamp":' + str(timestamp) \
		+ ',"speriod":' + str(profile.SamplingPeriod) + ',' \
		+ '"channels":[{"cname":"' + channelName + '","unit":"' + str(unit) + '",' \
		+ '"readings":[' + readings + ']' \
		+ '}]' \
		+ '}' \
		+ '}\r\n\r\n'

	variables.POST_buffer = 'POST ' + profile.ServerURL + ' HTTP/1.1\r\n' \
							+ 'Host: ' + profile.ServerIP + '\r\n' \
							+ 'Accept: */*\r\n' \
							+ 'Content-Length: ' + str(len(JSON)) + '\r\n' \
							+ 'Content-Type: application/json; charset=UTF-8\r\n' \
							+ 'Connection: keep-alive\r\n' \
							+ '\r\n' + JSON

	return
