#!/bin/bash

if [ "$(whoami)" != "root" ]
then
    sudo su -s "$0"
    exit
fi

echo input > /sys/class/leds/led1/trigger
echo mmc0 > /sys/class/leds/led0/trigger

echo "
Onboard LEDs will now return to system control"