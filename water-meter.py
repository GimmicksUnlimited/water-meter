import logging
from logging.handlers import RotatingFileHandler 
import time
import os
import configparser
from service import Service
from Adafruit_IO import Client
from flowcounter import FlowCounter


class MyService(Service):
    def __init__(self, *args, **kwargs):
        super(MyService, self).__init__(*args, **kwargs)
        rfh = RotatingFileHandler("/var/log/water-meter/water-meter.log", mode='a', maxBytes=10000, backupCount=3, 
							encoding=None, delay=False)
        
        rfh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(rfh)
        self.logger.setLevel(logging.INFO)
        self.config = configparser.ConfigParser()
        self.config.read('/usr/local/water-meter/config.ini')
        self.logger.info('config', self.config);

        self.logger.info("initialized...")


    def run(self):
        self.logger.info("run start");
        self.aio = Client(self.config['adafruit.io']['user'], self.config['adafruit.io']['api_key']) 
        self.fc = FlowCounter(self.aio, float (1) / 374, 200, self.logger)
        while not self.got_sigterm():
            self.log_temp()
            time.sleep(30)
        self.logger.info("run done");


    def log_temp(self):

        try:
            tf = open('/sys/class/thermal/thermal_zone0/temp')
            temp = float(tf.read())
            tempC = temp/1000
            self.logger.info("cpu temp %f" % tempC)
            self.aio.send('water-meter', tempC)

        except:
            self.logger.err("Problem reading a thermal file")


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND' % sys.argv[0])

    cmd = sys.argv[1].lower()
    service = MyService('water-meter', pid_dir='/tmp')

    if cmd == 'start':
        service.start()
    elif cmd == 'stop':
        service.stop()
    elif cmd == 'status':
        if service.is_running():
            print ("Service is running with PID.", service.get_pid());
        else:
            print ("Service is not running.");
    else:
        sys.exit('Unknown command "%s".' % cmd)
