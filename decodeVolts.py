#!/usr/bin/env python3
from argparse import ArgumentParser
import sys

def decodeVolts(hexString):
    return 3

def main():
    parser = ArgumentParser(description='BM Voltage Decode Utility')
    parser.add_argument('--hexVolts', help='Hex encoded voltage measurement', default='00006240')
    args = parser.parse_args()

    if len(args.hexVolts) != 8:
        print('Hex encoded value must be 4 bytes long')
        sys.exit(1)

    print(decodeVolts(args.hexVolts))
