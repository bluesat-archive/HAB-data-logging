##############################################
'''

# the 'sample' method will take a single reading and return a compensated_reading object
data = bme280.sample(bus, address)

# the compensated_reading class has the following attributes
print(data.id)
print(data.timestamp)
print(data.temperature)
print(data.pressure)
print(data.humidity)
# there is a handy string representation too
print(data)
'''
##############################################


# Import required modules
import smbus2
import bme280
import time
import sys
import csv
import signal
import os


# Initialise the sensor
port = 1
address = 0x76
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)


# The following code will write the Process ID of this script to a hidden file
pid = os.getpid()
PIDfilename = ".PID"
PIDfile = open(PIDfilename, "wt")
PIDfile.write(str(pid))
PIDfile.close()


# The following function handles the case when a kill signal is sent to the process
def signal_term_handler(signal, frame):
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()

signal.signal(signal.SIGTERM, signal_term_handler)


# Variables
rowNumber = 1		# this is the counter for the overall row number, regardless of the number of log files generated
sleepTime = 1		# time to wait between reading from the sensor in seconds


try:
	while True: 									# infinite loop
		filename = 'data/' + time.strftime('%I%M%p_%d-%m-%y') + '.csv'		# the strftime argument can be changed to produce a different time/date structure
		with open(filename, "wt") as ofile:					# ofile is the file handler for our new file (w means write, and t means text mode)
			writer = csv.writer(ofile)					# the csv writer module is initialised
			if rowNumber == 1:
				writer.writerow(("Row", "Time", "Pressure", "Temperature"))
			for i in range (0,300): 					# writes 300 rows in a single file
				time.sleep(sleepTime)
				data = bme280.sample(bus, address)
				Time = str(time.strftime('%X'))				# change this to the time format you want recorded in each row
				pressure = data.pressure
				temperature = data.temperature
				writer.writerow((rowNumber, Time, pressure, temperature))
				rowNumber = rowNumber + 1				# the loop will now restart and create a new log file, but continue the row numbers


# Handles the case when user exits the running script using Control+C
except KeyboardInterrupt:
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()