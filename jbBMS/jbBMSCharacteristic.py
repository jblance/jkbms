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
                })
            ]
        })
        print ('jbBMSCharacteristic __init__', uuid)
        self._uuid = uuid
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
        self._maxValueSize = 20

    def onReadRequest(self, offset, callback):
        print('jbBMSCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        print ('onWriteRequest')
        if hex(data[0]) == '0xaa' and hex(data[1]) == '0x55':
            print ('got data meeting info request pattern')
            #print data, offset, withoutResponse, callback
            print self._uuid
            print self._updateValueCallback
            #self._value = array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000'))
            infoData = array.array('B', bytes.fromhex('55aaeb9003b44a4b2d42314132345300000000000000332e300000000000332e312e32000000b0b878000f000000506f7765722057616c6c203200000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000abaa5590ebc8010100000000000000000000000044'))
            # chunk to max size
            chunks = []
            #result.append('{:^{width}}'.format(name[0:length], width=length))
            for i in range(0, len(infoData), self._maxValueSize):
                chunks.append(infoData[0+i:self._maxValueSize+i])
            for chunk in chunks:
                print chunk
                self._value = chunk
                #self.emit(ATT_OP_HANDLE_NOTIFY, self._value)
                if self._updateValueCallback:
                    print('jbBMSCharacteristic - onWriteRequest, chunk sent' )
                    #self.updateValueCallback(self._value)
        else:
            self._value = data
            #print('jbBMSCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
            print('jbBMSCharacteristic - onWriteRequest' )
        # data written - check what it was and handle? and respond...
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))

        if self._updateValueCallback:
            print('jbBMSCharacteristic - onWriteRequest: notifying')
            self._updateValueCallback(self._value)

        callback(Characteristic.RESULT_SUCCESS)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('jbBMSCharacteristic - onSubscribe')
        #print (self._uuid)
        self.maxValueSize = maxValueSize
        #print ('Set maxValueSize', maxValueSize)
        self._updateValueCallback = updateValueCallback
        #print ('Set updateValueCallback', updateValueCallback)

    #def onSubscribe(self, maxValueSize, updateValueCallback):
    #    print('jbBMSCharacteristic - onSubscribe')
    #    self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('jbBMSCharacteristic - onUnsubscribe')
        self._updateValueCallback = None

    def onNotify(self):
        print('jbBMSCharacteristic - onNotify')
        print('self._value len: ', len(self._value))
        #    print(hex(c))
        #try with callback
        #self.emit(ATT_OP_HANDLE_NOTIFY, array.array('B', bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000')))
        #self._updateValueCallback(bytes.fromhex('55aaeb9003b44a4b2d4231413234530000000000'))
