#!/bin/bash

sudo pigpiod
echo "
\"Can't initialise pigpio library\" message will display if the pigpiod daemon is already running. This is normal.
"

cd BMP280
python BMPlogger.py &
echo "BMP Process Number:" $!

cd ..
cd DHT22
python DHTlogger.py &
echo "DHT Process Number:" $!

cd ..
cd MPU9250
python MPUlogger.py &
echo "MPU Process Number:" $!

cd ..
cd MAX31865
python MAX31865logger.py &
echo "MAX Process Number:" $!

echo "
Started logging..."