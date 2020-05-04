from pybleno import *
from pybleno.hci_socket import Emit
import array
import struct
import sys
import traceback
from builtins import bytes

ATT_OP_HANDLE_NOTIFY = 0x1b

class jbBMSCharacteristic(Characteristic):

    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None,
            'descriptors' : [
                Descriptor({
                    'uuid': '2901',
                    'value': 'Descriptor'
                }),
                Descriptor({
                    'uuid': '2902',
                    'value': 'String 2902'
                }),
                Descriptor({
                    'uuid': '000c',
                    'value': array.array('B', [0x04, 0x01, 0x27, 0xAD, 0x01, 0x00, 0x00 ])
                })
            ]
        })
        print ('jbBMSCharacteristic __init__', uuid)
        self._uuid = uuid
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        print('jbBMSCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if hex(data[0]) == '0xaa' and hex(data[1]) == '0x55':
            print ('got data meeting info request pattern')
            #print data, offset, withoutResponse, callback
            print self._uuid
            print self._updateValueCallback
            #self._value = array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000'))
            self._value = array.array('B', bytes.fromhex('55aaeb9003b44a4b2d42314132345300000000000000332e300000000000332e312e32000000b0b878000f000000506f7765722057616c6c203200000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000abaa5590ebc8010100000000000000000000000044'))
            self.emit(ATT_OP_HANDLE_NOTIFY, self._value)
        else:
            self._value = data
            #print('jbBMSCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
            print('jbBMSCharacteristic - %s - onWriteRequest' )
        # data written - check what it was and handle? and respond...
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))

        if self._updateValueCallback:
            print('jbBMSCharacteristic - onWriteRequest: notifying')
            self._updateValueCallback(self._value)

        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('jbBMSCharacteristic - onSubscribe', self._uuid, updateValueCallback)
        self.maxValueSize = maxValueSize
        self._updateValueCallback = updateValueCallback

    #def onSubscribe(self, maxValueSize, updateValueCallback):
    #    print('jbBMSCharacteristic - onSubscribe')
    #    self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('jbBMSCharacteristic - onUnsubscribe')
        self._updateValueCallback = None

    def onNotify(self):
        print('jbBMSCharacteristic - onNotify')
        for c in self._value:
            print(hex(c))
        #try with callback
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))
        #self._updateValueCallback(bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000'))
