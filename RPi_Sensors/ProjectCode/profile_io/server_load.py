
import config
import device as Device
import sensoract as Sensoract
import connection as Connection
import log as LogParam
import traceback, sys

FILE_PATH = config.FOLDER_PATH + '/profile_io/data/'

DEVICE_PARAMETERS_FILE = 'device.conf'
SENSORACT_PARAMETERS_FILE = 'sensoract.conf'
CONNECTION_PARAMETERS_FILE = 'connection.conf'
LOG_PARAMETERS_FILE = 'log.conf'

try:
	PARAM = []
	PARAM += Device.load(FILE_PATH + DEVICE_PARAMETERS_FILE).items()
	PARAM += Sensoract.load(FILE_PATH + SENSORACT_PARAMETERS_FILE).items()
	PARAM += Connection.load(FILE_PATH + CONNECTION_PARAMETERS_FILE).items()
	PARAM += LogParam.load(FILE_PATH + LOG_PARAMETERS_FILE).items()

	print('SUCCESS')
	
	for i in PARAM:
		#~ print('\n')
		print(i[0] + ' ' + str(i[1]))

except Exception as e:
	print('ERROR')
	print(e.args)
	traceback.print_exc(file=sys.stdout)
