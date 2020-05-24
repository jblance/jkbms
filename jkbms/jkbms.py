#!/usr/bin/env python3
import sys
import math
from bluepy import btle

import logging
log = logging.getLogger('JKBMS-BT')
# setup logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# set default log levels
log.setLevel(logging.CRITICAL)
logging.basicConfig()

import configparser
config = configparser.ConfigParser()

EXTENDED_RECORD = 1
CELL_DATA       = 2
INFO_RECORD     = 3


class jkBmsDelegate(btle.DefaultDelegate):
    '''
    BLE delegate to deal with notifications (information) from the JKBMS device
    '''

    def __init__(self, params):
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

    def decodeHex(self, hexString):
        '''
        # For bluetooth battery monitor (model JK-B1A24S)
        # - which encodes cell voltages into 4 bytes (hex encoded)
        # - example 5f806240 -> 3.539
        '''
        answer = 0.0

        # Make sure supplied String is long enough
        if len(hexString) != 4:
            log.warning('Hex encoded value must be 4 bytes long. Was {} length'.format(len(hexString)))
            return None

        # Process most significant byte (position 3)
        byte1 = hexString[3]
        if byte1 == 0x0:
            return answer
        byte1Low = byte1 - 0x40
        answer = (2**(byte1Low*2))*2
        step1 = answer / 8.0
        step2 = answer / 128.0
        step3 = answer / 2048.0
        step4 = answer / 32768.0
        step5 = answer / 524288.0
        step6 = answer / 8388608.0

        # position 2
        byte2 = hexString[2]
        byte2High = byte2 >> 4
        byte2Low = byte2 & 0xf
        if byte2High & 8:
            #answer += (byte2High * step1 * 2) + (byte2Low * step2)
            answer += ((byte2High - 8) * step1 * 2) + (8 * step1) + (byte2Low * step2)
        else:
            answer += (byte2High * step1) + (byte2Low * step2)

        # position 1
        byte3 = hexString[1]
        byte3High = byte3 >> 4
        byte3Low = byte3 & 0xf
        answer += (byte3High * step3) + (byte3Low * step4)

        # position 0
        byte4 = hexString[0]
        byte4High = byte4 >> 4
        byte4Low = byte4 & 0xf
        answer += (byte4High * step5) + (byte4Low * step6)

        log.debug ('hexString: {}'.format(hexString))
        log.debug ('hex(byte1): {}'.format(hex(byte1)))
        log.debug ('byte1Low: {}'.format(byte1Low))
        #log.debug ('byte2', byte2)
        log.debug ('hex(byte2): {}'.format(hex(byte2)))
        log.debug ('byte2High: {}'.format(byte2High))
        log.debug ('byte2Low: {}'.format(byte2Low))
        #log.debug ('byte3', byte3)
        log.debug ('hex(byte3): {}'.format(hex(byte3)))
        log.debug ('byte3High: {}'.format(byte3High))
        log.debug ('byte3Low: {}'.format(byte3Low))
        #log.debug ('byte4', byte4)
        log.debug ('hex(byte4): {}'.format(hex(byte4)))
        log.debug ('byte4High: {}'.format(byte4High))
        log.debug ('byte4Low: {}'.format(byte4Low))

        log.debug ('step1: {}'.format(step1))
        log.debug ('step2: {}'.format(step2))
        log.debug ('step3: {}'.format(step3))
        log.debug ('step4: {}'.format(step4))
        log.debug ('step5: {}'.format(step5))
        log.debug ('step6: {}'.format(step6))
        return answer

    def crc8 (self, byteData):
        '''
        Generate 8 bit CRC of supplied string
        '''
        CRC = 0
        #for j in range(0, len(str),2):
        for b in byteData:
            #char = int(str[j:j+2], 16)
            #print (b)
            CRC = CRC + b
            CRC &= 0xff
        return CRC

    def handleNotification(self, handle, data):
        # handle is the handle of the characteristic / descriptor that posted the notification
        # data is the data in this notification - may take multiple notifications to get all of a message
        log.debug ('From handle: {:#04x} Got {} bytes of data'.format(handle, len(data)))
        self.notificationData += bytearray(data)
        if self.recordIsComplete():
            record = self.notificationData
            self.notificationData = bytearray()
            self.processRecord(record)

        #len(self.notificationData)
        #for x in range(len(data)):
        #    sys.stdout.write ('{:02x}'.format(ord(data[x])))
        #print('    {}'.format(data))
        #print('')

