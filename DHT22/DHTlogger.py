# Import required modules
import pigpio
import DHT22
import sys
import csv
import datetime
import time
import os
import signal

# The following code will write the Process ID of this script to a hidden file
pid = os.getpid()
PIDfilename = ".PID"
PIDfile = open(PIDfilename, "wt")
PIDfile.write(str(pid))
PIDfile.close()


# Initialise the sensor:
pi = pigpio.pi()
dht = DHT22.sensor(pi, 17)
dht.trigger()		#trigger the sensor at the start and ignore this initial reading


# The following function handles the case when a kill signal is sent to the process
def signal_term_handler(signal, frame):
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()

signal.signal(signal.SIGTERM, signal_term_handler)


# This function reads the sensor
def readDHT22():
	dht.trigger()
	humi = '%.2f' % (dht.humidity())
	temp = '%.2f' % (dht.temperature())
	return(humi, temp)


# Variables:
rowNumber = 1		# this is the counter for the overall row number, regardless of the number of log files generated
sleepTime = 3		# time to sleep between sensor reads in seconds (DO NOT READ THE DHT22 MORE THAN ONCE EVERY 2 SECS)


try:
	while True: 									# infinite loop
		filename = 'data/' + time.strftime('%I%M%p_%d-%m-%y') + '.csv'		# the strftime argument can be changed to produce a different time/date structure
		with open(filename, "wt") as ofile:					# ofile is the file handler for our new file (w means write, and t means text mode)
			writer = csv.writer(ofile)					# the csv writer module is initialised
			if rowNumber == 1:
				writer.writerow(("Row", "Time", "Temperature", "Humidity"))
			for i in range (0,100): 					# writes 100 rows in a single file
				time.sleep(sleepTime)
				Time = str(time.strftime('%X'))				# change this to the time format you want recorded in each row
				humidity, temperature = readDHT22()
				writer.writerow((rowNumber, Time, temperature, humidity))
				rowNumber = rowNumber + 1				# the loop will now restart and create a new log file, but continue the row numbers


except KeyboardInterrupt:
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()