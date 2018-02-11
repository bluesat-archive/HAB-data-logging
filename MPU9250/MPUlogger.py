# Import required modules
import FaBo9Axis_MPU9250
import time
import sys
import csv
import datetime
import os
import signal


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


# Variables:
rowNumber = 1				# this is the counter for the overall row number, regardless of the number of log files generated
sleepTime = 0.5				# time to sleep between sensor reads in seconds
mpu9250 = FaBo9Axis_MPU9250.MPU9250()


try:
	while True: 									# infinite loop
		filename = 'data/' + time.strftime('%I%M%p_%d-%m-%y') + '.csv'		# the strftime argument can be changed to produce a different time/date structure
		with open(filename, "wt") as ofile:					# ofile is the file handler for our new file (w means write, and t means text mode)
			writer = csv.writer(ofile)					# the csv writer module is initialised
			if rowNumber == 1:
				writer.writerow(('Row', 'Time', 'Acceleration-x', 'Acceleration-y', 'Acceleration-z', 'Gyro-x', 'Gyro-y', 'Gyro-z', 'Mag-x', 'Mag-y', 'Mag-z'))
			for i in range (0,600): 					# writes 600 rows in a single file
				time.sleep(sleepTime)
				Time = str(time.strftime('%X'))				# change this to the time format you want recorded in each row
				accel = mpu9250.readAccel()
				gyro = mpu9250.readGyro()
				mag = mpu9250.readMagnet()
				writer.writerow((rowNumber, Time, accel['x'], accel['y'], accel['z'], gyro['x'], gyro['y'], gyro['z'], mag['x'], mag['y'], mag['z']))
				rowNumber = rowNumber + 1				# the loop will now restart and create a new log file, but continue the row numbers

except KeyboardInterrupt:
	ofile.close() 			#closes the csv file handler (not sure if this works)
	os.remove(PIDfilename) 		#removes the hidden file
	sys.exit()
