# Profile File
# Author: Rishav Jain
#
# Parameters -
#  Mode,									[1 for Realtime Sample/Publish, 2 for Store & Upload]
#  Sampling Period,							[Time to sample the readings from the sensors, INTEGER>=1]
#  Publish Period,							[for Realtime Sample/Publish Mode]
#  Store Length, Store Path, Upload Period,	[for Store & Upload Mode]
#  API Key, Device Name, Device Location,	[SensorAct Parameters]
#  Server IP, Server Port, Server URL,		[Connection Parameters]
#  Enable Log, Log Directory, Log Tags		[Log Parameters]
#
# In order to add/remove any parameter,
# __init__(), saveProfile(), loadProfile(), printProfile() functions have to be altered
#
#

# importing files from the project's profile_io folder
# these files consist of functions - save, load for the parameters in their domain
# these files have been altered to save and load the parameters appropriately
import profile_io.device as Device
import profile_io.sensoract as Sensoract
import profile_io.connection as Connection
import profile_io.log as LogParam
import config as config				# config file contains the PATH to PROJECT FOLDER

# defining path where the profile parameters will be saved
FILE_PATH = config.FOLDER_PATH + '/profile_io/data/'

# defining names of the files in which parameters will be stored
DEVICE_PARAMETERS_FILE = 'device.conf'
SENSORACT_PARAMETERS_FILE = 'sensoract.conf'
CONNECTION_PARAMETERS_FILE = 'connection.conf'
LOG_PARAMETERS_FILE = 'log.conf'

