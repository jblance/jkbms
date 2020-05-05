from pybleno import *
from pybleno.hci_socket import Emit
import array
import struct
import sys
import traceback
from builtins import bytes

ATT_OP_HANDLE_NOTIFY = 0x1b

def crc8 ():
  str = '55aaeb9002ff5b566140e34e62406e6a62404a506240acd7624011d26240bddd62409ad1624044c86240cedc6240ccc7624079e1624057dc624073a262405f80624088c46240000000000000000000000000000000000000000000000000000000000000000013315c3d0636143d26e0113d8021f03c1153363d8980123d7e7c033dac41233d1ad83c3d9d6f4f3d8eb51e3d6a2c293deb28653d189c523da3724e3deb94493d9ab2c23d00000000000000000000000000000000000000000000000000000000000000001aad62400084053c00000000ffff00000b000000000000000000000000000036a3554c40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000be0b54001456a43fb876a43f00'
  CRC = 0
  for j in range(0, len(str),2):
    char = int(str[j:j+2], 16)
    CRC = CRC + char
    CRC &= 0xff
  return CRC

getInfo = '\xaa\x55\x90\xeb\x97\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x11'
getInfoData = array.array('B', bytes.fromhex('55aaeb9003b44a4b2d42314132345300000000000000332e300000000000332e312e32000000b0b878000f000000506f7765722057616c6c203200000000313233340000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000abaa5590ebc8010100000000000000000000000044'))
getCellInfo = '\xaa\x55\x90\xeb\x96\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10'
getCellInfoDataInitial = array.array('B', bytes.fromhex('55aaeb9001f30000803f000000000000000000000000000000000000000000000000100000009a993940000000000000000000000000000000000000000000000000000000000000000011bc3a40000000000000000000000000000000000000000000000000000000000ad7233c9a99993e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007aaa5590ebc8010100000000000000000000000044'))
#getCellInfoDataRepeat = array.array('B', bytes.fromhex('55aaeb9002f3ec426140f3466240011c6240593a62403f976240bbc16240cbb96240edb762404c6c62401fa762400fb662400da16240739b6240b47b62408c3e6240d7876240000000000000000000000000000000000000000000000000000000000000000013315c3d0636143d26e0113d8021f03c1153363d8980123d7e7c033dac41233d1ad83c3d9d6f4f3d8eb51e3d6a2c293deb28653d189c523da3724e3deb94493d9ab2c23d0000000000000000000000000000000000000000000000000000000000000000947162408067bf3c00000000ffff000005000000000000000000000000000086324e4c4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009435500cde4a33fae77a43f0095'))
# getCellInfoDataRepeat = array.array('B', bytes.fromhex('55aaeb9002f3')
#     + bytes.fromhex('ec426140')
#     + bytes.fromhex('f3466240')
#     + bytes.fromhex('011c6240')
#     + bytes.fromhex('593a6240')
#     + bytes.fromhex('3f976240')
#     + bytes.fromhex('bbc16240')
#     + bytes.fromhex('cbb96240')
#     + bytes.fromhex('edb76240')
#     + bytes.fromhex('4c6c6240')
#     + bytes.fromhex('1fa76240')
#     + bytes.fromhex('0fb66240')
#     + bytes.fromhex('0da16240')
#     + bytes.fromhex('739b6240')
#     + bytes.fromhex('b47b6240')
#     + bytes.fromhex('8c3e6240')
#     + bytes.fromhex('d7876240')
#     + bytes.fromhex('00000000' * 8)
#     + bytes.fromhex('13315c3d')
#     + bytes.fromhex('0636143d')
#     + bytes.fromhex('26e0113d')
#     + bytes.fromhex('8021f03c')
#     + bytes.fromhex('1153363d')
#     + bytes.fromhex('8980123d')
#     + bytes.fromhex('7e7c033d')
#     + bytes.fromhex('ac41233d')
#     + bytes.fromhex('1ad83c3d')
#     + bytes.fromhex('9d6f4f3d')
#     + bytes.fromhex('8eb51e3d')
#     + bytes.fromhex('6a2c293d')
#     + bytes.fromhex('eb28653d')
#     + bytes.fromhex('189c523d')
#     + bytes.fromhex('a3724e3d')
#     + bytes.fromhex('eb94493d')
#     + bytes.fromhex('9ab2c23d')
#     + bytes.fromhex('00000000' * 8)
#     + bytes.fromhex('947162408067bf3c00000000ffff000005000000000000000000000000000086324e4c4000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000009435500cde4a33fae77a43f0095')
#     )

with open('testinput.txt') as f:
    data = f.read()
    data = data.replace('\n', '')
    crc = crc8(data)
    getCellInfoDataRepeat = array.array('B', bytes.fromhex(data) + hex(crc))


def getChunks(_data, _size):
    chunks = []
    for i in range(0, len(_data), _size):
        chunks.append(_data[0+i:_size+i])
    return chunks

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
        if data == getInfo:
            print ('Got getInfo request')
            chunks = getChunks(getInfoData, self._maxValueSize)
            #print chunks
            for chunk in chunks:
                #print chunk, len(chunk)
                self._value = chunk
                #self.emit(ATT_OP_HANDLE_NOTIFY, self._value)
                if self._updateValueCallback:
                    print('jbBMSCharacteristic - onWriteRequest, getInfo chunk sent' )
                    self._updateValueCallback(self._value)
        if data == getCellInfo:
            print ('Got getCellInfo request')
            # send initial response to getCellInfo request
            chunks = getChunks(getCellInfoDataInitial, self._maxValueSize)
            for chunk in chunks:
                #print chunk
                self._value = chunk
                #self.emit(ATT_OP_HANDLE_NOTIFY, self._value)
                if self._updateValueCallback:
                    print('jbBMSCharacteristic - onWriteRequest, getCellInfoDataInitial chunk sent' )
                    self._updateValueCallback(self._value)
            # send 'repeating' response to getCellInfo request
            chunks = getChunks(getCellInfoDataRepeat, self._maxValueSize)
            for chunk in chunks:
                #print chunk
                self._value = chunk
                #self.emit(ATT_OP_HANDLE_NOTIFY, self._value)
                if self._updateValueCallback:
                    print('jbBMSCharacteristic - onWriteRequest, getCellInfoDataRepeat chunk sent' )
                    self._updateValueCallback(self._value)
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
