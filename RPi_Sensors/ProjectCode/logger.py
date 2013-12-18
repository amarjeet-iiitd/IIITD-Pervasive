# Logger File
# Author: Rishav Jain

# Tags - 'info', 'error', 'readings', 'post_buffer', 'server_response'
#

# importing necessary files from the project
from profile import profile
import variables

# importing files for standard functions
import threading
import time
import os

# global variables to be shared by functions below
LOG_ENABLED = True
START_TIME = None		# to store time when the program started executing
logFiles = None			# dict variable with key = TAG_NAME, value = (FILE_OBJECT, FILE_CREATION_TIME)
queue = ()				# to store the log messages

'''
 Writes the logs into files

 Uses Directory Structure -
  <LOG_DIR>/<PROGRAM_START_TIME>/<LOG_TAG>/<FILE_CREATION_TIME>

 Arguments - Log Tag, Message to log
'''
def writeLog(TAG, MSG):
	global TIME, logFiles, START_TIME

	if START_TIME == None:			# For the first excecution of program, note the start time
		START_TIME = time.asctime(time.gmtime(time.time()+19800))

	if logFiles[TAG][1] == None:	# if tag has not yet been logged
		logFiles[TAG][1] = time.time()

	if time.time()-logFiles[TAG][1] > 3600:		# if the tag has been logged for more than 1 hour, log into a new file
		if logFiles[TAG][0] != None:
			logFiles[TAG][0].close()
			logFiles[TAG][0] = None

	if logFiles[TAG][0] == None:			# opens the file for the log
											# (if the tag has not been logged previously, or satisfies the previous condition)
		logFiles[TAG][1] = time.time()

		log_path = profile.LogDir + START_TIME + '/' + TAG + '/'

		if not os.path.exists(log_path):
			os.makedirs(log_path)

		logFiles[TAG][0] = open(log_path +  time.asctime(time.gmtime(logFiles[TAG][1]+19800)), 'w+')

	# write to file
	logFiles[TAG][0].write(str(MSG))
	logFiles[TAG][0].write('\n')
	logFiles[TAG][0].flush()
	return

'''
 Log Service runs as seperate thread, continously writing logs to file
'''
def logService():
	global queue

	while True:			# continously polling
		if len(queue) > 0:		# if any log is pending in queue, write it to file
			tmp = queue
			queue = ()

			for i in tmp:
				writeLog(i[0], i[1])
				print(i[0], i[1]);		# TESTING
		#~ time.sleep(10)

'''
 Adds new message to the Queue (only if Logging is Enabled by User)
'''
def log(TAG, MSG):
	global queue
	if LOG_ENABLED:
		try:
			profile.LogTags.index(TAG)				# if tag is not present in the profile LogTags attribute, it gives ValueError
			queue += ((TAG, time.asctime(time.gmtime(time.time()+19800)) + ' - ' + str(MSG)),)	# adds a new message to queue, alongwith the timestamp at which it is added

		except ValueError as e:
			print('Tag Not Enabled : ' + TAG)		# TESTING
			return

	#~ print queue		# TESTING
	return


'''
 Initializes the Logger Service (only if Logging is Enabled by User)
'''
def logInit():
	global logFiles
	if profile.EnableLog:
		LOG_ENABLED = profile.EnableLog

		logFiles = {}				# setting the tags for the logFiles dict object

		for i in profile.LogTags:
			logFiles[i] = [None, None]	# value for a logFiles element in array of FILE_OBJECT and FILE_CREATION_TIME

		# starting the logService thread
		LogTask = threading.Thread(target = logService, args=())
		LogTask.start()

## TESTING this file			#
#~ i=0							#
#~ logInit()					#
#~ while True:					#
	#~ log('info', str(i))		#
	#~ i+=1						#
	#~ time.sleep(1)			#
