#!/usr/bin/env python3
import sys
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
        del record[0:4]
        counter = record.pop()
        print(counter)
        vendorID = bytearray()
        hardwareVersion = bytearray()
        softwareVersion = bytearray()
        uptimeReverse = bytearray()
        powerUpTimes = bytearray()
        deviceName = bytearray()
        passcode = bytearray()
        # start at byte 7, go till 0x00 for device model
        while len(record) > 0 :
            byte = (record.pop())
            if byte == 0x00:
                break
            else:
                vendorID += byte
        print (vendorID)

        sys.exit()

    def processRecord(self, record):
        recordType = record[4]
        counter = record[5]
        if recordType == INFO_RECORD:
            self.processInfoRecord(record)
        elif recordType == EXTENDED_RECORD:
            print('Extended record')
            pass
        elif recordType == CELL_DATA:
            print('Cell data record')
            pass

    def decodeVolts(hexString):
        '''
        # For bluetooth battery monitor (model JK-B1A24S)
        # - which encodes cell voltages into 4 bytes (hex encoded)
        # - example 5f806240 -> 3.539
        '''
        volts = 0.0

        # Make sure supplied String is long enough
        if len(hexString) != 8:
            log.warning('Hex encoded value must be 4 bytes long')
            return None

        # Process most significant byte (position 6,7)
        # valid values are 0x40 - 0x4f (normally 0x40 for LiPo cells
        if hexString[6] != '4':
            log.warning('Hex out of bounds - position 6 != 4: ', hexString[6])
        # interprete as int & get bottom 4 bits
        byte1 = int(hexString[6:8], 16)
        byte1Low = byte1 & 0xf
        volts = (2**(byte1Low*2))*2
        step1 = volts / 8.0
        step2 = volts / 128.0
        step3 = volts / 2048.0
        step4 = volts / 32768.0
        step5 = volts / 524288.0
        step6 = volts / 8388608.0

        # position 4,5
        byte2 = int(hexString[4:6], 16)
        byte2High = byte2 >> 4
        byte2Low = byte2 & 0xf
        if byte2High & 8:
            volts += (byte2High * step1 * 2) + (byte2Low * step2)
        else:
            volts += (byte2High * step1) + (byte2Low * step2)

        # position 2,3
        byte3 = int(hexString[2:4], 16)
        byte3High = byte3 >> 4
        byte3Low = byte3 & 0xf
        volts += (byte3High * step3) + (byte3Low * step4)

        # position 0,1
        byte4 = int(hexString[0:2], 16)
        byte4High = byte4 >> 4
        byte4Low = byte4 & 0xf
        volts += (byte4High * step5) + (byte4Low * step6)

        log.debug ('hexString', hexString)
        log.debug ('hex(byte1)', hex(byte1))
        log.debug ('byte1Low', byte1Low)
        #log.debug ('byte2', byte2)
        log.debug ('hex(byte2)', hex(byte2))
        log.debug ('byte2High', byte2High)
        log.debug ('byte2Low', byte2Low)
        #log.debug ('byte3', byte3)
        log.debug ('hex(byte3)', hex(byte3))
        log.debug ('byte3High', byte3High)
        log.debug ('byte3Low', byte3Low)
        #log.debug ('byte4', byte4)
        log.debug ('hex(byte4)', hex(byte4))
        log.debug ('byte4High', byte4High)
        log.debug ('byte4Low', byte4Low)

        log.debug ('step1', step1)
        log.debug ('step2', step2)
        log.debug ('step3', step3)
        log.debug ('step4', step4)
        log.debug ('step5', step5)
        log.debug ('step6', step6)
        return volts

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
    # Queries / info written to BMS to prompt responses
    getInfo = b'\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
    getCellInfo = b'\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
    # Get config from config file
    config.read('./jkbms.conf')
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
            if secs > 20:
                break

        log.info ('Write getCellInfo to read handle', device.writeCharacteristic(handleRead, getCellInfo))
        loops = 0
        recordsToGrab = 20
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
