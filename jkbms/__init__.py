# !/usr/bin/python3
import logging
from argparse import ArgumentParser

from .version import __version__  # noqa: F401
from .jkbmsdecode import *
# import mppcommands
# from .mpputils import mppUtils

log = logging.getLogger('JKBMS-BT')
# setup logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# ch = logging.StreamHandler()
# create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# add the handlers to logger
# log.addHandler(ch)
# set default log levels
log.setLevel(logging.WARNING)
# ch.setLevel(logging.WARNING)
logging.basicConfig()


def main():
    parser = ArgumentParser(description='JKBMS Utility, version: {}'.format(__version__))
    parser.add_argument('-c', '--configFile', help='Config file', default='/etc/jkbms/jkbms.conf')
    parser.add_argument('-l', '--loops', help='Number of loops to query the BMS', default='1')
    parser.add_argument('-x', '--decodeHex', help='Hex to decode (will not communication to BMS)')
    parser.add_argument('-D', '--enableDebug', action='store_true', help='Enable Debug and above (i.e. all) messages')
    parser.add_argument('-I', '--enableInfo', action='store_true', help='Enable Info and above level messages')
    args = parser.parse_args()

    # Turn on debug if needed
    if(args.enableDebug):
        log.setLevel(logging.DEBUG)
        # ch.setLevel(logging.DEBUG)
    elif(args.enableInfo):
        log.setLevel(logging.INFO)
        # ch.setLevel(logging.INFO)

    if args.decodeHex:
        print ('Decode Hex {}'.format(args.decodeHex))
        print ('Hex: {} decoded to {}'.format(args.decodeHex, jkbmsdecode.decodeHex(args.decodeHex)))
    else:
        print ('Query BMS via BLE')
        log.info('Querying {} times'.format(args.loops))
    # mp = mppcommands.mppCommands(args.device, args.baud)
    # mp = mppUtils(args.device, args.baud, args.model)
