#!/usr/bin/env python
import subprocess,sys
import time
import os
import datetime
import random
import glob
import csv
import os
import datetime
import logging
import threading
import thread

res = '640x480'
dev = '/dev/video0'
pallete = 'YUYV'

burst = 3
interval = 0.5

'''Timer method to check if process is alive every 60 secs'''
nextLog = time.time()
def periodicLog():
	global nextLog
	logger.info('Alive...')
	nextLog += 60
	threading.Timer(nextLog - time.time(), periodicLog).start()

def captureImg(startTime, numImg, interval):
	os.chdir('/home/pi/zWaveData/')
	dir = startTime.strftime("%Y-%m-%d %H:%M:%S")

	if not os.path.exists(dir):
		logger.info("Creating " + dir + "...")
		os.makedirs(dir)

	os.chdir('/home/pi/zWaveData/' + dir)
	cmd = 'sudo fswebcam' + ' -r ' + res + ' -d ' + dev + ' -p ' + pallete + ' '
	count = 1

	while (count <= numImg):
		timeDiff = datetime.datetime.now() - startTime
		diff = timeDiff.seconds
		imgName = 'img' + str(count) + '_' + str(diff) + '.jpeg'	
		execCMD = cmd + imgName
		logger.info('CWD: ' + os.getcwd())
		logger.info('Executing ' + execCMD)
		proc = subprocess.Popen(execCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = proc.communicate()
		logger.info(stdout)
		logger.info(stderr)
		count += 1
		time.sleep(interval)
		proc.wait()
	logger.info('Returning...')
	return

'''setup logger'''
logger = logging.getLogger('zWaveSensor')
form = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='/home/pi/zWaveSensor/zWave.log', level=logging.INFO, format=form)
logger.info('Script started...')

'''start main C zWave controller code in a process'''
os.chdir("/home/pi/zWaveSensor/")
os.system("LD_LIBRARY_PATH=/usr/local/lib")
os.system("export LD_LIBRARY_PATH")
process = subprocess.Popen("./HomeZwave", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
#so, se = process.communicate()

'''logging'''
periodicLog()
logger.info('HomeZwave started...')
os.chdir("/home/pi/zWaveData/")

'''poll process for new output until finished'''
while True:
	nextline = process.stdout.readline()
	if nextline == '' and process.poll() != None:
		break

	if "Received SensorBinary report:" in nextline:
		fields_in_line = nextline.split("State=")
		status = str(fields_in_line[1])
		
		if status == "On\n":
			logger.info('Opened...Capturing...')
			try:
				thread.start_new_thread(captureImg, (datetime.datetime.now(), burst, interval, ))
				logger.info('Thread started...')
			except:
				logger.info('ERROR: Thread could not start...')
	sys.stdout.flush()

#while True:
#	print 'New thread...'
#	thread.start_new_thread(captureImg, (datetime.datetime.now(), 3, 0, ))
#	time.sleep(300)