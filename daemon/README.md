# Installing as a Service #
source: https://github.com/torfsen/python-systemd-tutorial

## Pre-reqs ##
Need python-systemd package
* `sudo apt-get install python3-systemd`

Need to create a config file `/etc/jkbms/jkbms.conf`
* Use the example `/etc/jkbms/jkbms.conf.example` as a start

### Config File Description ###
```
[SETUP]
mqtt_broker = mqtthost
max_connection_attempts = 3
# Uncomment one of the logging_level lines
# All messages at the uncommented level and higher will be displayed
# i.e. DEBUG gives the most output and CRITICAL gives the least
### DEBUG
#logging_level =   10
### INFO
logging_level =  20
### WARNING
#logging_level =  30
### ERROR
#logging_level =  40
### CRITICAL
#logging_level =  50

# JKBMS
[Power Wall 1]
model =   JK-B2A24S
mac =     3c:a5:09:0a:85:79
tag =     Power_Wall_1
format =  influx2   # Format of MQTT message to post - valid (so far) influx2
                    # for MQTT to Grafana via telegraf (as documented)
```
## Add JKBMS service ##

* Check the service exists
`systemctl --user list-unit-files|grep jkbms`
```
jkbms.service              disabled
```
* Start the service
`systemctl --user start jkbms`

* Check service status
`systemctl --user status jkbms`
```
TODO ADD DEBUG HERE
...
```

* Stopping the service
`systemctl --user stop jkbms`

* Restart the service - for example after a config file change
`systemctl --user restart jkbms`

Logs and service output
* The output should show up in systemd's logs, which by default are redirected to syslog:
`grep 'jkbms' /var/log/syslog`
```
TODO
```

* Another way to display the service's output is via
`journalctl --user-unit jkbms`

## Automatically Starting the Service during Boot ##
```
systemctl --user enable jkbms
sudo loginctl enable-linger $USER
```

* To disable autostart, simply disable your service:
`systemctl --user disable jkbms`

Note that simply enabling a service does not start it, but only activates autostart during boot-up. Similarly, disabling a service doesn't stop it, but only deactivates autostart during boot-up. If you want to start/stop the service immediately then you still need to do that manually

To check whether your service is enabled, use

`systemctl --user list-unit-files | grep jkbms`
```
jkbms.service              enabled
```
