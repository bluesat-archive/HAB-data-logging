#!/bin/bash

cd BMP280/data
file1=$(ls -tr | tail -1)
geany "$file1" &

cd ../../DHT22/data
file2=$(ls -tr | tail -1)
geany "$file2" &

cd ../../DS18B20/data
file3=$(ls -tr | tail -1)
geany "$file3" &

cd ../../DS18B20/data2
file4=$(ls -tr | tail -1)
geany "$file4" &

cd ../../MAX31865/data
file5=$(ls -tr | tail -1)
geany "$file5" &

cd ../../MPU9250/data
file6=$(ls -tr | tail -1)
geany "$file6" &

cd ../../CPUtemp/data
file7=$(ls -tr | tail -1)
geany "$file7" &
