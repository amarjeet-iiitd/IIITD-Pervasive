import threading

timestamp = 0
lockTimestamp = threading.Lock()

alarmCount = 0
alarmRead = 0
alarmUpload = 0

Sensors = {'Temp':'Temp', 'Light':'Light', 'PIR':'PIR'}

TempReadings = ()

LightReadings = ()

PirReadings = ()

postQueue = []
lockQueue = threading.Lock()

POST_buffer = ''

Current_Store_Folder = ''
