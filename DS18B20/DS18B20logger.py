import os
import time
import glob
import csv 

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'

folder = '/home/pi/Desktop/Logger/DS18B20/data/'
filename = str(time.strftime('%d_%M_%s')) + '.csv'
os.system("touch " + filename)

def read_temp_raw():
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_time_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c

while True:
	temp = read_temp()
	date = str(time.strftime('%X %S %x %Z'))
	os.system("echo '" + date + ", " + str(temp) + "' >> " + folder + filename)
	time.sleep(0.5)

