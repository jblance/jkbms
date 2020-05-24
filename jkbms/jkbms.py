#!/usr/bin/env python3
import sys
import math
from bluepy import btle

import logging
log = logging.getLogger('JKBMS-BT')

EXTENDED_RECORD = 1
CELL_DATA       = 2
INFO_RECORD     = 3

getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
getCellInfo = b'\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'

class jkBmsDelegate(btle.DefaultDelegate):
    '''
    BLE delegate to deal with notifications (information) from the JKBMS device
    '''

    def __init__(self, jkbms):
        btle.DefaultDelegate.__init__(self)
        # extra initialisation here
        self.notificationData = bytearray()

    def recordIsComplete(self):
        '''
        '''
        # check for 'ack' record
        if self.notificationData.startswith(bytes.fromhex('aa5590eb')):
            log.info ('notificationData has ACK')
            self.notificationData = bytearray()
            return False # strictly record is complete, but we dont process this
        # check record starts with 'SOR'
        SOR = bytes.fromhex('55aaeb90')
        if not self.notificationData.startswith(SOR):
            log.info ('No SOR found in notificationData')
            self.notificationData = bytearray()
            return False
        # check that length one of the valid lengths (300, 320)
        if len(self.notificationData) == 300 or len(self.notificationData) == 320:
            # check the crc/checksum is correct for the record data
            crc = ord(self.notificationData[-1:])
            calcCrc = self.crc8(self.notificationData[:-1])
            #print (crc, calcCrc)
            if crc == calcCrc:
                return True
        return False

    def processInfoRecord(self, record):
        log.info('Processing info record')
        #print (record)
        del record[0:5]
        #print (record)
        counter = record.pop(0)
        #print (record)
        log.info ('Record number: {}'.format(counter))
        vendorID = bytearray()
        hardwareVersion = bytearray()
        softwareVersion = bytearray()
        uptime = 0
        powerUpTimes = 0
        deviceName = bytearray()
        passCode = bytearray()
        # start at byte 7, go till 0x00 for device model
        while len(record) > 0 :
            _int = record.pop(0)
            #print (_int)
            if _int == 0x00:
                break
            else:
                vendorID += bytes(_int.to_bytes(1, byteorder='big'))
        # consume remaining null bytes
        _int = record.pop(0)
        while _int == 0x00:
            _int = record.pop(0)
        # process hardware version
        hardwareVersion += bytes(_int.to_bytes(1, byteorder='big'))
        while len(record) > 0 :
            _int = record.pop(0)
            #print (_int)
            if _int == 0x00:
                break
            else:
                hardwareVersion += bytes(_int.to_bytes(1, byteorder='big'))
        # consume remaining null bytes
        _int = record.pop(0)
        while _int == 0x00:
            _int = record.pop(0)
        # process software version
        softwareVersion += bytes(_int.to_bytes(1, byteorder='big'))
        while len(record) > 0 :
            _int = record.pop(0)
            #print (_int)
            if _int == 0x00:
                break
            else:
                softwareVersion += bytes(_int.to_bytes(1, byteorder='big'))
        # consume remaining null bytes
        _int = record.pop(0)
        while _int == 0x00:
            _int = record.pop(0)
        # process uptime version
        upTimePos = 0
        uptime = _int * 256**upTimePos
        while len(record) > 0 :
            _int = record.pop(0)
            upTimePos += 1
            #print (_int)
            if _int == 0x00:
                break
            else:
                uptime += _int * 256**upTimePos
        # consume remaining null bytes
        _int = record.pop(0)
        while _int == 0x00:
            _int = record.pop(0)
        # power up times
        powerUpTimes = _int
        # consume remaining null bytes
        _int = record.pop(0)
        while _int == 0x00:
            _int = record.pop(0)
        # device name
        deviceName += bytes(_int.to_bytes(1, byteorder='big'))
        while len(record) > 0 :
            _int = record.pop(0)
            #print (_int)
            if _int == 0x00:
                break
            else:
                deviceName += bytes(_int.to_bytes(1, byteorder='big'))
        # consume remaining null bytes
        _int = record.pop(0)
        while _int == 0x00:
            _int = record.pop(0)
        # Passcode
        passCode += bytes(_int.to_bytes(1, byteorder='big'))
        while len(record) > 0 :
            _int = record.pop(0)
            #print (_int)
            if _int == 0x00:
                break
            else:
                passCode += bytes(_int.to_bytes(1, byteorder='big'))

        log.info ('VendorID: {}'.format(vendorID.decode('utf-8')))
        log.info ('Device Name: {}'.format(deviceName.decode('utf-8')))
        log.debug ('Pass Code: {}'.format(passCode.decode('utf-8')))
        log.info ('Hardware Version: {}'.format(hardwareVersion.decode('utf-8')))
        log.info ('Software Version: {}'.format(softwareVersion.decode('utf-8')))
        daysFloat = uptime/(60*60*24)
        days = math.trunc(daysFloat)
        hoursFloat = (daysFloat - days) * 24
        hours = math.trunc(hoursFloat)
        minutesFloat = (hoursFloat - hours) * 60
        minutes = math.trunc(minutesFloat)
        secondsFloat = (minutesFloat - minutes) * 60
        seconds = math.trunc(secondsFloat)
        log.info ('Uptime: {}D{}H{}M{}S'.format(days, hours, minutes, seconds))

    def processExtendedRecord(self, record):
        log.info('Processing extended record')
        del record[0:5]
        counter = record.pop(0)
        log.info ('Record number: {}'.format(counter))

    def processCellDataRecord(self, record):
        log.info('Processing cell data record')
        del record[0:5]
        counter = record.pop(0)
        log.info ('Record number: {}'.format(counter))
        # Process cell voltages
        volts = []
        size = 4
        number = 24
        for i in range(0, number):
            volts.append(record[0:size])
            del record[0:size]
        for cell, volt in enumerate(volts):
            log.info ('Cell: {:02d}, Volts: {:.4f}'.format(cell+1, self.decodeHex(volt)))

        # Process cell wire resistances
        resistances = []
        size = 4
        number = 25
        for i in range(0, number):
            resistances.append(record[0:size])
            del record[0:size]
        for cell, resistance in enumerate(resistances):
            log.info ('Cell: {:02d}, Resistance: {:.4f}'.format(cell, self.decodeHex(resistance)))
        print (record)

    def processRecord(self, record):
        recordType = record[4]
        counter = record[5]
        if recordType == INFO_RECORD:
            self.processInfoRecord(record)
        elif recordType == EXTENDED_RECORD:
            self.processExtendedRecord(record)
        elif recordType == CELL_DATA:
            self.processCellDataRecord(record)
        else:
            log.info('Unknown record type')


    def handleNotification(self, handle, data):
        # handle is the handle of the characteristic / descriptor that posted the notification
        # data is the data in this notification - may take multiple notifications to get all of a message
        log.debug ('From handle: {:#04x} Got {} bytes of data'.format(handle, len(data)))
        self.notificationData += bytearray(data)
        if self.recordIsComplete():
            record = self.notificationData
            self.notificationData = bytearray()
            self.processRecord(record)

