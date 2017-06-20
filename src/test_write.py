import matplotlib.pyplot as plt
import numpy as np
import csv
import re

x = []
y = []
lon_file = open('error_lon_readings.csv', 'w')
lat_file = open('error_lat_readings.csv', 'w')

def extract_write_file(filename):
	with open(filename,'r') as csvfile:
		plots = csv.reader(csvfile, delimiter='\t')
		for row in plots:
			x.append((row[0]))
			y.append((row[1]))    	

extract_write_file('Lat&Lon.txt')			


def extract_device_lon(filename, value, file):
	with open(filename, 'rU') as csvfile:
		plots = csv.reader(csvfile, delimiter=',')
		for row in plots:
			for num in range(0, 13):
				stationObj = re.search("Station", row[num])
				deviceObj = re.match("40", row[num])
				if row[num] == repr(num):
					if num == 12:
						file.write(row[num]+"\n")
					else:
						file.write(row[num]+";")	
				elif row[num] == "Device":
					file.write("Device"+";") 			
				else:		
					if deviceObj:
							file.write(row[num]+";")
					elif row[num]=='NA':
						if num == 12:
							file.write("NA"+"\n")
						else:
							file.write("NA"+";")	
					else:		
						measured_lon = row[num]
						error_lon = abs(float(value[num-1]) - (28*float(measured_lon)))
						error_lon = round(error_lon, 5)
						if num == 12:
							file.write(repr(error_lon)+"\n")
						else:
							file.write(repr(error_lon)+";")		
		file.close()

extract_device_lon('402_Lon.txt', x, lon_file)
extract_device_lon('402_Lat.txt', y, lat_file)