'''
 PROFILE class, contains all the parameters as attribute,
 and functions to save, load, initialize and print the parameters
'''
class PROFILE:
	'''
	 loads default values into the parameters, at the time class in initialized
	 All the parameters have to initialized inside this
	'''
	def __init__(self):
		## DEVICE PARAMETERS ##
		self.Mode = 1   # 1 for Real-time Sampling/Publish
								# 2 for Store & Upload

		self.SamplingPeriod = 1 # time Period to sample readings (in sec)

		##############################
		# in case of
		# Real-time Sampling/Publish
		#
		self.PublishPeriod = 10
		##############################

		##############################
		# in case of
		# Store & Upload
		#
		self.StoreLength = 10
		self.StorePath = '/home/rishav/readings/'
		self.UploadPeriod = 20
		##############################

		## SENSORACT PARAMETERS ##
		self.APIkey = '3773bd8cf9594ca7a2a6c0074f73ace7'
		self.DeviceName = 'RPi-RJ'
		self.DeviceLocation = 'RJ-Home'

		## CONNECTION PARAMETERS ##
		self.ServerIP = 'sensoract.iiitd.edu.in'
		self.ServerPort = 9000
		self.ServerURL = '/upload/wavesegment'

		## LOG PARAMETERS ##
		self.EnableLog = True
		self.LogDir = '/home/rishav/sensors_logs'
		self.LogTags = ('info', 'error', 'readings', 'post_buffer', 'server_response')

	'''
	 saves the profile parameters
	 calling functions using appropriate parameters

	 this function gets called only when profile cannot be loaded
	'''
	def saveProfile(self):
		PARAM = {}			# dict object that is passed to save functions

		PARAM = {'Mode':self.Mode,
				 'SamplingPeriod':self.SamplingPeriod,
				 'PublishPeriod':self.PublishPeriod,
				 'StoreLength':self.StoreLength,
				 'StorePath':self.StorePath,
				 'UploadPeriod':self.UploadPeriod}

		Device.save(FILE_PATH, DEVICE_PARAMETERS_FILE, PARAM)		# saving the device parameters

		PARAM = {'APIkey':self.APIkey,
				 'DeviceName':self.DeviceName,
				 'DeviceLocation':self.DeviceLocation}

		Sensoract.save(FILE_PATH, SENSORACT_PARAMETERS_FILE, PARAM)	# saving the sensoract parameters

		PARAM = {'ServerIP':self.ServerIP,
				 'ServerPort':self.ServerPort,
				 'ServerURL':self.ServerURL}

		Connection.save(FILE_PATH, CONNECTION_PARAMETERS_FILE, PARAM)	# saving the connection parameters

		PARAM = {'EnableLog':self.EnableLog,
				 'LogDir':self.LogDir,
				 'LogTags':self.LogTags}

		LogParam.save(FILE_PATH, LOG_PARAMETERS_FILE, PARAM)	# saving the log parameters

		return

	'''
	 loads the profile parameters
	'''
	def loadProfile(self):
		PARAM = Device.load(FILE_PATH + DEVICE_PARAMETERS_FILE)		# load function to load device parameters
																	# we just pass the path to the file where device parameters are saved
																	# such load functions return dict object containing parameters for that domain
		self.Mode = PARAM['Mode']
		self.SamplingPeriod = PARAM['SamplingPeriod']
		self.PublishPeriod = PARAM['PublishPeriod']
		self.StoreLength = PARAM['StoreLength']
		self.StorePath = PARAM['StorePath']

		if self.StorePath[-1] != '/':				# appends '/' to store path if not present
			self.StorePath = self.StorePath + '/'

		self.UploadPeriod = PARAM['UploadPeriod']

		PARAM = Sensoract.load(FILE_PATH + SENSORACT_PARAMETERS_FILE)	# load function to load sensoract parameters
		self.APIkey = PARAM['APIkey']
		self.DeviceName = PARAM['DeviceName']
		self.DeviceLocation = PARAM['DeviceLocation']

		PARAM = Connection.load(FILE_PATH + CONNECTION_PARAMETERS_FILE)	# load function to load connection parameters
		self.ServerIP = PARAM['ServerIP']
		self.ServerPort = PARAM['ServerPort']
		self.ServerURL = PARAM['ServerURL']

		PARAM = LogParam.load(FILE_PATH + LOG_PARAMETERS_FILE)		# load function to load log parameters

		self.EnableLog = PARAM['EnableLog']
		self.LogDir = PARAM['LogDir']
		self.LogTags = PARAM['LogTags']

		if self.LogDir[-1] != '/':				# appends '/' to log directory if not present
			self.LogDir = self.LogDir + '/'

		return

	'''
	 initializes profile
	 Called at start of the program
	 tries to load profile from files
	 if any error occurs loads default profile and save it
	'''
	def profileInit(self):
		from logger import log

		try:
			#~ raise Exception
			self.loadProfile()
			log('info', 'Loading Profile')

		except Exception as e:
			log('error', '\nError Loading Profile -\n' + str(e.args))
			log('info', '\nUnable to load profile\nLoading Default Values')
			self.__init__()
			self.saveProfile()
		return

	'''
	 logs the profile parameters
	'''
	def printProfile(self):
		from logger import log
		log('info', '\nProfile Parameters -\n' + str(('Mode', self.Mode)) \
					+ '\n' + str(('SamplingPeriod', self.SamplingPeriod)) \
					+ '\n' + str(('PublishPeriod', self.PublishPeriod)) \
					+ '\n' + str(('StoreLength', self.StoreLength)) \
					+ '\n' + str(('StorePath', self.StorePath)) \
					+ '\n' + str(('UploadPeriod', self.UploadPeriod)) \
					+ '\n' + str(('APIkey', self.APIkey)) \
					+ '\n' + str(('DeviceName', self.DeviceName)) \
					+ '\n' + str(('DeviceLocation', self.DeviceLocation)) \
					+ '\n' + str(('ServerIP', self.ServerIP)) \
					+ '\n' + str(('ServerPort', self.ServerPort)) \
					+ '\n' + str(('StorePath', self.StorePath)) \
					+ '\n' + str(('ServerURL', self.ServerURL)) \
					+ '\n' + str(('EnableLog', self.EnableLog)) \
					+ '\n' + str(('LogDir', self.LogDir)) \
					+ '\n' + str(('LogTags', self.LogTags)))

profile = PROFILE()

###
### FOR TESTING PURPOSES ONLY
###
#~ profile.profileInit()
#~
#~ profile.printProfile()