class jkBMS:
    """
    JK BMS Command Library
    - represents a JK BMS
    """

    def __str__(self):
        return 'JKBMS instance --- name: {}, model: {}, mac: {}, command: {}, tag: {}, format: {}, records: {}, maxConnectionAttempts: {}, mqttBroker: {}'.format(self.name, self.model, self.mac, self.command, self.tag, self.format, self.records, self.maxConnectionAttempts, self.mqttBroker)


    def __init__(self, name, model, mac, command, tag, format, records=1, maxConnectionAttempts=3, mqttBroker='localhost'):
        '''
        '''
        self.name = name
        self.model = model
        self.mac = mac
        self.command = command
        self.tag = tag
        self.format = format
        self.records = records
        self.maxConnectionAttempts = maxConnectionAttempts
        self.mqttBroker = mqttBroker
        self.device = btle.Peripheral(None)
        log.debug('Config data - name: {}, model: {}, mac: {}, command: {}, tag: {}, format: {}'.format(self.name, self.model, self.mac, self.command, self.tag, self.format))
        log.debug('Additional config - records: {}, maxConnectionAttempts: {}, mqttBroker: {}'.format(self.records, self.maxConnectionAttempts, self.mqttBroker))

    def connect(self):
        # Intialise BLE device
        self.device = btle.Peripheral(None)
        self.device.withDelegate( jkBmsDelegate(self) )
        # Connect to BLE Device
        connected = False
        attempts = 0
        log.info('Attempting to connect to {}'.format(self.name))
        while not connected:
            attempts += 1
            if attempts > self.maxConnectionAttempts:
                log.warning ('Cannot connect to {} with mac {} - exceeded {} attempts'.format(self.name, self.mac, attempts - 1))
                sys.exit(1)
            try:
                self.device.connect(self.mac)
                connected = True
            except Exception as e:
                continue
        return connected

    def getBLEData(self):
        # Get the device name
        serviceId = self.device.getServiceByUUID(btle.AssignedNumbers.genericAccess)
        deviceName = serviceId.getCharacteristics(btle.AssignedNumbers.deviceName)[0]
        log.info('Connected to {}'.format(deviceName.read()))

        # Connect to the notify service
        serviceNotifyUuid = 'ffe0'
        serviceNotify = self.device.getServiceByUUID(serviceNotifyUuid)

        # Get the handles that we need to talk to
        ### Read
        characteristicReadUuid = 'ffe3'
        characteristicRead = serviceNotify.getCharacteristics(characteristicReadUuid)[0]
        handleRead = characteristicRead.getHandle()
        log.info ('Read characteristic: {}, handle {:x}'.format(characteristicRead, handleRead))

        ### TODO sort below
        # Need to dynamically find this handle....
        log.info ('Enable 0x0b handle', self.device.writeCharacteristic(0x0b, b'\x01\x00'))
        log.info ('Enable read handle', self.device.writeCharacteristic(handleRead, b'\x01\x00'))
        log.info ('Write getInfo to read handle', self.device.writeCharacteristic(handleRead, getInfo))
        secs = 0
        while True:
            if self.device.waitForNotifications(1.0):
                continue
            secs += 1
            if secs > 5 :
                break

        log.info ('Write getCellInfo to read handle', self.device.writeCharacteristic(handleRead, getCellInfo))
        loops = 0
        recordsToGrab = 1
        log.info ('Grabbing {} records (after inital response)'.format(recordsToGrab))

        while True:
            loops += 1
            if loops > recordsToGrab * 15 + 16:
                break
            if self.device.waitForNotifications(1.0):
                continue

    def disconnect(self):
        log.info ('Disconnecting...')
        self.device.disconnect()
