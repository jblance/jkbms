#!/usr/bin/python3
#
#

import paho.mqtt.publish as publish


def publishMqtt(msgData, format='influx2', broker=None, tag=''):
    '''
    '''
    if broker is None:
        # Just print the msgData
        # {'VoltageCell01': '3.5387'}:influx2:192.168.1.230
        print('{}:{}:{}:{}'.format(msgData, format, broker, tag))
    elif format == 'influx2':
        #
        # mpp-solar,command=QPGS0 max_charger_range=120.0
        # jkbms, command=Power_Wall_1 volts_cell_01=3.4567
        #
        # +-----------+--------+-+---------+-+---------+
        # |measurement,tag_set field_set
        # +-----------+--------+-+---------+-+---------+
        # msgs.append('{}={}'.format(key, float(result)))
        print('Influx2 {}:{}:{}:{}'.format(msgData, format, broker, tag))
        # print('MPP-Solar-Service: format influx2 yet to be supported')
        msgs = []
        _data = msgData
        for _item in _data:
            payload = 'jkbms,command={} {}={}'.format(tag, _item, _data[_item])
            msg = {'topic': 'jkbms', 'payload': payload}
            msgs.append(msg)
            publish.multiple(msgs, hostname=broker)
