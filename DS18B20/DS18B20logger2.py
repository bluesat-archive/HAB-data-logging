# Import required modules
import smbus2
import bme280
import time
import sys
import csv
import signal
import os
import glob


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[1]
device_file = device_folder + '/w1_slave'


# The following code will write the Process ID of this script to a hidden file
pid = os.getpid()
PIDfilename = ".PID2"
PIDfile = open(PIDfilename, "wt")
PIDfile.write(str(pid))
PIDfile.close()


# The following function handles the case when a kill signal is sent to the process
def signal_term_handler(signal, frame):
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()

signal.signal(signal.SIGTERM, signal_term_handler)


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


# Variables
rowNumber = 1		# this is the counter for the overall row number, regardless of the number of log files generated
sleepTime = 1		# time to wait between reading from the sensor in seconds


try:
	while True: 									# infinite loop
		filename = 'data2/' + time.strftime('%I%M%p_%d-%m-%y') + '.csv'		# the strftime argument can be changed to produce a different time/date structure
		with open(filename, "wt") as ofile:					# ofile is the file handler for our new file (w means write, and t means text mode)
			writer = csv.writer(ofile)					# the csv writer module is initialised
			if rowNumber == 1:
				writer.writerow(("Row", "Time", "Temperature"))
			for i in range (0,300): 					# writes 300 rows in a single file
				time.sleep(sleepTime)
				temperature = read_temp()
				Time = str(time.strftime('%X'))				# change this to the time format you want recorded in each row
				writer.writerow((rowNumber, Time, temperature))
				rowNumber = rowNumber + 1				# the loop will now restart and create a new log file, but continue the row numbers


# Handles the case when user exits the running script using Control+C
except KeyboardInterrupt:
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()