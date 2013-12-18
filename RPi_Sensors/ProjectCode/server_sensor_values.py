
import PIR
import interfacei2clightsensor as Light
import ds1820_final_1 as Temp


print(Temp.read_temp())

Light.APDS_init()
print(Light.APDS_read())

print(PIR.PIR_Read())


#~ # TESTING
#~ import random
#~ print(int(random.random()*10))
#~ print(int(random.random()*10))
#~ print(int(random.random()*10))
