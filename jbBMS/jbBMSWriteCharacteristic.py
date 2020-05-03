from pybleno import *
from pybleno.hci_socket import Emit
import array
import struct
import sys
import traceback
from builtins import bytes

ATT_OP_HANDLE_NOTIFY = 0x1b

class jbBMSWriteCharacteristic(Characteristic):

    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write'],
            'value': None,
            'descriptors' : [
                Descriptor({
                    'uuid': '000a',
                    'value': 'Write char descriptor'
                }),
                Descriptor({
                    'uuid': '000b',
                    'value': array.array('B', [0x04, 0x01, 0x27, 0xAD, 0x01, 0x00, 0x00 ])
                }),
                Descriptor({
                    'uuid': '000c',
                    'value': array.array('B', [0x04, 0x01, 0x27, 0xAD, 0x01, 0x00, 0x00 ])
                })
            ]
        })
        print ('jbBMSWriteCharacteristic __init__', uuid)
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        print('jbBMSWriteCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data

        print('jbBMSWriteCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        # data written - check what it was and handle? and respond...
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))

        if self._updateValueCallback:
            print('jbBMSWriteCharacteristic - onWriteRequest: notifying');
            self._updateValueCallback(self._value)

        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('jbBMSWriteCharacteristic - onSubscribe')

        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('jbBMSWriteCharacteristic - onUnsubscribe');

        self._updateValueCallback = None

    def onNotify(self):
        print('jbBMSWriteCharacteristic - onNotify');
        for c in self._value:
            print(hex(c))
        #try with callback
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))
        #self._updateValueCallback(bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000'))
