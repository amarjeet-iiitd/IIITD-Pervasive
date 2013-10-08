
import variables
from profile import profile
from post import postReadings

import time
import threading


import PIR
import interfacei2clightsensor as Light
import ds1820_final_1 as Temp


profile.profileInit()
profile.printProfile()

PostTask = threading.Thread(target = postReadings, args=())

PostTask.start()

# Light.APDS_init()

prevTime = time.time()
nowTime = time.time()

while True:
#     print('alarmCount: ', variables.alarmCount)
	nowTime = time.time()
	
	if nowTime-prevTime > 1:
		prevTime = nowTime
		
		if variables.alarmCount == 0:
			variables.timestamp = nowTime
		    
		if variables.alarmCount % profile.SamplingPeriod == 0:
			variables.alarmRead = 1
			variables.alarmRead = 0
			# print('Sampling')
			
			'''
			if variables.alarmCount%2 == 0:
				variables.TempReadings += (0.0,)
				variables.LightReadings += (0.0,)
				variables.PirReadings += (0,)
				
		    	else:
				variables.TempReadings += (1.0,)
				variables.LightReadings += (1.0,)
				variables.PirReadings += (1,)		   

			'''
			
			variables.TempReadings += (Temp.read_temp(),)

			Light.APDS_init()
			variables.LightReadings += (Light.APDS_read(),)
		
			variables.PirReadings += (PIR.PIR_Read(),)
		
		
			print(variables.TempReadings)
			print(variables.LightReadings)
			print(variables.PirReadings)
		    
		variables.alarmCount += 1
		if variables.alarmCount % profile.PublishPeriod == 0:
		    variables.alarmUpload = 1
		    variables.alarmCount = 0
		
		#time.sleep(1)

