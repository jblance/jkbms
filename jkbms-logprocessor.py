#!/usr/bin/python
import sys
import logging
from argparse import ArgumentParser

###
recordCount = 0
currentRecord = ''
lastRecord = ''

SOR = '55aaeb90'

log = logging.getLogger('JKBMS-BT')
# setup logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# set default log levels
log.setLevel(logging.INFO)
logging.basicConfig()

#parser = ArgumentParser(description='MPP Solar Command Utility')
#parser.add_argument('-f', '--logfile', help='Log file to process', default='./jkbms.log')

#args = parser.parse_args()
logfile0 = './jkbms0.log'
logfile1 = './jkbms1.log'
logfile2 = './jkbms2.log'
logfile3 = './jkbms5.log'
logfile4 = './jkbms6.log'


def chunkString(name, string, length):
    result = []
    result.append('{:^{width}}'.format(name[0:length], width=length))
    for i in range(0, len(string), length):
        result.append(string[0+i:length+i])
    return result

def getRecord(contents, recordNum):
    offset = 0
    for x in range(0,recordNum):
        start = contents.find(SOR, offset) # gets 1st record
        end = contents.find(SOR, len(SOR)+offset) # gets 2nd record
        offset = end
    return contents[start:end].replace('\n','')

def compareRecords(location, chunkSize, records):
    #print location, chunkSize, records
    recordChunks = []
    for record in records:
        name = record[0]
        section = record[1][location[0]:location[1]]
        #print section
        chunks = chunkString(name, section, chunkSize)
        recordChunks.append(chunks)
    numRecords = len(recordChunks)
    numChunks = len(recordChunks[0])
    for x in range(numChunks):
        for y in range(numRecords):
            sys.stdout.write('{} '.format(recordChunks[y][x]))
        print('')

def processRecord(record):
    sor = record[0:len(SOR)]
    # Convert the 2 byte *stored as string' to int
    recordCounter = int('0x{}'.format(record[8:12]), 16)
    recordSize = len(record)/2
    print ('Counter: {} Length: {} bytes'.format(recordCounter, recordSize))

    if recordSize == 300:
        # this is the record that repeats and is likely the cell data
        recordCellData = chunkString(record[12:192+12], 8)
        print ('First Chunk of possible cell data')
        for x in recordCellData:
            print x
    elif recordSize == 320:
        # this in the info record and the first record of the extended record flow
        print ('Not processing record')
    else:
        # unknown what this is
        print ('Unknown recordSize', recordSize)



with open(logfile0) as f0, open(logfile1) as f1, open(logfile2) as f2, open(logfile3) as f3, open(logfile4) as f4:
     fileContents0 = f0.read()
     fileContents1 = f1.read()
     fileContents2 = f2.read()
     fileContents3 = f3.read()
     fileContents4 = f4.read()
# record 1 is device info
# record 2 is initial response from extended info request
# record 3-22 are extended info requests

# compareRecords(location=[12, 192+12], chunkSize=8, records=(
#     ['f0r3', getRecord(fileContents0, 3)],
#     ['f0r4', getRecord(fileContents0, 4)],
#     ['f0r5', getRecord(fileContents0, 5)],
#     ['f1r3', getRecord(fileContents1, 3)],
#     ['f1r4', getRecord(fileContents1, 4)],
#     ['f1r5', getRecord(fileContents1, 5)],
#     ['f2r3', getRecord(fileContents2, 3)],
#     ['f2r4', getRecord(fileContents2, 4)],
#     ['f2r5', getRecord(fileContents2, 5)],
#     ['f3r3', getRecord(fileContents3, 3)],
#     ['f3r4', getRecord(fileContents3, 4)],
#     ['f3r5', getRecord(fileContents3, 5)],
#     ))

cell = 1
for fileNum in (fileContents0, fileContents1, fileContents2, fileContents3, fileContents4):
    for recNum in range(3,22):
        record = getRecord(fileNum, recNum)
        print ('{} 0x{} {}'.format(record[0:10], record[10:12], record[cell*12:cell*12+8]))

## file is hex, but stored as ascii
# for line in fileContents:
#     line = line[:-1]  # remove newline
#     if line.startswith(SOR):
#         # this line signifies the start of a new reocrd
#         recordCount += 1
#         if recordCount > 1:
#             # have complete record
#             lastRecord = currentRecord
#             processRecord(lastRecord)
#         currentRecord = line
#     else:
#         # more data for the 'current' record
#         currentRecord += line
# recordCount += 1
# processRecord(currentRecord)
    #print (line)
#print ('Found {} records'.format(recordCount-1))

