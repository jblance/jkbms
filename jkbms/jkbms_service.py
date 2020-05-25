#!/usr/bin/python3
#
#
# jkbms-service
#
from argparse import ArgumentParser
import configparser
import paho.mqtt.publish as publish
import systemd.daemon
import time

import logging
log = logging.getLogger('JKBMS-BT')

from .jkbms import jkBMS


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
        mqtt_broker = config['SETUP'].get('mqtt_broker', fallback=None)
        logging_level = config['SETUP'].getint('logging_level', fallback=logging.CRITICAL)
        max_connection_attempts = config['SETUP'].getint('max_connection_attempts', fallback=3)
        records = config['SETUP'].getint('records', fallback=1)
        log.setLevel(logging_level)
        sections.remove('SETUP')
    else:
        print('JKBMS-Service: Config file missing SETUP section')
    print('JKBMS-Service: Config setting - mqtt_broker: {}'.format(mqtt_broker))
    print('JKBMS-Service: Config setting - command sections found: {}'.format(len(sections)))
    # Tell systemd that our service is ready
    systemd.daemon.notify('READY=1')

    # Build array of commands to run
    for section in sections:
        systemd.daemon.notify('WATCHDOG=1')
        name = section
        model = config[section].get('model')
        mac = config[section].get('mac')
        command = config[section].get('command')
        tag = config[section].get('tag')
        format = config[section].get('format')
        jk = jkBMS(name=name, model=model, mac=mac, command=command, tag=tag, format=format, records=records, maxConnectionAttempts=max_connection_attempts, mqttBroker=mqtt_broker)
        log.debug(str(jk))
        if jk.connect():
            systemd.daemon.notify('WATCHDOG=1')
            jk.getBLEData()
            jk.disconnect()
        else:
            print ('Failed to connect to {} {}'.format(self.name, self.mac))
