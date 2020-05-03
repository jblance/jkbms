from pybleno import *
from pybleno.hci_socket import Emit
import array
import struct
import sys
import traceback
from builtins import bytes

ATT_OP_HANDLE_NOTIFY = 0x1b

class jbBMSReadCharacteristic(Characteristic):

    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
        })
        print ('jbBMSReadCharacteristic __init__', uuid)
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        print('jbBMSReadCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data

        print('jbBMSCharjbBMSReadCharacteristicacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        # data written - check what it was and handle? and respond...
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))

        if self._updateValueCallback:
            print('jbBMSReadCharacteristic - onWriteRequest: notifying')
            self._updateValueCallback(self._value)

        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('jbBMSReadCharacteristic - onSubscribe')

        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('jbBMSReadCharacteristic - onUnsubscribe')

        self._updateValueCallback = None

    def onNotify(self):
        print('jbBMSReadCharacteristic - onNotify')
        for c in self._value:
            print(hex(c))
        #try with callback
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))
        #self._updateValueCallback(bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000'))
