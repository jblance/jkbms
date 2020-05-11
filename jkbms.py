#!/usr/bin/env python3
import sys
from bluepy import btle

import logging
log = logging.getLogger('JKBMS-BT')
# setup logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# set default log levels
log.setLevel(logging.INFO)
logging.basicConfig()

import configparser
config = configparser.ConfigParser()

# notificationData = ''

class jkBmsDelegate(btle.DefaultDelegate):
    '''
    BLE delegate to deal with notifications (information) from the JKBMS device
    '''
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        # extra initialisation here

    def handleNotification(self, handle, data):
        # handle is the handle of the characteristic / descriptor that posted the notification
        # data is the data in this notification - may take multiple notifications to get all of a message
        #print ('From handle: {:#04x} Got {} bytes of data'.format(handle, len(data)))
        for x in range(len(data)):
            sys.stdout.write ('{:02x}'.format(ord(data[x])))
        #print('    {}'.format(data))
        print('')


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

def crc8 (str):
    '''
    Generate 8 bit CRC of supplied string
    '''
    CRC = 0
    for j in range(0, len(str),2):
        char = int(str[j:j+2], 16)
        CRC = CRC + char
        CRC &= 0xff
    return CRC


def main():
    '''
    '''
    # Get config from config file
    config.read('./jkbms.conf')
    sections = config.sections()

    if 'SETUP' in config:
        pause = config['SETUP'].getint('pause', fallback=60)
        mqtt_broker = config['SETUP'].get('mqtt_broker', fallback='localhost')
        sections.remove('SETUP')
    for section in sections:
        # print('MPP-Solar-Service: Execute - {}'.format(config[section]))
        name = section
        model = config[section].get('model')
        mac = config[section].get('mac')
        command = config[section].get('command')
        tag = config[section].get('tag')
        format = config[section].get('format')
        print('Config data', name, model, mac, command, tag, format)


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
