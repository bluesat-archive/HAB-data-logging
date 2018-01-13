#!/bin/bash

if [ "$(whoami)" != "root" ]
then
    sudo su -s "$0"
    exit
fi

echo heartbeat > /sys/class/leds/led0/trigger
echo heartbeat > /sys/class/leds/led1/trigger

echo "
Onboard LEDs will now be flashing"