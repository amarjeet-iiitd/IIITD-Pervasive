import os

def save(PATH, FILE, PARAM):
	if not os.path.exists(PATH):
		os.makedirs(PATH)

	file = open(PATH+FILE, 'w+')
	file.write('EnableLog:' + str(PARAM['EnableLog']))
	file.write('\n')
	file.write('LogDir:' + str(PARAM['LogDir']))
	file.write('\n')
	file.write('LogTags:' + str(PARAM['LogTags'])[1:-1].replace("'", '').replace(' ', ''))
	file.write('\n')
	file.close()
	return

def load(PATH):
	file = open(PATH, 'r')

	PARAM={}

	PARAM['EnableLog'] = file.readline().strip().split(':')[1]
	if PARAM['EnableLog'] == 'True':
		PARAM['EnableLog'] = True
	else:
		PARAM['EnableLog'] = False

	PARAM['LogDir'] = file.readline().strip().split(':')[1]
	PARAM['LogTags'] = ()
	tags = file.readline().strip().split(':')[1].split(',')
	
	for i in tags:
		PARAM['LogTags'] += (i,)
	
	# print('Returning PARAM - ' + str(PARAM))  ## TESTING
	return PARAM

# TESTING
# print load('/home/rishav/rpi-sensors/V8/profile_io/data/log.conf')