def main():
    '''
    Main section
    '''

    configFile = './jkbms.conf'
    # Queries / info written to BMS to prompt responses
    getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
    getCellInfo = b'\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
    # Get config from config file
    print ('Reading config file: {}'.format(configFile))
    config.read(configFile)
    if not config:
        print ('Config not found or nothing parsed correctly')
        sys.exit(1)
    sections = config.sections()

    if 'SETUP' in config:
        pause = config['SETUP'].getint('pause', fallback=60)
        mqtt_broker = config['SETUP'].get('mqtt_broker', fallback='localhost')
        logging_level = config['SETUP'].getint('logging_level', fallback=logging.CRITICAL)
        max_connection_attempts = config['SETUP'].getint('max_connection_attempts', fallback=3)
        log.setLevel(logging_level)
        sections.remove('SETUP')

    # Process each section
    # This might need threading?
    # or notitfy to handle different devices?
    for section in sections:
        # print('MPP-Solar-Service: Execute - {}'.format(config[section]))
        name = section
        model = config[section].get('model')
        mac = config[section].get('mac')
        command = config[section].get('command')
        tag = config[section].get('tag')
        format = config[section].get('format')
        log.debug('Config data - name: {}, model: {}, mac: {}, command: {}, tag: {}, format: {}'.format(name, model, mac, command, tag, format))
        # Intialise BLE device
        device = btle.Peripheral(None)
        device.withDelegate( jkBmsDelegate(device) )
        # Connect to BLE Device
        connected = False
        attempts = 0
        log.info('Attempting to connect to {}'.format(name))
        while not connected:
            attempts += 1
            if attempts > max_connection_attempts:
                log.warning ('Cannot connect to {} with mac {} - exceeded {} attempts'.format(name, mac, attempts - 1))
                sys.exit(1)
            try:
                device.connect(mac)
                connected = True
            except Exception as e:
                continue
        # Get the device name
        serviceId = device.getServiceByUUID(btle.AssignedNumbers.genericAccess)
        deviceName = serviceId.getCharacteristics(btle.AssignedNumbers.deviceName)[0]
        log.info('Connected to {}'.format(deviceName.read()))

        # Connect to the notify service
        serviceNotifyUuid = 'ffe0'
        serviceNotify = device.getServiceByUUID(serviceNotifyUuid)

        # Get the handles that we need to talk to
        ### Read
        characteristicReadUuid = 'ffe3'
        characteristicRead = serviceNotify.getCharacteristics(characteristicReadUuid)[0]
        handleRead = characteristicRead.getHandle()
        log.info ('Read characteristic: {}, handle {:x}'.format(characteristicRead, handleRead))

        ### TODO sort below
        # Need to dynamically find this handle....
        log.info ('Enable 0x0b handle', device.writeCharacteristic(0x0b, b'\x01\x00'))
        log.info ('Enable read handle', device.writeCharacteristic(handleRead, b'\x01\x00'))
        log.info ('Write getInfo to read handle', device.writeCharacteristic(handleRead, getInfo))
        secs = 0
        while True:
            if device.waitForNotifications(1.0):
                continue
            secs += 1
            if secs > 5 :
                break

        log.info ('Write getCellInfo to read handle', device.writeCharacteristic(handleRead, getCellInfo))
        loops = 0
        recordsToGrab = 1
        log.info ('Grabbing {} records (after inital response)'.format(recordsToGrab))

        while True:
            loops += 1
            if loops > recordsToGrab * 15 + 16:
                break
            if device.waitForNotifications(1.0):
                continue

        log.info ('Disconnecting...')
        device.disconnect()

if __name__ == "__main__":
    # execute only if run as a script and python3
    if sys.version_info < (3,0):
        print ('Python3 required')
        sys.exit(1)
    main()

#print ('Hit <ENTER> to disconnect')
#if (sys.version_info > (3, 0)):
#    input()
#else:
#    raw_input()
