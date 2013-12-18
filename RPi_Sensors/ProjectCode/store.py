
# Store File (Store & Upload)
# Author: Rishav Jain
#
# This file stores the readings into files
#

# importing variables from other project files
from profile import profile
import variables
from upload import uploadReadings
from buffers import getReadings
from logger import log

# import required libraries
import time
import os
import threading


def StoreTask():
	UploadTask = threading.Thread(target = uploadReadings, args=())		# Task to Upload the data from files to SensorAct
	UploadTask.start()

	# saving current time
	prevTime = time.time()

	uploadCount = 0

	Files = None;
	path = ''
	
	while(True):
		nowTime = time.time()

		if nowTime-prevTime > 1:
			prevTime = nowTime

			if variables.alarmCount == 0:
				variables.timestamp = nowTime
				log('info', 'Updating TimeStamp')
				
				if Files == None:
					variables.Current_Store_Folder = str(variables.timestamp) + '__' + time.strftime('%d-%m-%y_%H:%M:%S', time.gmtime(variables.timestamp+19800))
					path = profile.StorePath + variables.Current_Store_Folder + '/'
					
					if not os.path.exists(path):
						os.makedirs(path)
					
					Files = {}
					
					for i in variables.Sensors:
						Files[i] = open(path + i + '.csv', 'a+')

			if variables.alarmCount % profile.SamplingPeriod == 0:
				variables.alarmRead = 1
				variables.alarmRead = 0
				
				log('info', 'Sampling')

				readings = getReadings()

				Files[variables.Sensors['Temp']].write(str(readings[0]))
				Files[variables.Sensors['Light']].write(str(readings[1]))
				Files[variables.Sensors['PIR']].write(str(readings[2]))
				
				for i in variables.Sensors:
					Files[i].flush()

			variables.alarmCount += 1
			uploadCount += 1

			if variables.alarmCount % profile.StoreLength != 0:
				for i in variables.Sensors:
					Files[i].write(', ')
					Files[i].flush()

			if variables.alarmCount % profile.StoreLength == 0:
				log('info', 'Storing Readings in a New File')
				variables.alarmCount = 0

				for i in variables.Sensors:
					Files[i].close()

				Files = None

			if uploadCount % profile.UploadPeriod == 0:
				log('info', 'Upload Initiated')
				variables.alarmUpload = 1
				uploadCount = 0



#For testing this module ONLY
#StoreTask()
