# Import required modules
import max31865
import time
import sys
import datetime
import os
import signal
import csv


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
sleepTime = 1				# time to sleep between sensor reads in seconds
rowNumber = 1				# this is the counter for the overall row number, regardless of the number of log files generated
reader = max31865.max31865()		# initialises this variable as the sensor


try:
	while True: 									# infinite loop
		filename = 'data/' + time.strftime('%I%M%p_%d-%m-%y') + '.csv'		# the strftime argument can be changed to produce a different time/date structure
		with open(filename, "wt") as ofile:					# ofile is the file handler for our new file (w means write, and t means text mode)
			writer = csv.writer(ofile)					# the csv writer module is initialised
			if rowNumber == 1:
				writer.writerow(("Row", "Time", "Temperature"))
			for i in range (0,300): 					# writes 300 rows in a single file
				time.sleep(sleepTime)					# change this to the time format you want recorded in each row
				temperature = reader.readTemp()				# reads sensor values
				Time = str(time.strftime('%X'))
				writer.writerow((rowNumber, Time, temperature))
				rowNumber = rowNumber + 1				# the loop will now restart and create a new log file, but continue the row numbers

except KeyboardInterrupt:
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()