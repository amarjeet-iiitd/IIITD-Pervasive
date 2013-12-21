import ConfigParser

import sys
import logging

from bacpypes.debugging import Logging, ModuleLogger
from bacpypes.consolelogging import ConsoleLogHandler
from bacpypes.consolecmd import ConsoleCmd

from bacpypes.core import run, stop

from bacpypes.pdu import Address, GlobalBroadcast
from bacpypes.app import LocalDeviceObject, BIPSimpleApplication
from bacpypes.object import get_object_class, get_datatype

from bacpypes.apdu import WhoIsRequest, IAmRequest, \
    ReadPropertyRequest, Error, AbortPDU, ReadPropertyACK
from bacpypes.primitivedata import Unsigned
from bacpypes.constructeddata import Array
from bacpypes.basetypes import ServicesSupported
from bacpypes.errors import DecodingError

from bacpypes.task import TaskManager
TaskManager()

application = None
#Ensure all instances of bacpypes on the same machine run on different ports!
bacpypesip = "10.0.0.5:47811"


class SynchronousApplication(BIPSimpleApplication):

    def __init__(self, local_address, routers):
        local_device_object = \
            LocalDeviceObject(objectName='IIITD BACnet Controller',
                              objectIdentifier=0)
        BIPSimpleApplication.__init__(self, local_device_object,
                local_address)

#        for (net, address) in routers.items():
#            self.nsap.add_router_references(self.nsap.adapters[0],
#                    Address(address), [net])

    def confirmation(self, apdu):
        self.apdu = apdu
        stop()

    def make_request(self, request):
        self.request(request)
        run()
        return self.apdu

def ReadProperty(
    object_type,
    object_instance,
    property_id,
    address,
    ):
    
    global application
    if (application == None):
        local_address = bacpypesip
        routers = None
        application = SynchronousApplication(local_address, routers)
    
    request = ReadPropertyRequest(objectIdentifier=(object_type,
                                  int(object_instance)),
                                  propertyIdentifier=property_id)
    request.pduDestination = Address(address)
    apdu = application.make_request(request)

    if isinstance(apdu, Error):
        sys.stdout.write('error: %s\n' % (apdu.errorCode, ))
        sys.stdout.flush()
        return 'Error!'
    elif isinstance(apdu, AbortPDU):

        apdu.debug_contents()
        return 'Error: AbortPDU'
    elif isinstance(request, ReadPropertyRequest) and isinstance(apdu,
            ReadPropertyACK):

        datatype = get_datatype(apdu.objectIdentifier[0],
                                apdu.propertyIdentifier)
        if not datatype:
            raise TypeError, 'unknown datatype'

        if issubclass(datatype, Array) and apdu.propertyArrayIndex\
             is not None:
            if apdu.propertyArrayIndex == 0:
                value = apdu.propertyValue.cast_out(Unsigned)
            else:
                value = apdu.propertyValue.cast_out(datatype.subtype)
        else:
            value = apdu.propertyValue.cast_out(datatype)
        if(value=="inactive"):
            value=0.0
        if (value=="active"):
            value=1.0
        return value


class BacnetMeterPoint:
    def __init__(self, ip, obj_type, inst_id, prop_type, value_type, value_unit, rate, wing, point_floor, point_building, point_source, point_type, point_loadtype, point_subloadtype, point_supplytype, meterid):#Add any new Metadata to be added here
        self.ip = ip
        self.obj_type = obj_type
        self.inst_id = inst_id
        self.prop_type = prop_type
        self.value_type = value_type        #Physical Type
        self.value_unit = value_unit
        self.rate = rate
        self.point_floor = point_floor
        self.point_building = point_building
        self.point_source = point_source
        self.point_type = point_type
        self.point_loadtype = point_loadtype
        self.point_subloadtype = point_subloadtype
        self.point_supplytype = point_supplytype
        self.wing = wing
        self.meterid = meterid
        #Add any new Metadata to be added here

def configreadkey(filename, section, key):
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform=str
    cfg.read(filename)
    return filter(None, cfg.get(section, key).split(','))

def configeditkey(filename, section, key, value):
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform=str
    cfg.read(filename)
    cfg.set(section, key, value)
    with open(filename, 'w') as configfile:
        cfg.write(configfile)
    

