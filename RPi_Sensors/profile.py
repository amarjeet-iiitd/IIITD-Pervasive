
class PROFILE:
    def __init__(self):
        self.SamplingPeriod = 1
        self.PublishPeriod = 10
        
        self.APIkey = '3773bd8cf9594ca7a2a6c0074f73ace7'
        self.DeviceName = 'RPi-RJ'
        self.DeviceLocation = 'RJ-Home'
        
        self.ServerIP = 'sensoract.iiitd.edu.in'
#         self.ServerIP = '192.168.1.2'
        self.ServerPort = 9000
        self.ServerURL = "/upload/wavesegment"
        
    def saveProfile(self):
        profileFile = open('/var/www/profile', 'r+')
        
        writeString = str(self.SamplingPeriod) + '||--||--||'
        writeString += str(self.PublishPeriod) + '||--||--||'
        writeString += self.APIkey + '||--||--||'
        writeString += self.DeviceName + '||--||--||'
        writeString += self.DeviceLocation + '||--||--||'
        writeString += self.ServerIP + '||--||--||'
        writeString += str(self.ServerPort) + '||--||--||'
        writeString += self.ServerURL

        profileFile.write(writeString)
        profileFile.close()
        print('Saved Profile')
        return
    
    def loadProfile(self):
        profileFile = open('/var/www/profile', 'r+')
        readString = profileFile.readline()
        profileFile.close()
#         print(readString)
        
        parameters = str.split(readString, '||--||--||')
        
#         print(parameters)

        self.SamplingPeriod = int(parameters[0])
        self.PublishPeriod = int(parameters[1])
        
        self.APIkey = parameters[2]
        self.DeviceName = parameters[3]
        self.DeviceLocation = parameters[4]
        
        self.ServerIP = parameters[5]
        self.ServerPort = int(parameters[6])
        self.ServerURL = parameters[7]
        
        print('Loaded Profile')    
        return
    
    def profileInit(self):
        try:
            profileFile = open('/var/www/profile')
            self.loadProfile()
            profileFile.close()
        except:
            print('Loading Default Values')
            #self.saveProfile()
        return
        
    def printProfile(self):
        print 'SamplingPeriod', self.SamplingPeriod
        print 'PublishPeriod', self.PublishPeriod
        print 'APIkey', self.APIkey
        print 'DeviceName', self.DeviceName
        print 'DeviceLocation', self.DeviceLocation
        print 'ServerIP', self.ServerIP
        print 'SeverPort', self.ServerPort
        print 'ServerURL', self.ServerURL
        return
    
profile = PROFILE()

#profile.profileInit()
