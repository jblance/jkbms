# JK BMS Inquiry #

*WIP*

Python library to talk to a JK-B1A24S or B2A24S battery monitor via bluetooth (BLE)

## Requirements: ##
- python3 (python2 not supported) `sudo apt-get install python3-pip`
- bluepy `sudo pip3 install bluepy`
- paho-mqtt if publishing to MQTT `sudo pip3 install paho-mqtt`
- a device with BLE support (Raspberry Pi 3 or 4 have BLE builtin)

If you are using the daemon, check the [daemon readme](daemon/README.md)


## Troubleshooting ##
- Make sure the JK App is getting data correctly
- Do a BLE scan (outside of python) `sudo hcitool lescan`
- Check the config file is as expected `jkbms -d`
- Try debuging without sending to MQTT broker `jkbms -D -p`
- Log an issue with the above information
