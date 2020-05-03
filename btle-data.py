#!/usr/bin/python
from builtins import bytes
from bluepy import btle
import sys
import struct
import logging
log = logging.getLogger('JKBMS-BT')
# setup logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# set default log levels
log.setLevel(logging.INFO)
logging.basicConfig()

class MyDelegate(btle.DefaultDelegate):
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        #print ('From handle: {:#04x} Got {} bytes of data'.format(cHandle, len(data)))
        for x in range(len(data)):
            sys.stdout.write ('{:02x}'.format(ord(data[x])))
        #print('    {}'.format(data))
        print('')

# Devices
pw1DeviceMac = '3c:a5:09:0a:85:79'  # Power Wall 1
pw2DeviceMac = '3c:a5:09:0a:26:a6'  # Power Wall 2
pw3DeviceMac = '3c:a5:09:0a:26:d8'  # Power Wall 3
deviceMac = pw2DeviceMac
maxConnectionAttempts = 3
secsToWait = 20
device = btle.Peripheral(None)
device.setDelegate( MyDelegate(device) )

# UUIDs
# serviceNameUuid = '00001800-0000-1000-8000-00805f9b34fb' # btle.AssignedNumbers.genericAccess
# characteristicNameUuid = '00002a00-0000-1000-8000-00805f9b34fb' # btle.AssignedNumbers.deviceName

serviceNotifyUuid = '0000ffe0-0000-1000-8000-00805f9b34fb'
characteristicReadUuid = '0000ffe3-0000-1000-8000-00805f9b34fb'
characteristicWriteUuid = '0000ffe2-0000-1000-8000-00805f9b34fb'
characteristicNotifyUuid = '0000ffe1-0000-1000-8000-00805f9b34fb'

rawLEAdvertisingReport = bytes.fromhex('0502e0ffe7fe0bffb60588a03ca5090a26a6')
revLEAdvertisingReport = rawLEAdvertisingReport[::-1]

# Stuff Samsung Tablet sent

getInfo = '\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
#aa5590eb96000000000000000000000000000010
getCellInfo = '\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
#aa5590eb440474cd3a400000000000000000007d
# get???? = '\xaa\x55\x90\xeb\x44\x04\x74\xcd\x3a\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7d'
#aa5590eb44040f133f4000000000000000000063
#'\xaa\x55\x90\xeb\x44\x04\x0f\x13\x3f\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x63'
#aa5590eb440459cc3a4000000000000000000061
#'\xaa\x55\x90\xeb\x44\x04\x59\xcc\x3a\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x61'



# Connect to BLE Device
connected = False
attempts = 0
while not connected:
    attempts += 1
    if attempts > maxConnectionAttempts:
        log.warning ('Cannot connect to {} - exceeded {} attempts'.format(deviceMac, attempts))
        sys.exit(1)
    try:
        device.connect(deviceMac)
        connected = True
    except Exception as e:
        continue

# Get the Name Service
deviceIDService = device.getServiceByUUID(btle.AssignedNumbers.genericAccess)
deviceName = deviceIDService.getCharacteristics(btle.AssignedNumbers.deviceName)[0]
log.info('Connected to {}'.format(deviceName.read()))

deviceNotifyServer = device.getServiceByUUID(serviceNotifyUuid)
characteristicRead = deviceNotifyServer.getCharacteristics(characteristicReadUuid)[0]
characteristicWrite = deviceNotifyServer.getCharacteristics(characteristicWriteUuid)[0]
characteristicNotify = deviceNotifyServer.getCharacteristics(characteristicNotifyUuid)[0]
handleRead = characteristicRead.getHandle()
handleWrite = characteristicWrite.getHandle()
handleNotify = characteristicNotify.getHandle()
log.info ('Read characteristic: {}, handle {:x}'.format(characteristicRead, handleRead))
log.info ('Write characteristic: {}, handle {:x}'.format(characteristicWrite, handleWrite))
log.info ('Notify characteristic: {}, handle {:x}'.format(characteristicNotify, handleNotify))


log.info ('Enable 0x0b handle', device.writeCharacteristic(0x0b, '\x01\x00'))
log.info ('Enable 0x0e handle', device.writeCharacteristic(0x0e, '\x01\x00'))
log.info ('Enable read handle', device.writeCharacteristic(handleRead, '\x01\x00'))
log.info ('Write getInfo to read handle', device.writeCharacteristic(handleRead, getInfo))
secs = 0
while True:
    if device.waitForNotifications(1.0):
        continue
    secs += 1
    if secs > secsToWait:
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
