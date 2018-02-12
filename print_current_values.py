#!/usr/bin/python2

# Import required modules
import pigpio
import smbus2
import time
import DHT22
import bme280
import max31865
import FaBo9Axis_MPU9250

# Read and print the DHT22 sensor:
pi = pigpio.pi()
dht = DHT22.sensor(pi, 17)
dht.trigger()		#trigger the sensor at the start and ignore this initial reading
time.sleep(2)
dht.trigger()
humi = '%.2f' % (dht.humidity())
temp = '%.2f' % (dht.temperature())
print 'DHT22 (Temperature, Humidity): ', temp, humi

# Read the BMP280 sensor
port = 1
address = 0x76
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address)
pressure = data.pressure
temperature = data.temperature
print 'BMP280 (Pressure, Temperature): ', pressure, temperature

# Read both DS18B20 temp sensors
base_dir = '/sys/bus/w1/devices/'
device1_folder = base_dir + '28-000008c640c9' # This is sensor module PCB
device1_file = device1_folder + '/w1_slave'
device2_folder = base_dir + '28-00000a42b554' # This is the sensor soldered onto the Pi Hat
device2_file = device2_folder + '/w1_slave'

def read_temp_raw(device_file):
	f = open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(device_file):
	lines = read_temp_raw(device_file)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_time_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c

temperature1 = read_temp(device1_file)
temperature2 = read_temp(device2_file)
print 'First DS18B20 temperature (on module): ', temperature1
print 'Second DS18B20 temperature (on HAT): ', temperature2

# Read PT100 probe temperature
reader = max31865.max31865()		# initialises this variable as the sensor
print 'PT100 Probe Temperature: ', reader.readTemp()

# Read MPU motion data
mpu9250 = FaBo9Axis_MPU9250.MPU9250()
accel = mpu9250.readAccel()
gyro = mpu9250.readGyro()
mag = mpu9250.readMagnet()
print 'MPU9250 Data ' '(Acceleration-x', 'Acceleration-y', 'Acceleration-z', 'Gyro-x', 'Gyro-y', 'Gyro-z', 'Mag-x', 'Mag-y', 'Mag-z): ', accel['x'], accel['y'], accel['z'], gyro['x'], gyro['y'], gyro['z'], mag['x'], mag['y'], mag['z']

# Read CPU Temperature
tFile = open('/sys/class/thermal/thermal_zone0/temp')
temp = float(tFile.read())
CPUtemp = temp/1000
print 'CPU Temperature: ', CPUtemp
