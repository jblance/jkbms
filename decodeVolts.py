#!/usr/bin/env python3
from argparse import ArgumentParser

def decodeVolts(hexString):
    '''
    # For bluetooth battery monitor (model XXXX) w
    # - which encodes cell voltages into 4 bytes (hex encoded)
    # - example 5f806240 -> 3.539
    '''
    volts = 0.0

    # Make sure supplied String is long enough
    if len(hexString) != 8:
        print('Hex encoded value must be 4 bytes long')
        return None

    # Process most significant byte (position 6,7)
    # valid values are 0x40 - 0x4f (normally 0x40 for LiPo cells
    if hexString[6] != '4':
        print('Hex out of bounds - position 6 != 4: ', hexString[6])
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


    print ('hexString', hexString)
    print ('hex(byte1)', hex(byte1))
    print ('byte1Low', byte1Low)
    #print ('byte2', byte2)
    print ('hex(byte2)', hex(byte2))
    print ('byte2High', byte2High)
    print ('byte2Low', byte2Low)
    #print ('byte3', byte3)
    print ('hex(byte3)', hex(byte3))
    print ('byte3High', byte3High)
    print ('byte3Low', byte3Low)
    #print ('byte4', byte4)
    print ('hex(byte4)', hex(byte4))
    print ('byte4High', byte4High)
    print ('byte4Low', byte4Low)
    
    print ('step1', step1)
    print ('step2', step2)
    print ('step3', step3)
    print ('step4', step4)
    print ('step5', step5)
    print ('step6', step6)
    return volts


parser = ArgumentParser(description='BM Voltage Decode Utility')
parser.add_argument('-x', '--hexVolts', help='Hex encoded voltage measurement', default='5f806240')
args = parser.parse_args()

print(decodeVolts(args.hexVolts))
