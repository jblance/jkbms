from pybleno import *
import sys
import signal
import math, random
#from jbBMSNotifyCharacteristic import *
#from jbBMSReadCharacteristic import *
#from jbBMSWriteCharacteristic import *
from jbBMSCharacteristic import *
#from jbCharacteristic import *


origLEAdvertisingR  = 'a6260a09a53ca08805b6ff0b-fee7ffe00205'
LEAdvertisingReport = '0a09a53c-a088-05b6-ff0b-fee7ffe00205'
manuSpecific        = 'a6260a09a53ca08805b6ff0b'
#serviceClassUuids   = ['ffe0','fee7']
serviceClassUuids   = ['ffe0','fee7', 'ff0b', '05b6', 'a088', 'a53c', '0a09', 'a626']
primaryUuid         = '0000ffe0-0000-1000-8000-00805f9b34fb'
notifyUuid          = '0000ffe1-0000-1000-8000-00805f9b34fb'
writeUuid           = '0000ffe2-0000-1000-8000-00805f9b34fb'
readUuid            = '0000ffe3-0000-1000-8000-00805f9b34fb'
pw2Mac = '3c:a5:09:0a:26:a6'

name = 'jbBMS-{}'.format(math.trunc(random.random()*100))
print('bleno - Echo with name: {}'.format(name))

bleno = Bleno()

def onStateChange(state):
   print('on -> stateChange: ' + state)

   if (state == 'poweredOn'):
     #bleno.startAdvertising(name, [serviceClass, manuSpecific])
     bleno.startAdvertising(name, serviceClassUuids)
   else:
     bleno.stopAdvertising()

bleno.on('stateChange', onStateChange)

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': primaryUuid,
                'characteristics': [
                    jbBMSCharacteristic(notifyUuid)
                    ]
            })
        ])


bleno.on('advertisingStart', onAdvertisingStart)
bleno.start()


print ('Hit <ENTER> to disconnect')
if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()

bleno.stopAdvertising()
bleno.disconnect()

print ('terminated.')
