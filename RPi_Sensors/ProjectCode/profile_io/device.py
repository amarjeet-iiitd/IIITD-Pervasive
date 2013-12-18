import os

def save(PATH, FILE, PARAM):
	if not os.path.exists(PATH):
		os.makedirs(PATH)

	file = open(PATH+FILE, 'w+')
	file.write('Mode:' + str(PARAM['Mode']))
	file.write('\n')
	file.write('SamplingPeriod:' + str(PARAM['SamplingPeriod']))
	file.write('\n')
	file.write('PublishPeriod:' + str(PARAM['PublishPeriod']))
	file.write('\n')
	file.write('StoreLength:' + str(PARAM['StoreLength']))
	file.write('\n')
	file.write('StorePath:' + str(PARAM['StorePath']))
	file.write('\n')
	file.write('UploadPeriod:' + str(PARAM['UploadPeriod']))
	file.write('\n')

	file.close()
	return

def load(PATH):
	file = open(PATH, 'r')

	PARAM={}

	PARAM['Mode'] = int(file.readline().strip().split(':')[1])
	PARAM['SamplingPeriod'] = int(file.readline().strip().split(':')[1])
	PARAM['PublishPeriod'] = int(file.readline().strip().split(':')[1])
	PARAM['StoreLength'] = int(file.readline().strip().split(':')[1])
	PARAM['StorePath'] = file.readline().strip().split(':')[1]
	PARAM['UploadPeriod'] = int(file.readline().strip().split(':')[1])

##	print('Returning PARAM - ' + str(PARAM))
	return PARAM
