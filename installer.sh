#!/bin/bash


sudo pip3 install -r requirements.txt

mkdir -p /usr/local/water-meter
cp water-meter.py /usr/local/water-meter/water-meter.py
cp flowcounter.py /usr/local/water-meter/flowcounter.py
cp config.ini /usr/local/water-meter/config.ini
cp water-meter.service /lib/systemd/system/water-meter.service 
sudo systemctl enable water-meter.service

mkdir -p /var/log/water-meter
