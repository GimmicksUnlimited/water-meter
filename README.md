# water-meter
raspberrypi water metering service.


Watermeter uses a flow meter with signal wire attached to pin 23 using 650ohm 
resistor.  Daemon is bootstraped using Service package that wraps application 
code under run method.  Service automatically responds to ```start, stop, status``` 
commands.  Service is added to the os using sysctl through water-meter.service.

# Installation

Installation is done using ```installer.sh``` which using pip3 installs python 
module prerequisites, these are specified in the requirements.txt, copies code
and service files in appropriate locations, sets up service to run by defailt 
and creates directory for logs. 


# Running

To run water-meter service use service command:

```sudo service water-meter start```
This starts up the service


```sudo service water-meter status```
Current status of the service

```sudo service water-meter start```
Shuts down the service.


Besides capturing water flow metrics such as timing, volume and 'ticks' this 
service logs raspberrypi's temperature.


# Files

```/usr/local/water-meter/``` application code and configuration.

```/var/log/water-meter/``` water-meter logs. Short lived and quickly rotated. 

```/lib/systemd/system/water-meter.service``` - service script
