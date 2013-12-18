
# SAVE PARAMETERS FROM SERVER
# Author: Rishav Jain

import sys

import device as Device
import sensoract as Sensoract
import connection as Connection
import log as LogParam
import config

FILE_PATH = config.FOLDER_PATH + '/profile_io/data/'

DEVICE_PARAMETERS_FILE = 'device.conf'
SENSORACT_PARAMETERS_FILE = 'sensoract.conf'
CONNECTION_PARAMETERS_FILE = 'connection.conf'
LOG_PARAMETERS_FILE = 'log.conf'

try:
	if sys.argv[1] == 'device':
		PARAM = {'Mode':sys.argv[2],
				 'SamplingPeriod':sys.argv[3],
				 'PublishPeriod':sys.argv[4],
				 'StoreLength':sys.argv[5],
				 'StorePath':sys.argv[6],
				 'UploadPeriod':sys.argv[7]}

		Device.save(FILE_PATH, DEVICE_PARAMETERS_FILE, PARAM)

	elif sys.argv[1] == 'sensoract':
		PARAM = {'APIkey':sys.argv[2],
				 'DeviceName':sys.argv[3],
				 'DeviceLocation':sys.argv[4]}

		Sensoract.save(FILE_PATH, SENSORACT_PARAMETERS_FILE, PARAM)

	elif sys.argv[1] == 'connection':
		PARAM = {'ServerIP':sys.argv[2],
				 'ServerPort':sys.argv[3],
				 'ServerURL':sys.argv[4]}

		Connection.save(FILE_PATH, CONNECTION_PARAMETERS_FILE, PARAM)

	elif sys.argv[1] == 'log':
		PARAM = {'EnableLog':sys.argv[2],
				 'LogDir':sys.argv[3],
				 'LogTags':'('+sys.argv[4]+')'}
		LogParam.save(FILE_PATH, LOG_PARAMETERS_FILE, PARAM)

	print('SUCCESS')

except Exception as e:
	print('ERROR')
	print(e.args)
	traceback.print_exc(file=sys.stdout)
