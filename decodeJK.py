#!/usr/bin/env python3
import sys
import math
import logging
log = logging.getLogger('JKBMS-BT')
# setup logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# set default log levels
log.setLevel(logging.CRITICAL)
logging.basicConfig()

import configparser
config = configparser.ConfigParser()

from argparse import ArgumentParser
parser = ArgumentParser(description='JK Hex Decode Utility')
parser.add_argument('-x', '--hex', help='Hex to decode', default='8acdbd3d')
parser.add_argument('-D', '--enableDebug', action='store_true', help='Enable Debug and above (i.e. all) messages')
arser.add_argument('-I', '--enableInfo', action='store_true', help='Enable Info and above level messages')
args = parser.parse_args()

# Turn on debug if needed
if(args.enableDebug):
    log.setLevel(logging.DEBUG)
    # ch.setLevel(logging.DEBUG)
elif(args.enableInfo):
    log.setLevel(logging.INFO)
    # ch.setLevel(logging.INFO)

hexString = args.hex

answer = 0.0

# Make sure supplied String is long enough
if len(hexString) != 4:
    log.warning('Hex encoded value must be 4 bytes long. Was {} length'.format(len(hexString)))
    sys.exit(1)

# Process most significant byte (position 3)
byte1 = hexString[3]
if byte1 == 0x0:
    sys.exit(0)
byte1Low = byte1 - 0x40
answer = (2**(byte1Low*2))*2
step1 = answer / 8.0
step2 = answer / 128.0
step3 = answer / 2048.0
step4 = answer / 32768.0
step5 = answer / 524288.0
step6 = answer / 8388608.0

# position 2
byte2 = hexString[2]
byte2High = byte2 >> 4
byte2Low = byte2 & 0xf
if byte2High & 8:
    answer += (byte2High * step1 * 2) + (byte2Low * step2)
else:
    answer += (byte2High * step1) + (byte2Low * step2)

# position 1
byte3 = hexString[1]
byte3High = byte3 >> 4
byte3Low = byte3 & 0xf
answer += (byte3High * step3) + (byte3Low * step4)

# position 0
byte4 = hexString[0]
byte4High = byte4 >> 4
byte4Low = byte4 & 0xf
answer += (byte4High * step5) + (byte4Low * step6)

log.debug ('hexString: {}'.format(hexString))
log.debug ('hex(byte1): {}'.format(hex(byte1)))
log.debug ('byte1Low: {}'.format(byte1Low))
#log.debug ('byte2', byte2)
log.debug ('hex(byte2): {}'.format(hex(byte2)))
log.debug ('byte2High: {}'.format(byte2High))
log.debug ('byte2Low: {}'.format(byte2Low))
#log.debug ('byte3', byte3)
log.debug ('hex(byte3): {}'.format(hex(byte3)))
log.debug ('byte3High: {}'.format(byte3High))
log.debug ('byte3Low: {}'.format(byte3Low))
#log.debug ('byte4', byte4)
log.debug ('hex(byte4): {}'.format(hex(byte4)))
log.debug ('byte4High: {}'.format(byte4High))
log.debug ('byte4Low: {}'.format(byte4Low))

log.debug ('step1: {}'.format(step1))
log.debug ('step2: {}'.format(step2))
log.debug ('step3: {}'.format(step3))
log.debug ('step4: {}'.format(step4))
log.debug ('step5: {}'.format(step5))
log.debug ('step6: {}'.format(step6))

print('Hex {} decoded to {}'.format(hexString, answer))
