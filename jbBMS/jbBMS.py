from pybleno import Bleno
from pybleno import BlenoPrimaryService
import sys
from jbBMSCharacteristic import jbBMSCharacteristic

# origLEAdvertisingR  = 'a6260a09a53ca08805b6ff0b-fee7ffe00205'  # noqa: E221
# LEAdvertisingReport = '0a09a53c-a088-05b6-ff0b-fee7ffe00205'
# manuSpecific        = 'a6260a09a53ca08805b6ff0b'  # noqa: E221
# 2manu               = '0bff737b88a03ca519db5861'
# JK-BD6A20S10P
serviceClassUuids   = ['ffe0', 'fee7', 'ff0b', '7b73', 'a088', 'a53c', 'db19', '6158']  # noqa: E221
# JK-B2A24S JK-B1A24S
# serviceClassUuids   = ['ffe0', 'fee7', 'ff0b', '05b6', 'a088', 'a53c', '0a09', 'a626']  # noqa: E221
primaryUuid         = '0000ffe0-0000-1000-8000-00805f9b34fb'  # noqa: E221
notifyUuid          = '0000ffe1-0000-1000-8000-00805f9b34fb'  # noqa: E221
writeUuid           = '0000ffe2-0000-1000-8000-00805f9b34fb'  # noqa: E221
readUuid            = '0000ffe3-0000-1000-8000-00805f9b34fb'  # noqa: E221
pw2Mac = '3c:a5:09:0a:26:a6'

name = 'jbBMS-v3'
print('bleno - Echo with name: {}'.format(name))

bleno = Bleno()


def onStateChange(state):
    print('on -> stateChange: ' + state)

    if (state == 'poweredOn'):
        # bleno.startAdvertising(name, [serviceClass, manuSpecific])
        bleno.startAdvertising(name, serviceClassUuids)
    else:
        bleno.stopAdvertising()


bleno.on('stateChange', onStateChange)


def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'))

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': primaryUuid,
                'characteristics': [
                    jbBMSCharacteristic(notifyUuid),
                    jbBMSCharacteristic(writeUuid),
                    jbBMSCharacteristic(readUuid)
                ]
            })
        ])


bleno.on('advertisingStart', onAdvertisingStart)
bleno.start()


print('Hit <ENTER> to disconnect')
if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()  # noqa

bleno.stopAdvertising()
bleno.disconnect()

print('terminated.')
