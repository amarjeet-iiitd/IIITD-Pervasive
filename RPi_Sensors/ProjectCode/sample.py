# Sample File (Realtime Sample/Publish)
# Author: Rishav Jain
#
# This file samples the readings from the sensor
#

# importing variables from other files from the project
from profile import profile
import variables
from publish import postReadings
from buffers import getReadings
from logger import log

# import required libraries
import threading
import time

def SampleTask():
	PublishTask = threading.Thread(target = postReadings, args=())		# starting the PublishTask thread
	PublishTask.start()												# that posts the readings to server and clear the readings buffers

	prevTime = time.time()			# noting the time

	while True:
		nowTime = time.time()

		if nowTime-prevTime > 1:		# execute the below code, every 1 second
			prevTime = nowTime

			if variables.alarmCount == 0:			# note the timestamp from which we start sampling
				log('info', 'Updating Timestamp - ' + str(time.time()))
				variables.timestamp = time.time()

			if variables.alarmCount % profile.SamplingPeriod == 0:		# if sampling time is reached
				log('info', 'Sampling')

				readings = getReadings()

				variables.TempReadings += (readings[0],)
				
				variables.LightReadings += (readings[1],)
				
				variables.PirReadings += (readings[2],)

			variables.alarmCount += 1
			if variables.alarmCount % profile.PublishPeriod == 0:		# if publish time is reached
				variables.alarmCount = 0

				variables.lockQueue.acquire()
				variables.postQueue.append((variables.timestamp, variables.TempReadings, variables.LightReadings, variables.PirReadings))
				variables.lockQueue.release()

				variables.TempReadings = ()
				variables.LightReadings = ()
				variables.PirReadings = ()
