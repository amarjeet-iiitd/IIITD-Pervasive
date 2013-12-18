import os

def save(PATH, FILE, PARAM):
	if not os.path.exists(PATH):
		os.makedirs(PATH)

	file = open(PATH+FILE, 'w+')
	file.write('ServerIP:' + str(PARAM['ServerIP']))
	file.write('\n')
	file.write('ServerPort:' + str(PARAM['ServerPort']))
	file.write('\n')
	file.write('ServerURL:' + str(PARAM['ServerURL']))
	file.write('\n')

	file.close()
	return

def load(PATH):
	file = open(PATH, 'r')

	PARAM={}

	PARAM['ServerIP'] = file.readline().strip().split(':')[1]
	PARAM['ServerPort'] = int(file.readline().strip().split(':')[1])
	PARAM['ServerURL'] = file.readline().strip().split(':')[1]

##	print('Returning PARAM - ' + str(PARAM))
	return PARAM