def configread(filename):
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform=str
    cfg.read(filename)
    inst_id=filter(None, cfg.get("/BMS", "inst_id").split(','))
    obj_type =filter(None, cfg.get("/BMS", "obj_type").split(','))
    prop_type=filter(None, cfg.get("/BMS", "prop_type").split(','))
    value_type=filter(None, cfg.get("/BMS", "value_type").split(','))
    value_unit=filter(None, cfg.get("/BMS", "value_unit").split(','))
    rate=filter(None, cfg.get("/BMS", "rate").split(','))
    point_floor=filter(None, cfg.get("/BMS", "point_floor").split(','))
    point_building=filter(None, cfg.get("/BMS", "point_building").split(','))
    point_source=filter(None, cfg.get("/BMS", "point_source").split(','))
    point_type=filter(None, cfg.get("/BMS", "point_type").split(','))
    point_loadtype=filter(None, cfg.get("/BMS", "point_loadtype").split(','))
    point_subloadtype=filter(None, cfg.get("/BMS", "point_subloadtype").split(','))
    point_supplytype=filter(None, cfg.get("/BMS", "point_supplytype").split(','))
    wing=filter(None, cfg.get("/BMS", "wing").split(','))
    meterid=filter(None, cfg.get("/BMS", "meterid").split(','))
    ip=filter(None, cfg.get("/BMS", "ip").split(','))
    #Add any new Metadata to be added here
    
    listofpoints = []
    for i in xrange(0, len(inst_id)):
        listofpoints.append(BacnetMeterPoint(ip[i], obj_type[i], inst_id[i], prop_type[i], value_type[i], value_unit[i], rate[i], wing[i], point_floor[i], point_building[i], point_source[i], point_type[i], point_loadtype[i], point_subloadtype[i], point_supplytype[i], meterid[i]))#Add any new Metadata to be added here
    return listofpoints
    
def configreadpoint(filename, i):
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform=str
    cfg.read(filename)
    inst_id=filter(None, cfg.get("/BMS", "inst_id").split(','))
    obj_type =filter(None, cfg.get("/BMS", "obj_type").split(','))
    prop_type=filter(None, cfg.get("/BMS", "prop_type").split(','))
    value_type=filter(None, cfg.get("/BMS", "value_type").split(','))
    value_unit=filter(None, cfg.get("/BMS", "value_unit").split(','))
    rate=filter(None, cfg.get("/BMS", "rate").split(','))
    point_floor=filter(None, cfg.get("/BMS", "point_floor").split(','))
    point_building=filter(None, cfg.get("/BMS", "point_building").split(','))
    point_source=filter(None, cfg.get("/BMS", "point_source").split(','))
    point_type=filter(None, cfg.get("/BMS", "point_type").split(','))
    point_loadtype=filter(None, cfg.get("/BMS", "point_loadtype").split(','))
    point_subloadtype=filter(None, cfg.get("/BMS", "point_subloadtype").split(','))
    point_supplytype=filter(None, cfg.get("/BMS", "point_supplytype").split(','))
    wing=filter(None, cfg.get("/BMS", "wing").split(','))
    meterid=filter(None, cfg.get("/BMS", "meterid").split(','))
    ip=filter(None, cfg.get("/BMS", "ip").split(','))
    #Add any new Metadata to be added here
    
    return BacnetMeterPoint(ip[i], obj_type[i], inst_id[i], prop_type[i], value_type[i], value_unit[i], rate[i], wing[i], point_floor[i], point_building[i], point_source[i], point_type[i], point_loadtype[i], point_subloadtype[i], point_supplytype[i], meterid[i])#Add any new Metadata to be added here

def configaddpoint(filename, point):
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform=str
    cfg.read(filename)
    
    inst_id=filter(None, cfg.get("/BMS", "inst_id").split(','))
    obj_type =filter(None, cfg.get("/BMS", "obj_type").split(','))
    prop_type=filter(None, cfg.get("/BMS", "prop_type").split(','))
    value_type=filter(None, cfg.get("/BMS", "value_type").split(','))
    value_unit=filter(None, cfg.get("/BMS", "value_unit").split(','))
    rate=filter(None, cfg.get("/BMS", "rate").split(','))
    point_floor=filter(None, cfg.get("/BMS", "point_floor").split(','))
    point_building=filter(None, cfg.get("/BMS", "point_building").split(','))
    point_source=filter(None, cfg.get("/BMS", "point_source").split(','))
    point_type=filter(None, cfg.get("/BMS", "point_type").split(','))
    point_loadtype=filter(None, cfg.get("/BMS", "point_loadtype").split(','))
    point_subloadtype=filter(None, cfg.get("/BMS", "point_subloadtype").split(','))
    point_supplytype=filter(None, cfg.get("/BMS", "point_supplytype").split(','))
    wing=filter(None, cfg.get("/BMS", "wing").split(','))
    meterid=filter(None, cfg.get("/BMS", "meterid").split(','))
    ip=filter(None, cfg.get("/BMS", "ip").split(','))
    #Add any new Metadata to be added here
    
    inst_id.append(point.inst_id)
    obj_type.append(point.obj_type)
    prop_type.append(point.prop_type)
    value_type.append(point.value_type)
    value_unit.append(point.value_unit)
    rate.append(point.rate)
    point_floor.append(point.point_floor)
    point_building.append(point.point_building)
    point_source.append(point.point_source)
    point_type.append(point.point_type)
    point_loadtype.append(point.point_loadtype)
    point_subloadtype.append(point.point_subloadtype)
    point_supplytype.append(point.point_supplytype)
    wing.append(point.wing)
    meterid.append(point.meterid)
    ip.append(point.ip)
    #Add any new Metadata to be added here
    
    cfg.set("/BMS", "inst_id", ",".join(inst_id))
    cfg.set("/BMS", "obj_type", ",".join(obj_type))
    cfg.set("/BMS", "prop_type", ",".join(prop_type))
    cfg.set("/BMS", "value_type", ",".join(value_type))
    cfg.set("/BMS", "value_unit", ",".join(value_unit))
    cfg.set("/BMS", "rate", ",".join(rate))
    cfg.set("/BMS", "point_floor", ",".join(point_floor))
    cfg.set("/BMS", "point_building", ",".join(point_building))
    cfg.set("/BMS", "point_source", ",".join(point_source))
    cfg.set("/BMS", "point_type", ",".join(point_type))
    cfg.set("/BMS", "point_loadtype", ",".join(point_loadtype))
    cfg.set("/BMS", "point_subloadtype", ",".join(point_subloadtype))
    cfg.set("/BMS", "point_supplytype", ",".join(point_supplytype))
    cfg.set("/BMS", "wing", ",".join(wing))
    cfg.set("/BMS", "meterid", ",".join(meterid))
    cfg.set("/BMS", "ip", ",".join(ip))
    #Add any new Metadata to be added here
    
    with open(filename, 'w') as configfile:
        cfg.write(configfile)

