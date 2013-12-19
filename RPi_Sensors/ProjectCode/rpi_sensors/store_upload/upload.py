
# Upload File (Store & Upload)
# Rishav Jain

import variables
from profile import profile
from buffers import makePacket
from logger import log

import time
import os
import socket

## TESTING
#~ import threading

def uploadReadings():
	log('info', 'UploadTask started')

	while(True):
		if variables.alarmUpload == 1:
			variables.alarmUpload = 0

			folders = os.listdir(profile.StorePath)
			log('info', ('No. of Folders to upload : ', len(folders)))

			folders.sort()
			
			ERROR = False
			
			try:
				skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				skt.connect((profile.ServerIP, profile.ServerPort))
				for FOLDER in folders:
					
					if FOLDER == variables.Current_Store_Folder:
						continue
					
					files = os.listdir(profile.StorePath + FOLDER)

					for FILE in files:
						fp = open(profile.StorePath + FOLDER + '/' + FILE.strip('.csv') + '.csv', 'r')
						readingsDump = fp.readline()
						fp.close()
						
						makePacket(FILE.strip('.csv'), FOLDER.split('__')[0], readingsDump)
						#~ makePacket(FILE.strip('.csv'), FOLDER, readingsDump)
						
						log('post_buffer', '\n' + variables.POST_buffer)
						
						skt.send(variables.POST_buffer)
						log('server_response', '\n' + skt.recv(1000))
						
						os.remove(profile.StorePath + FOLDER + '/' + FILE)

					if len(os.listdir(profile.StorePath + FOLDER)) == 0:
						log('info', ('uploadReadings', 'Removing Folder - ', FOLDER))
						os.rmdir(profile.StorePath + FOLDER)
					
				skt.close()
			except Exception as e:
				log('error', '\nNetwork Error - ' + '\n' + str(e.args) + '\n' + str(e.message))

#~ ## FOR TESTING PURPOSES ONLY
#~ UploadTask = threading.Thread(target = uploadReadings, args=())
#~ UploadTask.start()
#~ 
#~ variables.alarmUpload = 1
