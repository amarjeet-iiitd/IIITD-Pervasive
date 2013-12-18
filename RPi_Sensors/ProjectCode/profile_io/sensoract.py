import os

def save(PATH, FILE, PARAM):
	if not os.path.exists(PATH):
		os.makedirs(PATH)

	file = open(PATH+FILE, 'w+')
	file.write('APIkey:' + str(PARAM['APIkey']))
	file.write('\n')
	file.write('DeviceName:' + str(PARAM['DeviceName']))
	file.write('\n')
	file.write('DeviceLocation:' + str(PARAM['DeviceLocation']))
	file.write('\n')

	file.close()
	return

def load(PATH):
	file = open(PATH, 'r')

	PARAM={}

	PARAM['APIkey'] = file.readline().strip().split(':')[1]
	PARAM['DeviceName'] = file.readline().strip().split(':')[1]
	PARAM['DeviceLocation'] = file.readline().strip().split(':')[1]

##	print('Returning PARAM - ' + str(PARAM))
	return PARAM