def configdeletepoint(filename, index):
    cfg = ConfigParser.ConfigParser()
    cfg.optionxform=str
    cfg.read(filename)
    
    inst_id=filter(None, cfg.get("/BMS", "inst_id").split(','))
    obj_type =filter(None, cfg.get("/BMS", "obj_type").split(','))
    prop_type=filter(None, cfg.get("/BMS", "prop_type").split(','))
    value_type=filter(None, cfg.get("/BMS", "value_type").split(','))
    value_unit=filter(None, cfg.get("/BMS", "value_unit").split(','))
    rate=filter(None, cfg.get("/BMS", "rate").split(','))
    point_floor=filter(None, cfg.get("/BMS", "point_floor").split(','))
    point_building=filter(None, cfg.get("/BMS", "point_building").split(','))
    point_source=filter(None, cfg.get("/BMS", "point_source").split(','))
    point_type=filter(None, cfg.get("/BMS", "point_type").split(','))
    point_loadtype=filter(None, cfg.get("/BMS", "point_loadtype").split(','))
    point_subloadtype=filter(None, cfg.get("/BMS", "point_subloadtype").split(','))
    point_supplytype=filter(None, cfg.get("/BMS", "point_supplytype").split(','))
    wing=filter(None, cfg.get("/BMS", "wing").split(','))
    meterid=filter(None, cfg.get("/BMS", "meterid").split(','))
    ip=filter(None, cfg.get("/BMS", "ip").split(','))
    #Add any new Metadata to be added here
    
    del inst_id[index]
    del obj_type[index]
    del prop_type[index]
    del value_type[index]
    del value_unit[index]
    del rate[index]
    del point_floor[index]
    del point_building[index]
    del point_source[index]
    del point_type[index]
    del point_loadtype[index]
    del point_subloadtype[index]
    del point_supplytype[index]
    del wing[index]
    del meterid[index]
    del ip[index]
    #Add any new Metadata to be added here
    
    cfg.set("/BMS", "inst_id", ",".join(inst_id))
    cfg.set("/BMS", "obj_type", ",".join(obj_type))
    cfg.set("/BMS", "prop_type", ",".join(prop_type))
    cfg.set("/BMS", "value_type", ",".join(value_type))
    cfg.set("/BMS", "value_unit", ",".join(value_unit))
    cfg.set("/BMS", "rate", ",".join(rate))
    cfg.set("/BMS", "point_floor", ",".join(point_floor))
    cfg.set("/BMS", "point_building", ",".join(point_building))
    cfg.set("/BMS", "point_source", ",".join(point_source))
    cfg.set("/BMS", "point_type", ",".join(point_type))
    cfg.set("/BMS", "point_loadtype", ",".join(point_loadtype))
    cfg.set("/BMS", "point_subloadtype", ",".join(point_subloadtype))
    cfg.set("/BMS", "point_supplytype", ",".join(point_supplytype))
    cfg.set("/BMS", "wing", ",".join(wing))
    cfg.set("/BMS", "meterid", ",".join(meterid))
    cfg.set("/BMS", "ip", ",".join(ip))
    #Add any new Metadata to be added here
    
    with open(filename, 'w') as configfile:
        cfg.write(configfile)
