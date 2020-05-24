#!/usr/bin/python3
#
#
# jkbms-service
#
import configparser
import time
import systemd.daemon
from argparse import ArgumentParser

import paho.mqtt.publish as publish


def main():
    # Some default defaults
    mqtt_broker = 'localhost'
    sectionArray = []

    # Process arguments
    parser = ArgumentParser(description='JKBMS Helper Service')
    parser.add_argument('-c', '--configfile', type=str, help='Full location of config file', default='/etc/jkbms/jkbms.conf')
    args = parser.parse_args()

    print('JKBMS-Service: Initializing ...')
    print('JKBMS-Service: Config file: {}'.format(args.configfile))
    config = configparser.ConfigParser()
    config.read(args.configfile)
    sections = config.sections()

    if 'SETUP' in config:
        mqtt_broker = config['SETUP'].get('mqtt_broker', fallback='localhost')
        sections.remove('SETUP')
    print('JKBMS-Service: Config setting - mqtt_broker: {}'.format(mqtt_broker))
    print('JKBMS-Service: Config setting - command sections found: {}'.format(len(sections)))
    # Build array of commands to run

    for section in sections:
        # print('MPP-Solar-Service: Execute - {}'.format(config[section]))
        model = config[section].get('model')
        mac = config[section].get('mac')
        command = config[section].get('command')
        tag = config[section].get('tag')
        format = config[section].get('format')
        # Need to build something here....
        # mp = mppUtils(port, baud, model)
        sectionArray.append({'section': section, 'model': model, 'mac': mac, 'command': command, 'format': format, 'tag': tag})

    # Tell systemd that our service is ready
    systemd.daemon.notify('READY=1')

    while True:
        # Loop through the configured commands
        for item in sectionArray:
            # Tell systemd watchdog we are still alive
            systemd.daemon.notify('WATCHDOG=1')
            print('JKBMS-Service: item {}'.format(item))
            # mpp-solar,command=QPGS0 max_charger_range=120.0
            # +-----------+--------+-+---------+-+---------+
            # |measurement,tag_set field_set
            # +-----------+--------+-+---------+-+---------+
            # msgs.append('{}={}'.format(key, float(result)))
            if item['format'] == 'influx200':
                # print('JKBMS-Service: format influx2 yet to be supported')
                msgs = []
                _data = item['mp'].getInfluxLineProtocol2(item['command'])
                for _item in _data:
                    payload = 'jkbms,command={} {}'.format(item['tag'], _item)
                    msg = {'topic': 'jkbms', 'payload': payload}
                    msgs.append(msg)
                publish.multiple(msgs, hostname=mqtt_broker)
            else:
                print('JKBMS-Service: format {} not supported'.format(item['format']))

        # Tell systemd watchdog we are still alive
        systemd.daemon.notify('WATCHDOG=1')
        time.sleep(pause)
