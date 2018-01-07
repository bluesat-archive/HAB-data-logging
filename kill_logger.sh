#!/bin/bash

# ONLY RUN THIS SCRIPT IF YOU HAVE RUN THE start.sh SCRIPT FIRST
# This script will read the Process IDs saved by each python script and kill them one by one
# By Adithya Rajendran
# BLUEsat December 2017

file1="BMP280/.PID"
read -r BMP_PID<$file1
kill $BMP_PID
echo "$BMP_PID was killed"

file2="DHT22/.PID"
read -r DHT_PID<$file2
kill $DHT_PID
echo "$DHT_PID was killed"

file3="MPU9250/.PID"
read -r MPU_PID<$file3
kill $MPU_PID
echo "$MPU_PID was killed"

file4="MAX31865/.PID"
read -r MAX_PID<$file4
kill $MAX_PID
echo "$MAX_PID was killed"

echo "
All loggers successfully killed."