import matplotlib.pyplot as plt
import numpy as np
import csv
import re
import pandas
import sys
import argparse
import operator
	
file = open('box_lat.csv', 'w')
file_lng = open('box_lng.csv', 'w')
actual = []
overallLatData = []
overallLngData = []
deviceList = []

reader_pre = csv.reader(open("history.csv"), delimiter=",")
next(reader_pre)
sortedlist = sorted(reader_pre, key=operator.itemgetter(0), reverse=False)
# file.write("100, 101\n")
def extract_write_file(file_list):
	global overallLatData
	global overallLngData
	currentDevice = '100'
	latList=[]
	lngList=[]
	global deviceList
	deviceList.append(100)
	for index in range(0, len(file_list)):
		if(currentDevice!=file_list[index][0]):
			# print file_list[index][0]
			deviceList.append(file_list[index][0])
			# print latList
			overallLatData.append(latList)
			overallLngData.append(lngList)
			lngList=[]
			latList=[]
			latList.append(float(file_list[index][1])*27)
			lngList.append(float(file_list[index][2])*27)
			currentDevice = file_list[index][0]
		else:
			latList.append(float(file_list[index][1])*27)
			lngList.append(float(file_list[index][2])*27)

	for j in range(0, len(deviceList)):
		file.write(str(deviceList[j])+ ",")
		file_lng.write(str(deviceList[j])+ ",")
	file_lng.write("\n") 	
	file.write(str("\n"))



def check_write(Data, filename):
	maxLength = 0
	for i in range(0, len(Data)):
		if(len(overallLatData[i])>maxLength):
			maxLength=len(Data[i])
	
	k=0


	while(k<maxLength):
		for i in range(0, len(Data)):
			if(len(Data[i])>k):
				filename.write(str(Data[i][k])+ ",")
		k+=1;
		filename.write(str("\n"))
	# print(deviceList)
extract_write_file(sortedlist)	
check_write(overallLatData, file)
check_write(overallLngData, file_lng)	
		# if currentDevice!=row[0]:
		
		# file.write()
	# with open(filename,'r') as csvfile:
	# 	next(csvfile)
	# 	plots = csv.reader(csvfile, delimiter=',')
	# 	for row in plots:
	# 		if row[0]=='100':
	# 			actual.insert(int('100')%100, row[1])
	# 		elif row[0]=='101':
	# 			actual.insert(int('101')%100, row[1])	
				#next(csvfile)
				# actual.append((row[k].replace(' ', '')))		
			# x.append((row[0]))
			# y.append((row[1]))  
		# print actual
			  	
# extract_write_file('history.csv')	
# # for i in range(0, len(actual)):
# # 	print str(actual[i]) + "\n"	
# print actual[0][0]

# print sortedlist[0]
data = pandas.read_csv('box_lng.csv')
# device_data = data.groupby('deviceid')
data.boxplot(column=['100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111',
						'112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123',
							'124', '125', '126', '127'])
# data.boxplot(column=['101'])

# from pandas.tools import plotting
# plotting.scatter_matrix(data[['Weight', 'Height', 'MRI_Count']])

# plotting.scatter_matrix(data[['PIQ', 'VIQ', 'FSIQ']])

# plt.figure(figsize=(4, 3))
# data.boxplot(column=['Station1'])

# plt.figure(figsize=(4, 3))
# plt.boxplot(data['FSIQ'] - data['PIQ'])
# plt.xticks((1, ), ('FSIQ - PIQ', ))

plt.show()