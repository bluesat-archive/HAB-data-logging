#!/bin/bash

timestamp=`date +%I%M%p_%d-%m-%y`
filepath=data/$timestamp.csv
echo "CPU Temperature Log (*C) - $(date)" > $filepath
echo "Time,Temperature" >> $filepath
while :
do
	temp=`/opt/vc/bin/vcgencmd measure_temp`
	temp=${temp:5:4}
	time=`date +%T`
	echo "$time,$temp" >> $filepath
	sleep 10
done
