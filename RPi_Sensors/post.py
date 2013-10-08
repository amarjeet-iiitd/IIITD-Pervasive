
import variables
from profile import profile

import socket

Sensors = ['Temp', 'Light', 'PIR']

def makeJSON(Sensor):
#     str(sample.TempReadings)[1:len(str(sample.TempReadings))-1]

    sensorID = 1
    channelName = 'channel1'
    sensorName = ''
    unit = ''
    sReadings = ''
        
    if Sensor == 'Temp':
        sensorName = 'TemperatureSensor'
        unit = 'celcius'
        sReadings = str(variables.TempReadings)[1:len(str(variables.TempReadings))-1]
        variables.TempReadings = ()
        
    elif Sensor == 'Light':
        sensorName = 'LightSensor'
        unit = 'none'
        sReadings = str(variables.LightReadings)[1:len(str(variables.LightReadings))-1]
        variables.LightReadings = ()
        
    elif Sensor == 'PIR':
        sensorName = 'PIRSensor'
        unit = 'none'
        sReadings = str(variables.PirReadings)[1:len(str(variables.PirReadings))-1]
        variables.PirReadings = ()
    

    JSON = '{"secretkey":"' + str(profile.APIkey) + '","data":{"loc":"'
    JSON += profile.DeviceLocation + '","dname":"' + profile.DeviceName + '",'
    JSON += '"sname":"' + sensorName + '","sid":' + str(sensorID) + ','
    JSON += '"timestamp":' + str(variables.timestamp) + ',"speriod":' + str(profile.SamplingPeriod) + ','
    JSON += '"channels":[{"cname":"' + channelName + '","unit":"' + str(unit) + '",'
    JSON += '"readings":[' + sReadings + ']}]}}\r\n\r\n'
        
    variables.POST_buffer = 'POST ' + profile.ServerURL + ' HTTP/1.1\r\n'
    variables.POST_buffer += 'Host: ' + profile.ServerIP + '\r\n'
    variables.POST_buffer += 'Accept: */*\r\n'
    variables.POST_buffer += 'Content-Length: ' + str(len(JSON)) + '\r\n'
    variables.POST_buffer += 'Content-Type: application/json; charset=UTF-8\r\n'
    variables.POST_buffer += 'Connection: close\r\n'
    variables.POST_buffer += '\r\n' + JSON
        
    return

def postReadings():
	while True:
		if variables.alarmUpload == 1:
		    print('Posting')
		    variables.alarmUpload = 0
            
		    for i in range(0,len(Sensors)):
		    
		    	try:
				skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				    
				skt.connect((profile.ServerIP, profile.ServerPort))
			
				makeJSON(Sensors[i])
				    
				print(variables.POST_buffer)
			
				skt.send(variables.POST_buffer)
			
				print(skt.recv(10000))
						    
				skt.close()
			except:
				print 'error'
				continue
	return
