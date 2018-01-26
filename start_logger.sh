#!/bin/bash

file1="BMP280/.PID"
file2="DHT22/.PID"
file3="MPU9250/.PID"
file4="MAX31865/.PID"
file5="DS18B20/.PID"
file6="DS18B20/.PID2"
file7="CPUtemp/.PID"

if [ -f "$file1" ] || [ -f "$file2" ] || [ -f "$file3" ] || [ -f "$file4" ] || [ -f "$file5" ] || [ -f "$file6" ] || [ -f "$file7" ]
then
	echo "Logging scripts are already running. Type ./kill_logger.sh to stop them. Or reboot the Pi using \"reboot\" if that does not work."
	exit 1
fi

sudo pigpiod
echo "
\"Can't initialise pigpio library\" message will display if the pigpiod daemon is already running. This is normal.
"

cd BMP280
python BMPlogger.py &
echo "BMP Process Number:" $!

cd ../DHT22
python DHTlogger.py &
echo "DHT Process Number:" $!

cd ../MPU9250
python MPUlogger.py &
echo "MPU Process Number:" $!

cd ../MAX31865
python MAX31865logger.py &
echo "MAX Process Number:" $!

cd ../DS18B20
python DS18B20logger.py &
echo "B20 Process Number:" $!

python DS18B20logger2.py &
echo "B20 Process Number:" $!

cd ../CPUtemp
./temperature_log.sh &
echo "$!" > .PID
echo "CPU temp_logger Process Number:" $!

echo "
Started logging..."

cd ..
./heartbeat_onboard_LEDs.sh
