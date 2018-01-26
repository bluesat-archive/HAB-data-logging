#!/bin/bash

if [ -f "BMP280/.PID" ] || [ -f "DHT22/.PID" ] || [ -f "MPU9250/.PID" ] || [ -f "MAX31865/.PID" ] || [ -f "DS18B20/.PID" ] || [ -f "DS18B20/.PID2" ]
then
	echo "Recording script is running. Please stop this first by running ./kill_logger.sh"
	exit 1
fi


echo "
Do you wish to delete all logs? 
Enter Option No. and hit enter.
WARNING: THIS CANNOT BE UNDONE!
"
select yn in "Yes" "No" "Cancel"; do
    case $yn in
        Yes )
		rm -f BMP280/data/*.csv		
		rm -f DHT22/data/*.csv
		rm -f MPU9250/data/*.csv
		rm -f MAX31865/data/*.csv
		rm -f DS18B20/data/*.csv
		rm -f DS18B20/data2/*.csv
		rm -f CPUtemp/data/*.csv
		echo "
Cleaned up all log files."
		exit 1;;
        No )
		echo "
Did not remove anything"
		exit 1;;
	Cancel )
		echo "
Cancelled"
		exit 1;;
	*)
		echo "Invalid Option";;
    esac
done
