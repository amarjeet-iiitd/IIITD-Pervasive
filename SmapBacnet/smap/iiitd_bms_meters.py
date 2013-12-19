#!/usr/bin/python
# -*- coding: utf-8 -*-
#Author Romil Bhardwaj 
#romil11092@iiitd.ac.in
import os
from os.path import join
from smap.driver import SmapDriver, util
import struct
from smap import core, actuate

import sys
import logging

from ConfigParser import ConfigParser

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

#Smap BACnet Application definition. SynchronousApplication because it runs only when required, instead of running all the time in the background.
class SynchronousApplication(BIPSimpleApplication):

    def __init__(self, local_address, routers):
        local_device_object = \
            LocalDeviceObject(objectName='IIITD BACnet Meter Controller',
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

#BACnet readproperty function
def ReadProperty(
    object_type,
    object_instance,
    property_id,
    address,
    ):

    request = ReadPropertyRequest(objectIdentifier=(object_type,
                                  int(object_instance)),
                                  propertyIdentifier=property_id)
    request.pduDestination = Address(address)
    apdu = application.make_request(request)
    #Error handling
    if isinstance(apdu, Error):
        sys.stdout.write('error: %s\n' % (apdu.errorCode, ))
        sys.stdout.flush()
        return 'Error!'
    #Error handling
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
        if(value=="inactive"): #For binary values
            value=0.0
        if (value=="active"):
            value=1.0
        return value

class BacnetPoint:
    def __init__(self, ip, obj_type, inst_id, prop_type, value_type, value_unit, rate, wing, point_floor, point_building, point_source, point_type, point_loadtype, point_subloadtype, point_supplytype, meterid):
        self.ip = ip
        self.obj_type = obj_type
        self.inst_id = inst_id
        self.prop_type = prop_type
        self.value_type = value_type        #Physical Type, eg Power
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

class BACnetBMSMetersDriver(SmapDriver):

    def setup(self, opts):

        if type(opts.get('inst_ids')) == str:
            print "Reading Single Point!"
            self.ips = [str(opts.get('ip'))]
            self.obj_types = [str(opts.get('obj_type'))]
            self.inst_ids = [int(opts.get('inst_ids'))]
            self.prop_types = [str(opts.get('prop_type'))]
            self.value_types = [str(opts.get('value_types'))]
            self.value_units = [str(opts.get('value_unit'))]
            self.rates = [int(opts.get('rate'))]
            self.point_floors = [int(opts.get('point_floor'))]
            self.point_builings = [str(opts.get('point_builing'))]
            self.point_sources = [str(opts.get('point_source'))]
            self.point_types = [str(opts.get('point_type'))]
            self.point_loadtypes = [str(opts.get('point_source'))]
            self.point_subloadtypes = [str(opts.get('point_source'))]
            self.point_supplytypes = [str(opts.get('point_supplytype'))]
            self.wings = [str(opts.get('wing'))]
            self.meterids = [str(opts.get('meterid'))]
        else:
            print "Reading Multiple Points!"
            self.ips = [str(x) for x in opts.get('ip')]
            self.obj_types = [str(x) for x in opts.get('obj_type')]
            self.inst_ids = [int(x) for x in opts.get('inst_id')]
            self.prop_types = [str(x) for x in opts.get('prop_type')]
            self.value_types = [str(x) for x in opts.get('value_type')]
            self.value_units = [str(x) for x in opts.get('value_unit')]
            self.rates = [int(x) for x in opts.get('rate')]
            self.point_floors = [int(x) for x in opts.get('point_floor')]
            self.point_buildings = [str(x) for x in opts.get('point_building')]
            self.point_sources = [str(x) for x in opts.get('point_source')]
            self.point_types = [str(x) for x in opts.get('point_type')]
            self.point_loadtypes = [str(x) for x in opts.get('point_loadtype')]
            self.point_subloadtypes = [str(x) for x in opts.get('point_subloadtype')]
            self.point_supplytypes = [str(x) for x in opts.get('point_supplytype')]
            self.wings = [str(x) for x in opts.get('wing')]
            self.meterids = [str(x) for x in opts.get('meterid')]

        self.point_count = len(self.inst_ids)

        points = []
        print self.ips
        #Add all read points to collection of points
        for x in xrange(0, self.point_count):
            points += [BacnetPoint(
                self.ips[x],
                self.obj_types[x],
                self.inst_ids[x],
                self.prop_types[x],
                self.value_types[x],
                self.value_units[x],
                self.rates[x],
                self.wings[x],
                self.point_floors[x],
                self.point_buildings[x],
                self.point_sources[x],
                self.point_types[x],
                self.point_loadtypes[x],
                self.point_subloadtypes[x],
                self.point_supplytypes[x],
                self.meterids[x]
                )]

        """del self.ips
        del self.obj_types
        del self.inst_ids
        del self.prop_types
        del self.value_types
        del self.value_units
        del self.rates
        del self.point_floors
        del self.point_buildings
        del self.point_sources
        del self.point_types
        del self.point_loadtypes
        del self.point_subloadtypes
        del self.point_supplytypes
        del self.wings
        del self.meterids"""

        self.current = 0  # #Index for the queue

        self.SLOWEST_POSSIBLE_RATE = 64
        self.queue = []
        #Instantiate empty queue
        for x in xrange(0, self.SLOWEST_POSSIBLE_RATE):
            self.queue += [[]]
        #Add all points to the list of points to be read
        for self.current in xrange(0, self.point_count):
            self.queue[self.current].append(points[self.current])

        self.current = 0

        for x in points:
            #Creating paths as required
            path = ('/' + str(x.point_source))
            if (self.get_collection(path) == None):
                print ("Adding " + path)
                self.add_collection(path)
            path = ('/' + str(x.point_source) + '/' + str(x.point_building))
            if (self.get_collection(path) == None):
                print ("Adding " + path)
                self.add_collection(path)
            path = ('/' + str(x.point_source) + '/' + str(x.point_building) + '/Meter' + str(x.meterid))
            if (self.get_collection(path) == None):
                print ("Adding " + path)
                self.add_collection(path)

            self.point_coll = self.get_collection(path)
            print self.point_coll
            #Add metadata to the whole collection
            self.point_coll['Metadata'] = \
                {'Instrument': {'Manufacturer': 'Schneider Electric',
                 'Model': 'EM6400'}}
            #print "Adding TimeSeries"
            ts = self.add_timeseries('/' + str(x.point_source) + '/' + str(x.point_building) + '/Meter' + str(x.meterid) + '/' + str(x.value_type), x.value_unit, data_type='double',timezone='Asia/Kolkata')
            #Add Metadata to specific timeseries
            ts['Metadata'] = {'Instrument': {'SamplingPeriod': str(str(x.rate) + ' Seconds')}, 'Location': {'Floor': str(x.point_floor), 'Building': x.point_building}, 'Extra': {
                'PhysicalParameter': x.value_type,
                'IP': x.ip,
                'MeterID': x.meterid,
                'LoadType': x.point_loadtype,
                'SubLoadType': x.point_subloadtype,
                'SupplyType': x.point_supplytype,
                'Type': x.point_type,
                'Wing': x.wing
                },'BACnet': {
                'BACnetObjType': x.obj_type,
                'BACnetInstID': x.inst_id
                }}

        print "Initializing BACpypes!"

        #INIT BACPYPES
        local_address = str(opts.get('bacpypesdeviceip'))
        routers = None
        global application
        application = SynchronousApplication(local_address, routers)

        self.res = None
        self.current = 0

    def start(self):
        print "Starting function."
        util.periodicSequentialCall(self.read).start(1)

    def read(self):
        for x in self.queue[self.current]:
            t = util.now()
            self.res = ReadProperty(x.obj_type, x.inst_id, "presentValue", x.ip)      #ReadBacpypes
            print ("Reading Meter" + x.meterid + " " + x.value_type)
            value = self.res
            print value

            if self.res == None:
                continue

            self.add('/' + str(x.point_source) + '/' + str(x.point_building) + '/Meter' + str(x.meterid) + '/' + str(x.value_type), t, value)

        pop_count = len(self.queue[self.current])
        #Pop and append the point to its corresponding list when its to be read next.
        for x in xrange(0, pop_count):
            popped = self.queue[self.current].pop(0)
            next_index = (self.current + popped.rate)\
                 % self.SLOWEST_POSSIBLE_RATE
            while len(self.queue[next_index]) == 2:
                next_index += 1
                if next_index == self.SLOWEST_POSSIBLE_RATE:
                    next_index = 0

            self.queue[next_index].append(popped)

        self.current += 1
        if self.current == self.SLOWEST_POSSIBLE_RATE:
            self.current = 0
