# Publish File (Realtime Sample/Publish)
# Author: Rishav Jain
#
# This file copies the timestamp and readings from the sample file,
# clears the buffers and then upload the readings to the server
#

# importing other files from the project
import variables
from profile import profile
from logger import log
from buffers import makePacket

# importing required libraries
import socket
import time

def postReadings():
	log('info', 'Starting Post Task ')

	toPublish = []
	
	while True:					# this thread continously polls

		if len(variables.postQueue) > 0:

			variables.lockQueue.acquire()
			toPublish += variables.postQueue
			variables.postQueue = []
			variables.lockQueue.release()
			
			log('info', 'Publishing Readings to the server')

			try:
				skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)			# connecting the server
				skt.connect((profile.ServerIP, profile.ServerPort))

				for i in toPublish:
					readingsDump = {}
					readingsDump[variables.Sensors['Temp']] = str(i[1])[1:-1]
					readingsDump[variables.Sensors['Light']] = str(i[2])[1:-1]
					readingsDump[variables.Sensors['PIR']] = str(i[3])[1:-1]
					
					for j in readingsDump:				# sending the all the packets, once the connection is established
						makePacket(j, i[0], readingsDump[j])

						log('post_buffer', '\n' + variables.POST_buffer)

						skt.send(variables.POST_buffer)
						log('server_response', '\n' + skt.recv(1000))		# TESTING

				skt.close()
				toPublish = []

			except Exception as e:
			   log('error', '\nNetwork Error - ' + time.asctime() + '\n' + str(e.args) + '\n' + e.message)
			   continue
	return
