import base64
import requests
# import urllib3
import json
from bokeh.charts import BoxPlot, Bar
from bokeh.layouts import row, layout
from bokeh.plotting import figure, show, output_file
from storePOI import office_POI, ward5_POI, actlab_POI
from storeScale import getScale, getCoordinates, getImage
import csv, operator
from datetime import datetime
from datetime import timedelta
from bokeh.io import curdoc
from bokeh.models import HoverTool, LabelSet
from bokeh.models.sources import ColumnDataSource
import csv, operator
import pandas as pd
from bokeh.models.widgets import Select, TextInput, CheckboxGroup
from bokeh.layouts import layout
import dateutil.relativedelta
import time
import dateutil.parser
import math
import calendar

robotAcc = []
beaconData = []
beaconData2 = []
beaconAcc = []
robotDev = []
robotDev2 = []
beaconDev = []
robotOverall = []
beaconOverall = []
coord_lat_list = []
coord_lng_list = []
history_list = []
temp = []
center = []
xlist = []
ylist = []
circle_x = []
circle_y = []
circle2_x = []
robot_time = []
circle2_y = []
coord_total_list = []
path_list = []
sortedlist = []
path_x = []
path_y = []
predicted_time = []
devList = []
robotX_avg = 0.0
robotY_avg = 0.0
strDate = 0
distance = 0.0
predict = 1
currTime = 1
startTime = 0
duration = 0
rtime_now = 0
ctime_now = 0
midx = 0.0
mid_y = 0.0
predictedStart = 0
predict_duration = 0
predict_time = 1
pre_current_dur = 0
# count = 0
timestamp = 0
mindiff = 0
robotLat = []
robotLat2 = []
robotLng = []
robotLng2 = []
beaconLat = []
beaconLat2 = []
beaconLng2 = []
beaconDev2 = []
beaconLng = []
stations = 0
robotlist2 = []
beaconlist2 = []
modifiedbeacon2 = []
data_dict = {}
data_dict2 = {}
data_dict3 = {}
data_dict4 = {}
data_dict5 = {}
data_dict6 = {}
checkpointNum = []
devicelist = []
# robo_data_dict = {}

beaconheat = open('beacon_heatmap.csv', 'w')
# robo_boxplot = open('robot_boxplot.csv', 'w')
# beacon_boxplot = open('beacon_boxplot.csv', 'w')
# robo_heatmap = open('heatmap_robot.csv', 'w')
# robo_boxplot2 = open('robot_boxplot2.csv', 'w')
# beacon_boxplot2 = open('beacon_boxplot2.csv', 'w')
# heatmap_error = open('heatmap_error.csv', 'w')
# heatmap_error2 = open('heatmap_error2.csv', 'w')
# robo_boxplot.write("Checkpoint, RobotX, RobotY\n")
# beacon_boxplot.write("Checkpoint, Device, BeaconX, BeaconY\n")
# heatmap_error.write("Checkpoint, ErrorDistance\n")
beaconheat.write("Checkpoint, Longtitude, Latitude, Device, Mean Error, Variance Error\n")
# robo_heatmap.write("Checkpoint, Longtitude, Latitude, Mean Error, Variance Error\n")
# robo_boxplot2.write("Checkpoint, RobotX, RobotY\n")
# beacon_boxplot2.write("Checkpoint, Device, BeaconX, BeaconY\n")
# heatmap_error2.write("Checkpoint, ErrorDistance\n")
def findMinimum_Maximum(_list):
	minimum = float((_list[0]))
	maximum = float((_list[0]))
	for a in range(1, len(_list)):
		temp = float((_list[a]))
		if temp<minimum:
			minimum = temp
		elif temp>maximum:   
			maximum = temp
	return minimum, maximum

def midpoint(x1, x2, y1, y2, divisor):
	midx = (x1 + x2)/divisor
	midy = (y1 + y2)/divisor
	return midx, midy

def setCheckpoints():
	checkpointfile = open('Checkpoints.csv', 'w')
	checkpointfile.write("Checkpoints, Longtitude, Latitude, Start Time, End Time\n")
	map_scale = getScale("MD6")
	checkpointfile.write("1, " + str((-4.52)/map_scale) + ", " + str((-1.05)/map_scale) + ", 2017-07-28 12:56:16, 2017-07-28 12:56:31\n")
	checkpointfile.write("2, " + str((-2.32)/map_scale) + ", " + str((-1.17)/map_scale) + ", 2017-07-28 12:56:56, 2017-07-28 12:57:11\n")
	checkpointfile.write("3, " + str((-0.801)/map_scale) + ", " + str((0.223)/map_scale) + ", 2017-07-28 12:57:32, 2017-07-28 12:57:47\n")
	checkpointfile.write("4, " + str((1.74)/map_scale) + ", " + str((1.35)/map_scale) + ", 2017-07-28 12:59:00, 2017-07-28 12:59:15\n")
	checkpointfile.write("5, " + str((0.0283)/map_scale) + ", " + str((3.8)/map_scale) + ", 2017-07-28 12:59:34, 2017-07-28 12:59:49\n")
	checkpointfile.write("6, " + str((-1.76)/map_scale) + ", " + str((2.53)/map_scale) + ", 2017-07-28 13:00:14, 2017-07-28 13:00:29\n")
	checkpointfile.write("7, " + str((-3.28)/map_scale) + ", " + str((1.59)/map_scale) + ", 2017-07-28 13:00:34, 2017-07-28 13:00:49\n")
	checkpointfile.write("8, " + str((-4.39)/map_scale) + ", " + str((0.657)/map_scale) + ", 2017-07-28 13:01:00, 2017-07-28 13:01:15\n")
	checkpointfile.write("9, " + str((-5.28)/map_scale) + ", " + str((2.17)/map_scale) + ", 2017-07-28 13:01:42, 2017-07-28 13:01:57\n")
	checkpointfile.write("10, " + str((-3.51)/map_scale) + ", " + str((3.26)/map_scale) + ", 2017-07-28 13:02:18, 2017-07-28 13:02:33\n")
	checkpointfile.write("11, " + str((-1.72)/map_scale) + ", " + str((4.29)/map_scale) + ", 2017-07-28 13:03:30, 2017-07-28 13:03:45\n")
	checkpointfile.write("12, " + str((-1.41)/map_scale) + ", " + str((5.37)/map_scale) + ", 2017-07-28 13:04:02, 2017-07-28 13:04:17\n")
	checkpointfile.write("13, " + str((-1.92)/map_scale) + ", " + str((6.96)/map_scale) + ", 2017-07-28 13:04:34, 2017-07-28 13:04:49\n")
	checkpointfile.write("14, " + str((-4.6)/map_scale) + ", " + str((6.38)/map_scale) + ", 2017-07-28 13:05:30, 2017-07-28 13:05:45\n")
	checkpointfile.write("15, " + str((-5.7)/map_scale) + ", " + str((3.98)/map_scale) + ", 2017-07-28 13:06:10, 2017-07-28 13:06:25\n")
	checkpointfile.write("16, " + str((-6.44)/map_scale) + ", " + str((3.12)/map_scale) + ", 2017-07-28 13:06:44, 2017-07-28 13:06:59\n")
	checkpointfile.write("17, " + str((-7.64)/map_scale) + ", " + str((1.55)/map_scale) + ", 2017-07-28 13:07:16, 2017-07-28 13:07:31\n")
	checkpointfile.write("18, " + str((-9.14)/map_scale) + ", " + str((4.23)/map_scale) + ", 2017-07-28 13:07:38, 2017-07-28 13:07:53\n")
	checkpointfile.write("19, " + str((-8.14)/map_scale) + ", " + str((6.75)/map_scale) + ", 2017-07-28 13:08:14, 2017-07-28 13:08:29\n")
	checkpointfile.write("20, " + str((-3.91)/map_scale) + ", " + str((9.23)/map_scale) + ", 2017-07-28 13:08:42, 2017-07-28 13:08:57\n")
	checkpointfile.write("21, " + str((0.359)/map_scale) + ", " + str((11.8)/map_scale) + ", 2017-07-28 13:09:20, 2017-07-28 13:09:35\n")
	checkpointfile.write("22, " + str((2.58)/map_scale) + ", " + str((13.5)/map_scale) + ", 2017-07-28 13:09:48, 2017-07-28 13:10:03\n")
	checkpointfile.write("23, " + str((3.28)/map_scale) + ", " + str((11.2)/map_scale) + ", 2017-07-28 13:10:26, 2017-07-28 13:10:41\n")
	checkpointfile.write("24, " + str((3.42)/map_scale) + ", " + str((8.47)/map_scale) + ", 2017-07-28 13:11:14, 2017-07-28 13:11:29\n")
	checkpointfile.write("25, " + str((4.88)/map_scale) + ", " + str((6.9)/map_scale) + ", 2017-07-28 13:12:22, 2017-07-28 13:12:37\n")
	checkpointfile.write("26, " + str((7.12)/map_scale) + ", " + str((8.49)/map_scale) + ", 2017-07-28 13:12:52, 2017-07-28 13:13:07\n")
	checkpointfile.write("27, " + str((6.58)/map_scale) + ", " + str((10.4)/map_scale) + ", 2017-07-28 13:13:26, 2017-07-28 13:13:41\n")
	checkpointfile.write("28, " + str((5.78)/map_scale) + ", " + str((12)/map_scale) + ", 2017-07-28 13:13:58, 2017-07-28 13:14:13\n")
	checkpointfile.write("29, " + str((9.83)/map_scale) + ", " + str((9.75)/map_scale) + ", 2017-07-28 13:14:54, 2017-07-28 13:15:09\n")
	checkpointfile.write("30, " + str((8.6)/map_scale) + ", " + str((11.7)/map_scale) + ", 2017-07-28 13:15:48, 2017-07-28 13:16:03\n")
	checkpointfile.write("31, " + str((7.25)/map_scale) + ", " + str((13.8)/map_scale) + ", 2017-07-28 13:16:50, 2017-07-28 13:17:05\n")
	checkpointfile.write("32, " + str((4.42)/map_scale) + ", " + str((14.6)/map_scale) + ", 2017-07-28 13:17:42, 2017-07-28 13:17:57")
	checkpointfile.close()
# setCheckpoints()

map_scale = getScale("MD6")
reader = csv.reader(open("robot_path_experiment4.csv"), delimiter=",")
beacon_reader = csv.reader(open("beacon_path_experiment4.csv"), delimiter=",")
# reader2 = csv.reader(open("robot_path_experiment2.csv"), delimiter=",")
# beacon_reader2 = csv.reader(open("beacon_path_experiment2.csv"), delimiter=",")
checkpoint_reader = csv.reader(open("Checkpoints.csv"), delimiter=",")
# next(reader)
# next(beacon_reader)
# next(reader2)
# next(beacon_reader2)
next(checkpoint_reader)
checkpointlist = sorted(checkpoint_reader, key=operator.itemgetter(0), reverse=False)
robotlist = sorted(reader, key=operator.itemgetter(0), reverse=False)
beaconlist = sorted(beacon_reader, key=operator.itemgetter(0, 1), reverse=False)
# robotlist2 = sorted(reader2, key=operator.itemgetter(0), reverse=False)
# beaconlist2 = sorted(beacon_reader2, key=operator.itemgetter(0, 5), reverse=False)

for i in range(0, len(checkpointlist)):
	checkpointNum.append(int(checkpointlist[i][0]))



def compileBoxplotList(_beacon, beacon_box, experimentID):
	randomRobotX = 0.0
	randomRobotY = 0.0
	PosrangeX = 0.0
	NegrangeX = 0.0
	PosrangeY = 0.0
	NegrangeY = 0.0
	beaconTime = 0
	modifiedbeacon = []
	for item in range(0, len(_beacon)):
		# if _beacon[item][3]==" ward5678":
		_beacon[item][1] = datetime.fromtimestamp((int(_beacon[item][1]))/1000).strftime("%Y-%m-%d %H:%M:%S")
		_beacon[item][2] = float(_beacon[item][2])
		_beacon[item][3] = float(_beacon[item][3])
		_beacon[item][0] = _beacon[item][0].split("b")
		_beacon[item][0] = _beacon[item][0][1]
		modifiedbeacon.append(_beacon[item])
	print (modifiedbeacon)
	# for num in range(0, len(_robot)):
	# 	randomRobotX = float(_robot[num][1])
	# 	randomRobotY = float(_robot[num][2])
	# 	_robot[num][0] = datetime.fromtimestamp(int(_robot[num][0])).strftime("%Y-%m-%d %H:%M:%S")
		# for indexes in range(0, len(checkpointlist)):
		# 	if checkpointlist[indexes][0]==str(3):
		# 		# print("Are you there?")
		# 		PosrangeX = float(checkpointlist[indexes][1]) + 1
		# 		NegrangeX = float(checkpointlist[indexes][1]) - 1
		# 		PosrangeY = float(checkpointlist[indexes][2]) + 1
		# 		NegrangeY = float(checkpointlist[indexes][2]) - 1
		# 		if ((randomRobotX<=PosrangeX) and (randomRobotX>=NegrangeX)) and ((randomRobotY>=NegrangeY) and (randomRobotY<=PosrangeY)):
		# 			print (_robot[num][0])
	for number in range(0, len(checkpointlist)):
		if experimentID==1:
			checkptStart = dateutil.parser.parse(checkpointlist[number][3]) + timedelta(seconds=5)
			checkptEnd = dateutil.parser.parse(checkpointlist[number][4])
		else:
			checkptStart = dateutil.parser.parse(checkpointlist[number][5])
			checkptEnd = dateutil.parser.parse(checkpointlist[number][6])
		# for num in range(0, len(_robot)):
		# 	robotTime = dateutil.parser.parse(_robot[num][0])
		# 	if robotTime>=checkptStart and robotTime<=checkptEnd:
		# 		robot_box.write(str(number+1) + "," + str(_robot[num][1]) + "," + str(_robot[num][2]) + "\n")
		for beacon in range(0, len(modifiedbeacon)):
			beaconTime = dateutil.parser.parse(modifiedbeacon[beacon][1])
			# beaconStart = dateutil.parser.parse(modifiedbeacon[beacon][5])
			# beaconEnd = dateutil.parser.parse(modifiedbeacon[beacon][6])
			if (beaconTime>=checkptStart and beaconTime<=checkptEnd):
				beacon_box.write(str(number+1) + "," + str(modifiedbeacon[beacon][0]) + ", " + str(modifiedbeacon[beacon][2]) + "," + str(modifiedbeacon[beacon][3]) + "\n")

# compileBoxplotList(beaconlist, beacon_boxplot, 1)
# compileBoxplotList(beaconlist2, beacon_boxplot2, 2)

# robo_boxplot.close()
# beacon_boxplot.close()
# robo_boxplot2.close()
# beacon_boxplot2.close()

def prepare_dict(dev, _mean, _variance):
	data = {}
	errdict = {	
			'Mean' : _mean,
			'Standard Deviation' : _variance
	}

	
	data['checkpoints'] = []
	data['value'] = []
	data['group-name'] = []

	for group, group_list in errdict.items():
		index = 0
		for item in group_list:
			# print dev[index]
			data['checkpoints'].append(dev[index])
			if _mean[index]!='No Mean':
				data['value'].append(item)
			else:
				data['value'].append(0)	
			data['group-name'].append(group)
			index += 1
	return data					

def prepare_dict2(checkpoint, _dev1, _dev2, _dev3, _dev4, _dev5, _dev6):
	data = {}
	errdict = {
			'Device 1': _dev1,
			'Device 2': _dev2,
			'Device 3': _dev3,
			'Device 4': _dev4,
			'Device 5': _dev5,
			'Device 6': _dev6
	}

	data['checkpoints'] = []
	data['value'] = []
	data['group-name'] = []

	for group, group_list in errdict.items():
		index = 0
		for item in group_list:
			data['checkpoints'].append(checkpoint[index])
			if item!='No Mean':
				data['value'].append(item)
			else:
				data['value'].append(0)	
			data['group-name'].append(group)
			index += 1
	return data					

checkpointNum = sorted(checkpointNum)
# print (checkpointNum)
# index = 0
# indexj = 0
# indexi = 0
# prevCount = 0
# roboCt = 0
# diff = 0
# tempX = []
# tempY = []
# tempX_avg = 0.0
# tempY_avg = 0.0
# pre_count = 0
# errorDist = 0
# errorDistance = 0
# errorVariance = 0
# tempDistance = 0
# tempVariance = 0
# temp_raw_x = []
# temp_raw_y = []
# robotMean_Variance = []
# beaconMean_Variance = []
# robot_reader = csv.reader(open("robot_boxplot.csv"), delimiter=",")
beacon_read = csv.reader(open("beacon_boxplot.csv"), delimiter=",")
# robot_reader2 = csv.reader(open("robot_boxplot2.csv"), delimiter=",")
# beacon_read2 = csv.reader(open("beacon_boxplot2.csv"), delimiter=",")
# next(robot_reader)
next(beacon_read)
# next(robot_reader2)
# next(beacon_read2)
# robotAcc = list(robot_reader)
def calculateRobotPos():
	robotIndex = 0
	curr = 0
	avgPosX = 0.0
	avgPosY = 0.0
	counter = 0
	while(robotIndex!=len(robotAcc)-1):
		avgPosX = int(robotAcc[robotIndex][1])
		avgPosY = int(robotAcc[robotIndex][2])
		if (curr==1):
			avgPosX += float(robotAcc[robotIndex][1])
			avgPosY += float(robotAcc[robotIndex][2])
			counter += 1 
		robotIndex += 1	
	avgPosX /= counter
	avgPosY /= counter
	print (float("{0:.3f}".format(float(avgPosX))))
	print (float("{0:.3f}".format(float(avgPosY))))
# calculateRobotPos()	
beaconAcc = list(beacon_read)
# print (beaconAcc)
for j in range(0, len(beaconAcc)):
	# if beaconAcc[j][1] not in devicelist:
	# deviceIndex = beaconAcc[j][1].split('b')
	if int(beaconAcc[j][1]) not in devicelist:
		devicelist.append(int(beaconAcc[j][1]))
devicelist = sorted(devicelist)
# print (devicelist)
# # robotAcc2 = list(robot_reader2)
# beaconAcc2 = list(beacon_read2)
# for i in range(0, len(robotAcc)):
# 	robotDev.append(int(robotAcc[i][0]))
# 	robotLng.append(float(robotAcc[i][1]))
# 	robotLat.append(float(robotAcc[i][2]))
# for i2 in range(0, len(robotAcc2)):
# 	robotDev2.append(int(robotAcc2[i2][0]))
# 	robotLng2.append(float(robotAcc2[i2][1]))
# 	robotLat2.append(float(robotAcc2[i2][2]))	
# while indexi != len(robotAcc):
# 	strChkpt = int(robotAcc[indexi][0])
# 	if indexi==0:
# 		if strChkpt==checkpointNum[index]:
# 			currentChkpt = strChkpt
# 			index += 1
	# if (strChkpt==currentChkpt) and (strChkpt==20):
	# 	tempX.append(float(robotAcc[indexi][1])) 
	# 	tempY.append(float(robotAcc[indexi][2]))
	# 	for checkpointindex in range(0, len(checkpointlist)):
	# 		if currentChkpt==int(checkpointlist[checkpointindex][0]):
	# 			tempDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(robotAcc[indexi][1])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(robotAcc[indexi][2]),2)))
	# 	pre_count += 1
	# if 	(strChkpt==currentChkpt) or (indexi==len(robotAcc)-1):
	# 	robotX_avg += float(robotAcc[indexi][1])
	# 	robotY_avg += float(robotAcc[indexi][2])
	# 	temp_raw_x.append(float(robotAcc[indexi][1]))
	# 	temp_raw_y.append(float(robotAcc[indexi][2]))
	# 	for checkpointindex in range(0, len(checkpointlist)):
	# 		if currentChkpt==int(checkpointlist[checkpointindex][0]):
	# 			errorDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(robotAcc[indexi][1])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(robotAcc[indexi][2]),2)))
	# 	roboCt += 1
	# 	if indexi==len(robotAcc)-1:
	# 		robotX_avg /= (roboCt)
	# 		robotY_avg /= (roboCt)
	# 		errorDistance /= roboCt
	# 		for numValues in range(0, roboCt):
	# 			errorVariance += math.sqrt((pow((temp_raw_x[numValues]-errorDistance),2) + pow((temp_raw_y[numValues]-errorDistance),2)))
	# 			if numValues==roboCt-1:
	# 				errorVariance /= roboCt
	# 				errorVariance = math.sqrt(errorVariance)
	# 		temp_raw_x = []
	# 		temp_raw_y = []
	# 		strStored = str(currentChkpt) + ", " + str(robotX_avg) + ", " + str(robotY_avg)
	# 		strMean_Variance = str(currentChkpt) + ", " + str(errorDistance) + ", " + str(errorVariance)
	# 		robotMean_Variance.append(strMean_Variance.split(", "))
	# 		robotOverall.append(strStored.split(", "))
	# 		index = 0
	# 		prevCount = 0
			# if currentChkpt==33:
			# 	print (errorDistance)
			# 	print (errorVariance)
			# errorDistance = 0
			# errorVariance = 0
			# break

	# else:
	# 	diff = strChkpt - currentChkpt
	# 	if (robotX_avg==0.0 and robotY_avg==0.0) and (diff==1):
	# 		robotX_avg = float(robotAcc[indexi-1][1])
	# 		robotY_avg = float(robotAcc[indexi-1][2])
	# 		roboCt = 1
	# 	robotX_avg /= (roboCt)
	# 	robotY_avg /= (roboCt)
	# 	errorDistance /= roboCt
	# 	for numValues in range(0, roboCt):
	# 		errorVariance += math.sqrt((pow((temp_raw_x[numValues]-errorDistance),2) + pow((temp_raw_y[numValues]-errorDistance),2)))
	# 		if numValues==roboCt-1:
	# 			errorVariance /= roboCt
	# 			errorVariance = math.sqrt(errorVariance)
		# if currentChkpt==20:
		# 	print (errorDistance)
		# 	print (errorVariance)
	# 	temp_raw_x = []
	# 	temp_raw_y = []
	# 	strStored = str(currentChkpt) + ", " + str(robotX_avg) + ", " + str(robotY_avg)
	# 	strMean_Variance = str(currentChkpt) + ", " + str(errorDistance) + ", " + str(errorVariance)
	# 	robotMean_Variance.append(strMean_Variance.split(", "))
	# 	robotOverall.append(strStored.split(", "))

	# 	if strChkpt==checkpointNum[index]:
	# 		currentChkpt = strChkpt
	# 		prevCount = i
	# 		index += 1
	# 		robotX_avg = 0.0
	# 		robotY_avg = 0.0
	# 		indexi -= 1
	# 		roboCt = 0
	# 		errorDistance = 0
	# 		errorVariance = 0
	# indexi += 1
def CalculateBeaconError(_BeaconAcc):
	index = 0
	indexj = 0
	# indexi = 0
	prevCount = 0
	devDiff = 0
	# roboCt = 0
	diff = 0
	tempX = []
	tempY = []
	tempCheck = []
	tempDist = []
	tempError = []
	tempX_avg = 0.0
	tempY_avg = 0.0
	pre_count = 0
	errorDist = 0
	errorDistance = 0.0
	errorVariance = 0.0
	tempDistance = 0
	tempVariance = 0
	temp_raw_x = []
	temp_raw_y = []
	rawError = []
	count = 0
	beaconX_avg = 0.0
	beaconY_avg = 0.0
	deviceID = 0
	nextID = 0
	indexID = 0
	devIndex = 0
	indexCt = 1
	# robotMean_Variance = []
	beaconMean_Variance = []
	tempList = []
	for check in range(0, len(checkpointNum)):
		for beaDev in range(0, len(devicelist)):
			tempList.append(checkpointNum[check])
			tempList.append(devicelist[beaDev])
			tempList.append(0)
			tempList.append(0)
			# print (tempList)
			beaconMean_Variance.append(tempList)
			tempList = []
	# print (beaconMean_Variance[20][0])
	for index in range(0, len(beaconMean_Variance)):
		# print (beaconMean_Variance[index][0])
		while indexj!=len(_BeaconAcc):
			if beaconMean_Variance[index][0] == int(_BeaconAcc[indexj][0]):
				if beaconMean_Variance[index][1] == int(_BeaconAcc[indexj][1]):
					beaconX_avg += float(_BeaconAcc[indexj][2])
					beaconY_avg += float(_BeaconAcc[indexj][3])
					temp_raw_x.append(float(_BeaconAcc[indexj][2]))
					temp_raw_y.append(float(_BeaconAcc[indexj][3]))
					for checkpointindex in range(0, len(checkpointlist)):
						if beaconMean_Variance[index][0]==int(checkpointlist[checkpointindex][0]):
							# errorDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][3]),2)))
							errorDistance += math.sqrt((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][2]))**2 + ((float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][3]))**2))
							rawError.append(math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][3]),2))))
					count += 1
					if indexj != len(_BeaconAcc)-1:
						if beaconMean_Variance[index][1] != int(_BeaconAcc[indexj+1][1]):
							break
			indexj += 1
		indexj = 0
		if count>1:
			beaconX_avg /= (count)
			beaconY_avg /= (count)
			errorDistance /= count
			for numValues in range(0, count):
				errorVariance += pow((rawError[numValues]-errorDistance),2)
				if numValues==count-1:
					errorVariance /= count
					errorVariance = math.sqrt(errorVariance)
			beaconMean_Variance[index][2] = errorDistance * map_scale
			beaconMean_Variance[index][3] = errorVariance * map_scale
		elif count==1:
			beaconMean_Variance[index][2] = errorDistance * map_scale
			beaconMean_Variance[index][3] = 0
		else:
			beaconMean_Variance[index][2] = "No Mean"
			beaconMean_Variance[index][3] = "No Variance"
		# if beaconMean_Variance[index][0] == 3 and beaconMean_Variance[index][1] == 1:
		# 	print (rawError)
		errorDistance = 0
		errorVariance = 0
		count = 0
	return beaconMean_Variance

	# print (beaconMean_Variance)
	# deviceID = int(_BeaconAcc[0][1])
	# nextID = int(_BeaconAcc[1][1])
	# for j in range(0, len(_BeaconAcc)):
	# 	beaconDev.append(int(_BeaconAcc[j][0]))
	# 	beaconLng.append(float(_BeaconAcc[j][1]))
	# 	beaconLat.append(float(_BeaconAcc[j][2]))
	# while indexj!=len(_BeaconAcc):

# 		strChkpt = int(_BeaconAcc[indexj][0])
# 		print ("deviceID: " + str(deviceID))
# 		if indexj==0:
# 			if strChkpt==checkpointNum[index]:
# 				currentChkpt = strChkpt
# 				index += 1
# 			else:
# 				for numDev in  range(0, len(devicelist)):
# 					strMean_Variance = str(checkpointNum[index]) + ", " + str(devicelist[numDev]) + ", No Mean, No Variance"
# 					print (strMean_Variance)
# 					beaconMean_Variance.append(strMean_Variance.split(", "))
# 				currentChkpt = strChkpt
# 				print (currentChkpt)
# 				index += 2
# # 		if (currentChkpt==2) and (deviceID==3):
# # 			tempX.append(float(_BeaconAcc[indexj + indexID][1])) 
# # 			tempY.append(float(_BeaconAcc[indexj + indexID][2]))
# # 			print (tempX)
# # 			print (tempY)
# # 			for checkpointindex in range(0, len(checkpointlist)):
# # 				if currentChkpt==int(checkpointlist[checkpointindex][0]):
# # 					# print (checkpointlist[checkpointindex])
# # 					# print (float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][1]))
# # 					# print (float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][2]))
# # 					tempDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][1])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][2]),2)))
# # 					# print (tempDistance)
# # 			pre_count += 1
# 		while 	(strChkpt==currentChkpt) or ((indexj+indexID)==len(_BeaconAcc)-1): #for the same checkpoint
# 			print ("Current: " + str(currentChkpt))
# 			# print ((indexj+indexID)==len(_BeaconAcc)-1)
# 			if (indexj+indexID)==len(_BeaconAcc)-1:
# 				beaconX_avg += float(_BeaconAcc[indexj + indexID][2])
# 				beaconY_avg += float(_BeaconAcc[indexj + indexID][3])
# 				temp_raw_x.append(float(_BeaconAcc[indexj + indexID][2]))
# 				temp_raw_y.append(float(_BeaconAcc[indexj + indexID][3]))
# 				for checkpointindex in range(0, len(checkpointlist)):
# 					if currentChkpt==int(checkpointlist[checkpointindex][0]):
# 						errorDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2)))
# 						rawError.append(math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2))))
# 				count += 1
# 				indexj += indexID
# 				# print (indexj)
# 				beaconX_avg /= (count)
# 				beaconY_avg /= (count)
# 				errorDistance /= count
# 				for numValues in range(0, count):
# 					errorVariance += pow((rawError[numValues]-errorDistance),2)
# 					if numValues==count-1:
# 						errorVariance /= count
# 						errorVariance = math.sqrt(errorVariance)
# 				# if (currentChkpt==33) and (deviceID==306):
# 				# 	print (temp_raw_x)
# 				# 	print (temp_raw_y)
# 				rawError = []
# 				# temp_raw_x = []
# 				# temp_raw_y = []
# 				strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
# 				beaconMean_Variance.append(strMean_Variance.split(", "))
# 				errorVariance = 0
# 				errorDistance = 0
# 				count = 0
# 				# print (pre_count)
# 				# print (tempDistance)
# # 				tempDistance /= (pre_count)
# # 				for numValue in range(0, pre_count):
# # 					tempVariance += pow((tempError[numValue]-tempDistance),2)
# 				# 	# tempVariance += (pow((tempX[numValue]-tempDistance),2) + pow((tempY[numValue]-tempDistance),2))
# # 					if numValue==pre_count-1:
# # 						tempVariance /= pre_count
# # 						tempVariance = math.sqrt(tempVariance)
# 				# # tempY_avg = tempY/(pre_count)
# # 				print (tempDistance)
# # 				print (tempVariance)
# # 				tempDistance = 0
# # 				tempVariance = 0
# 				return beaconMean_Variance
# 			# print (indexj)
			
# 			# print (strChkpt)
# 			# indexID = indexj
# 			# print (indexID)
# 			# print (indexj)
# 			# if currentChkpt==strChkpt:
# 			# 	print (currentChkpt)
# 			if (indexj+indexID)==0:
# 				nextID = int(_BeaconAcc[indexj][1])
# 				print (nextID)
# 				print (_BeaconAcc[indexj])
# 				if nextID!=devicelist[devIndex]:
# 					print (devicelist[0])
# 					devDiff = nextID - devicelist[0]
# 				else:
# 					devDiff = 0	
# 				# print (devDiff)
# 				# for find in range(0, len(devicelist)):
# 				# 	if (devicelist[find]==deviceID) and (find!=len(devicelist)-1):
# 				# 		devIndex = find + 1
# 				# 	elif (devicelist[find]==deviceID) and (find==len(devicelist)-1):
# 				# 		devIndex = 0	
# 				if devDiff==1:
# 					strMean_Variance = str(currentChkpt) + ", " + str(devicelist[devIndex]) + ", No Mean, No Variance"
# 					print (strMean_Variance)
# 					beaconMean_Variance.append(strMean_Variance.split(", "))
# 					devIndex += 2
# 					deviceID = nextID
# 				elif devDiff>=2:
# 					while devDiff!=0:
						
# 						strMean_Variance = str(currentChkpt) + ", " + str(devicelist[devIndex]) + ", No Mean, No Variance"
# 						print (strMean_Variance)
# 						beaconMean_Variance.append(strMean_Variance.split(", "))
# 						if devIndex != len(devicelist)-1:
# 							devIndex += 1
# 						else:
# 							devIndex = 0	
# 						# deviceID += 1
# 						devDiff -= 1
# 					devIndex += 1
# 					deviceID = nextID
# 				devDiff = 0
# 				indexID += 1
# 				nextID = int(_BeaconAcc[indexj+indexID][1])
# 			else:
# 				if indexID==0:
# 					nextID = int(_BeaconAcc[indexj][1])
# 					# print ("Initial: " + str(nextID) + ", " + str(indexj))
# 					# print ("Actual: " + str(deviceID) + ", " + str(indexj))
# 					# print (nextID==devicelist[devIndex])
# 					if nextID==devicelist[devIndex]:
# 						deviceID = nextID
# 						devIndex += 1
# 						nextID = int(_BeaconAcc[indexj+1][1])
# 					else:
# 						# print (devDiff)
# 						for find in range(0, len(devicelist)):
# 							if (devicelist[find]==deviceID) and (find!=len(devicelist)-1):
# 								devIndex = find + 1
# 							elif (devicelist[find]==deviceID) and (find==len(devicelist)-1):
# 								devIndex = 0	
# 						if devDiff==1:
# 							strMean_Variance = str(currentChkpt) + ", " + str(devicelist[devIndex]) + ", No Mean, No Variance"
# 							beaconMean_Variance.append(strMean_Variance.split(", "))
# 							devIndex += 2
# 							deviceID = nextID
# 							beaconX_avg = 0.0
# 							beaconY_avg = 0.0
# 							indexID -= 1
# 							count = 0
# 							errorDistance = 0
# 							errorVariance = 0
# 						elif devDiff>=2:
# 							while devDiff!=0:
								
# 								strMean_Variance = str(currentChkpt) + ", " + str(devicelist[devIndex]) + ", No Mean, No Variance"
# 								beaconMean_Variance.append(strMean_Variance.split(", "))
# 								if devIndex != len(devicelist)-1:
# 									devIndex += 1
# 								else:
# 									devIndex = 0	
# 								# deviceID += 1
# 								devDiff -= 1
# 							devIndex += 1
# 							beaconX_avg = 0.0
# 							beaconY_avg = 0.0
# 							deviceID = nextID
# 							indexID -= 1
# 							count = 0
# 							errorDistance = 0
# 							errorVariance = 0
# 						devDiff = 0
# 						# nextID = int(_BeaconAcc[indexj+indexID+1][1])
# 				else:
# # 					indexID += 1
# 					print ("Index: " + str(indexID))
# 					nextID = int(_BeaconAcc[indexj + indexID + 1][1])
# # 					indexID -= 1
# 				# print (deviceID)
# 				# print (nextID)
# 				# if (deviceID!=nextID) and (count==0): #for only one value of a device
# 				# 	beaconX_avg = float(_BeaconAcc[indexID][2])
# 				# 	beaconY_avg = float(_BeaconAcc[indexID][3])
# 				# 	temp_raw_x.append(float(_BeaconAcc[indexID][2]))
# 				# 	temp_raw_y.append(float(_BeaconAcc[indexID][3]))

# 				# 	for checkpointindex in range(0, len(checkpointlist)):
# 				# 		if currentChkpt==int(checkpointlist[checkpointindex][0]):
# 				# 			errorDistance = math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexID][3]),2)))
# 				# 	# count = 1
# 				# 	errorVariance = 0
# 				# 	temp_raw_x = []
# 				# 	temp_raw_y = []
# 				# 	indexj = indexID
# 				# 	# count = 0
# 				# 	strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
# 				# 	beaconMean_Variance.append(strMean_Variance.split(", "))
				
# 			if (deviceID==nextID): #for multiple values of a device
# 				print (indexID + indexj)
# 				# if (strChkpt==currentChkpt) and (currentChkpt==23) and (deviceID==nextID) and (deviceID==301):
# 				# 	# tempX.append(float(_BeaconAcc[indexj + indexID][2])) 
# 				# 	# tempY.append(float(_BeaconAcc[indexj + indexID][3]))
# 				# 	# print (tempX)
# 				# 	# print (tempY)
# 				# 	for checkpointindex in range(0, len(checkpointlist)):
# 				# 		if currentChkpt==int(checkpointlist[checkpointindex][0]):
# 				# 			# print (checkpointlist[checkpointindex])
# 				# 			# print (float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][1]))
# 				# 			# print (float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][2]))
# 				# 			tempDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2)))
# 				# 			tempError.append(math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2))))
# 				# 			# print (tempError)
# 				# 	pre_count += 1
# 				beaconX_avg += float(_BeaconAcc[indexj + indexID][2])
# 				beaconY_avg += float(_BeaconAcc[indexj + indexID][3])
# 				temp_raw_x.append(float(_BeaconAcc[indexj + indexID][2]))
# 				temp_raw_y.append(float(_BeaconAcc[indexj + indexID][3]))
# 				# if (currentChkpt==2) and (deviceID==3):
# 				# 	print (temp_raw_x)
# 				# 	print (temp_raw_y)
# 				for checkpointindex in range(0, len(checkpointlist)):
# 					if currentChkpt==int(checkpointlist[checkpointindex][0]):
# 						errorDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2)))
# 						rawError.append(math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2))))
# 						break
# 				count += 1
# 				# print (count)
# 				# indexj + indexID += 1
# 				# if currentChkpt==1 and deviceID==306:
# 				# 	print (devIndex==len(devicelist))
# 				# 	print (len(temp_raw_x))
# 				# 	print (len(temp_raw_y))
# 				# nextID = int(_BeaconAcc[indexj + indexID][1])
# 				# print (devIndex)
# 				# if devIndex==len(devicelist):
# 				# 	beaconX_avg /= (count)
# 				# 	beaconY_avg /= (count)
# 				# 	errorDistance /= count
# 				# 	for numValues in range(0, count):
# 				# 		errorVariance += math.sqrt((pow((temp_raw_x[numValues]-errorDistance),2) + pow((temp_raw_y[numValues]-errorDistance),2)))
# 				# 		if numValues==count-1:
# 				# 			errorVariance /= count
# 				# 			errorVariance = math.sqrt(errorVariance)
# 				# 	temp_raw_x = []
# 				# 	temp_raw_y = []
# 				# 	strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
# 				# 	beaconMean_Variance.append(strMean_Variance.split(", "))
# 				# 	errorVariance = 0
# 				# 	errorDistance = 0
# 				# 	count = 0
# 				# 	devIndex = 0
# 				# 	break	
# 			else:	#once hit a different device but still within same checkpoint
# 				# print (_BeaconAcc[indexj + indexID][2])
# 				# print(currentChkpt==strChkpt)
# 				# print (count)
# 				if count!=0:
# 					beaconX_avg += float(_BeaconAcc[indexj + indexID-1][2])
# 					beaconY_avg += float(_BeaconAcc[indexj + indexID-1][3])
# 					temp_raw_x.append(float(_BeaconAcc[indexj + indexID-1][2]))
# 					temp_raw_y.append(float(_BeaconAcc[indexj + indexID-1][3]))
# 					for checkpointindex in range(0, len(checkpointlist)):
# 						if currentChkpt==int(checkpointlist[checkpointindex][0]):
# 							errorDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2)))
# 							rawError.append(math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj + indexID][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj + indexID][3]),2))))
# 							break
# 					count += 1
# 				if devDiff == 0:
# 					strChkpt = int(_BeaconAcc[indexj + indexID][0])
# 					if strChkpt==currentChkpt:
# 						devDiff = nextID - deviceID
# 					else:
# 						devDiff = abs((devicelist[len(devicelist)-1] - deviceID) + (nextID - devicelist[0]) + 1)
# 				# print (devDiff)
# 				# print (beaconX_avg)
# 				if (beaconX_avg==0.0 and beaconY_avg==0.0) and (count==0):
# 					# print (float(_BeaconAcc[indexj + indexID-1][2]))
# 					print (indexj + indexID -1)
# 					beaconX_avg = float(_BeaconAcc[indexj + indexID-1][2])
# 					beaconY_avg = float(_BeaconAcc[indexj + indexID-1][3])
# 					temp_raw_x.append(float(_BeaconAcc[indexj + indexID-1][2]))
# 					temp_raw_y.append(float(_BeaconAcc[indexj + indexID-1][3]))
# 					for checkpointindex in range(0, len(checkpointlist)):
# 						if currentChkpt==int(checkpointlist[checkpointindex][0]):
# 							errorDistance = math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexID-1][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexID-1][3]),2)))
# 							rawError.append(errorDistance)
# 							break
# 					count = 1
# 				beaconX_avg /= (count)
# 				beaconY_avg /= (count)
# 				errorDistance /= count
# 				for numValues in range(0, count):
# 					errorVariance += pow((rawError[numValues]-errorDistance),2)
# 					if numValues==count-1:
# 						errorVariance /= count
# 						errorVariance = math.sqrt(errorVariance)
# 				# temp_raw_x = []
# 				# temp_raw_y = []
# 				rawError = []
# 				# strStored = str(currentChkpt) + ", " + str(beaconX_avg) + ", " + str(beaconY_avg)
# 				strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
# 				beaconMean_Variance.append(strMean_Variance.split(", "))
# 				errorVariance = 0
# 				errorDistance = 0
# 				count = 0
# 				if strChkpt!=currentChkpt:
# 					indexj += indexID
# 					indexID = -1
# 					devIndex = 0
# 					devDiff = 0
# 					beaconX_avg = 0
# 					beaconY_avg = 0
# 					currentChkpt = strChkpt
				

# 				# print (devicelist)
# 				# beaconOverall.append(strStored.split(", "))
# 				# print (currentChkpt)
# 				# print (deviceID)
# 				if devDiff==1:
# 					deviceID = nextID
# 					devIndex += 1
# 					beaconX_avg = 0.0
# 					beaconY_avg = 0.0
# 					indexID -= 1
# 					errorDistance = 0
# 					errorVariance = 0
# 				if devDiff==2:
# 					strMean_Variance = str(currentChkpt) + ", " + str(deviceID+1) + ", No Mean, No Variance"
# 					beaconMean_Variance.append(strMean_Variance.split(", "))
# 					devIndex += 2
# 					deviceID = nextID
# 					beaconX_avg = 0.0
# 					beaconY_avg = 0.0
# 					indexID -= 1
# 					count = 0
# 					errorDistance = 0
# 					errorVariance = 0
# 				elif devDiff>2:
# 					while devDiff!=1:
						
# 						strMean_Variance = str(currentChkpt) + ", " + str(deviceID+indexCt) + ", No Mean, No Variance"
# 						beaconMean_Variance.append(strMean_Variance.split(", "))
# 						devIndex += 1
# 						# deviceID += 1
# 						indexCt += 1
# 						devDiff -= 1
# 					devIndex += 1
# 					beaconX_avg = 0.0
# 					beaconY_avg = 0.0
# 					deviceID = nextID
# 					indexID -= 1
# 					count = 0
# 					errorDistance = 0
# 					errorVariance = 0
# 				devDiff = 0
# 			indexID += 1
# 			strChkpt = int(_BeaconAcc[indexj + indexID][0])
# 			print (temp_raw_x)
# 			print (beaconMean_Variance)
		# if (strChkpt==currentChkpt) and (currentChkpt==1) and (deviceID==nextID) and (deviceID==301):
		# 	print (pre_count)
		# 	tempDistance /= (pre_count)
		# 	for numValue in range(0, pre_count):
		# 		print (tempX[numValue])
		# 		print (tempDistance)
		# 		tempVariance += math.sqrt((pow((tempX[numValue]-tempDistance),2) + pow((tempY[numValue]-tempDistance),2)))
		# 		if numValue==pre_count-1:
		# 			tempVariance /= pre_count
		# 			tempVariance = math.sqrt(tempVariance)
			# tempY_avg = tempY/(pre_count)
			# print (tempDistance)
			# print (tempVariance)
			
		# print (strChkpt!=currentChkpt)
			
					
			# if indexj==len(_BeaconAcc)-1: #for last entry
			# 	print (count)
				# deviceID = int(_BeaconAcc[indexID][1])
				# nextID = int(_BeaconAcc[indexj][1])
				# indexID = indexj
				# if (deviceID!=nextID) and (count==0): #for only one value of a device
				# 	beaconX_avg = float(_BeaconAcc[indexj][2])
				# 	beaconY_avg = float(_BeaconAcc[indexj][3])
				# 	temp_raw_x.append(float(_BeaconAcc[indexj][2]))
				# 	temp_raw_y.append(float(_BeaconAcc[indexj][3]))

				# 	for checkpointindex in range(0, len(checkpointlist)):
				# 		if currentChkpt==int(checkpointlist[checkpointindex][0]):
				# 			errorDistance = math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][3]),2)))
				# 	count = 1
				# 	errorVariance = 0
				# 	temp_raw_x = []
				# 	temp_raw_y = []
				# 	# indexj = indexj
				# 	count = 0
				# 	strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
				# 	beaconMean_Variance.append(strMean_Variance.split(", "))
				# else:	#for multiple values of a device
				# 	if deviceID==nextID:
				# 		beaconX_avg += float(_BeaconAcc[indexj][2])
				# 		beaconY_avg += float(_BeaconAcc[indexj][3])
				# 		temp_raw_x.append(float(_BeaconAcc[indexj][2]))
				# 		temp_raw_y.append(float(_BeaconAcc[indexj][3]))
				# 		for checkpointindex in range(0, len(checkpointlist)):
				# 			if currentChkpt==int(checkpointlist[checkpointindex][0]):
				# 				errorDistance += math.sqrt((pow((float(checkpointlist[checkpointindex][1])-float(_BeaconAcc[indexj][2])), 2) + pow(float(checkpointlist[checkpointindex][2])-float(_BeaconAcc[indexj][3]),2)))
				# 		count += 1
				# 		indexj += 1
				# 		if currentChkpt==2 and deviceID==301:
				# 			print (temp_raw_x)
				# 		nextID = int(_BeaconAcc[indexj][1])
				# 	else:	#once hit a different device but still within same checkpoint
				# beaconX_avg /= (count)
				# beaconY_avg /= (count)
				# errorDistance /= count
				# for numValues in range(0, count):
				# 	errorVariance += math.sqrt((pow((temp_raw_x[numValues]-errorDistance),2) + pow((temp_raw_y[numValues]-errorDistance),2)))
				# 	if numValues==count-1:
				# 		errorVariance /= count
				# 		errorVariance = math.sqrt(errorVariance)
				# temp_raw_x = []
				# temp_raw_y = []
				# # indexj = indexj
				# # strStored = str(currentChkpt) + ", " + str(beaconX_avg) + ", " + str(beaconY_avg)
				# strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
				# beaconMean_Variance.append(strMean_Variance.split(", "))
				# errorVariance = 0
				# errorDistance = 0
				# count = 0
				# beaconX_avg /= (count)
				# beaconY_avg /= (count)
				# errorDistance /= count
				# for numValues in range(0, count):
				# 	errorVariance += math.sqrt((pow((temp_raw_x[numValues]-errorDistance),2) + pow((temp_raw_y[numValues]-errorDistance),2)))
				# 	if numValues==count-1:
				# 		errorVariance /= count
				# 		errorVariance = math.sqrt(errorVariance)
				# temp_raw_x = []
				# temp_raw_y = []		
				# # strStored = str(currentChkpt) + ", " + str(beaconX_avg) + ", " + str(beaconY_avg)
				# strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
				# beaconMean_Variance.append(strMean_Variance.split(", "))
				# # beaconOverall.append(strStored.split(", "))
				# index = 0
				# prevCount = 0
				# errorDistance = 0
				# errorVariance = 0
				# break

# 		if (strChkpt!= currentChkpt) or ((indexj+indexID)!=len(_BeaconAcc)-1): #for different checkpoint
# 			# print (indexj + indexID)
# # 			beaconX_avg /= (count)
# # 			beaconY_avg /= (count)
# # 			errorDistance /= count
# # 			for numValues in range(0, count):
# # 				errorVariance += pow((rawError[numValues]-errorDistance),2)
# # 				if numValues==count-1:
# # 					errorVariance /= count
# # 					errorVariance = math.sqrt(errorVariance)
# 			# temp_raw_x = []
# 			# temp_raw_y = []
# # 			rawError = []
# 			# strStored = str(currentChkpt) + ", " + str(beaconX_avg) + ", " + str(beaconY_avg)
# # 			strMean_Variance = str(currentChkpt) + ", " + str(deviceID) + ", " + str(errorDistance) + ", " + str(errorVariance)
# # 			beaconMean_Variance.append(strMean_Variance.split(", "))
# # 			errorVariance = 0
# # 			errorDistance = 0
# # 			count = 0
# 			# deviceID = int(_BeaconAcc[indexID][1])
# 			# nextID = int(_BeaconAcc[indexID+1][1])
			
# 			# print ("This is: " + str(nextID))
# 			# print ("That is: " + str(deviceID))
# 			diff = strChkpt - currentChkpt
# 			indexj += indexID
# 			indexID = 0
# 			devIndex = 0
# 			nextID = int(_BeaconAcc[indexj + indexID][1])
# 			# print (indexID)
# 			# print (indexj)
# 			# indexj = indexID
# 			devDiff = abs((devicelist[len(devicelist)-1] - deviceID) + (nextID - devicelist[0]))
# 			# if (beaconX_avg==0.0 and beaconY_avg==0.0) and (diff==1):
# 			# 	beaconX_avg = float(_BeaconAcc[indexj-1][1])
# 			# 	beaconY_avg = float(_BeaconAcc[indexj-1][2])
# 			# 	count = 1
# 			# beaconX_avg /= (count)
# 			# beaconY_avg /= (count)
# 			# errorDistance /= count
# 			# for numValues in range(0, count):
# 			# 	errorVariance += math.sqrt((pow((temp_raw_x[numValues]-errorDistance),2) + pow((temp_raw_y[numValues]-errorDistance),2)))
# 			# 	if numValues==count-1:
# 			# 		errorVariance /= count
# 			# 		errorVariance = math.sqrt(errorVariance)
# 			# if currentChkpt==1:
# 			# 	print (errorDistance)
# 			# 	print (errorVariance)
# 			# temp_raw_x = []
# 			# temp_raw_y = []		
# 			# strStored = str(currentChkpt) + ", " + str(beaconX_avg) + ", " + str(beaconY_avg)
# 			# strMean_Variance = str(currentChkpt) + ", " + str(errorDistance) + ", " + str(errorVariance)
# 			# beaconMean_Variance.append(strMean_Variance.split(", "))
# 			# beaconOverall.append(strStored.split(", "))

# 			if strChkpt==checkpointNum[index]:
# 				currentChkpt = strChkpt
# 				deviceID = nextID
# 				# prevCount = j
# 				index += 1
# 				beaconX_avg = 0.0
# 				beaconY_avg = 0.0
# 				indexj -= 1
# 				# count = 0
# 				errorDistance = 0
# 				errorVariance = 0

# 			elif diff == 2:
# 				# strStored = str(checkpointNum[index]) + ", Empty"
# 				for k in range(0, len(devicelist)):
# 					strMean_Variance = str(checkpointNum[index]) + ", " + str(devicelist[k]) + ", No Mean, No Variance"
# 					beaconMean_Variance.append(strMean_Variance.split(", "))
# 				# beaconOverall.append(strStored.split(", "))
# 				index += 2
# 				currentChkpt = strChkpt
# 				deviceID = nextID
# 				# prevCount = j
# 				beaconX_avg = 0.0
# 				beaconY_avg = 0.0
# 				indexj -= 1
# 				count = 0
# 				errorDistance = 0
# 				errorVariance = 0

# 			elif diff>2:
# 				while currentChkpt!=strChkpt-1:
# 					# strStored = str(checkpointNum[index]) + ", Empty"
# 					for missing in range(0, len(devicelist)):
# 						strMean_Variance = str(checkpointNum[index]) + ", " + str(devicelist[missing]) + ", No Mean, No Variance"
# 						beaconMean_Variance.append(strMean_Variance.split(", "))
# 					# beaconOverall.append(strStored.split(", "))
# 					index += 1
# 					currentChkpt += 1
# 				index += 1	
# 				beaconX_avg = 0.0
# 				beaconY_avg = 0.0
# 				currentChkpt = strChkpt
# 				deviceID = nextID
# 				# prevCount = j
# 				indexj -= 1	
# 				count = 0
# 				errorDistance = 0
# 				errorVariance = 0
# 		indexj += 1
	# return beaconMean_Variance
	# print (pre_count)			
	# tempDistance /= (pre_count)
	# for numValue in range(0, pre_count):
	# 	tempVariance += math.sqrt((pow((tempX[numValue]-tempDistance),2) + pow((tempY[numValue]-tempDistance),2)))
	# 	if numValue==pre_count-1:
	# 		tempVariance /= pre_count
	# 		tempVariance = math.sqrt(tempVariance)
	# # tempY_avg = tempY/(pre_count)
	# print (tempDistance)
	# print (tempVariance)
	# print (beaconOverall)
	# roboterrorX = 0
	# roboterrorY = 0
	
beaconData = CalculateBeaconError(beaconAcc)
# beaconData2 = CalculateBeaconError(beaconAcc2)
# print (beaconData)

# beaconerrorX = 0
# beaconerrorY = 0
# errorX = 0
# errorY = 0
bMean1 = []
bVar1 = []
bMean2 = []
bVar2 = []
bMean3 = []
bVar3 = []
bMean4 = []
bVar4 = []
bMean5 = []
bVar5 = []
bMean6 = []
bVar6 = []
# robotMean = []
# robotVariance = []
def compilingResults(_beaconData, _beaconDev):
	beaconMean = []
	# beaconMean2 = []
	beaconVariance = []
	# beaconVariance2 = []
	beaconLabel = []
	# for upgrade in range(0, len(checkpointlist)):
		# checkpointlist[upgrade][1] = float(checkpointlist[upgrade][1]) * float(map_scale)
		# checkpointlist[upgrade][2] = float(checkpointlist[upgrade][2]) * float(map_scale)
	for checkpoints in range(0, len(_beaconData)):
		# if _beaconData[checkpoints][2]!='No Mean':
		# 	_beaconData[checkpoints][2] = float(_beaconData[checkpoints][2]) * float(map_scale)
		# 	_beaconData[checkpoints][3] = float(_beaconData[checkpoints][3]) * float(map_scale)
		if _beaconData[checkpoints][1]==_beaconDev:
			if _beaconData[checkpoints][2]!='No Mean':
				beaconMean.append(float(_beaconData[checkpoints][2]))
				beaconVariance.append(float(_beaconData[checkpoints][3]))
				# beaconLabel.append(float("{0:.3f}".format(float(_beaconData[checkpoints][2]))))
			elif _beaconData[checkpoints][2]=='No Mean':
				beaconMean.append(_beaconData[checkpoints][2])
				beaconVariance.append(_beaconData[checkpoints][3])
				# beaconLabel.append(_beaconData[checkpoints][2])
			# if _beaconData2[checkpoints][1]==str(_beaconDev):	
			# 	if beaconData2[checkpoints][2]!='No Mean':
			# 		beaconMean2.append(float(beaconData2[checkpoints][2]))
			# 		beaconVariance2.append(float(beaconData2[checkpoints][3]))
			# 	elif beaconData2[checkpoints][2]=='No Mean':
			# 		beaconMean2.append(beaconData2[checkpoints][2])
			# 		beaconVariance2.append(beaconData2[checkpoints][3])
			# print (checkpoints)
			# if _beaconDev!=6:
				# checkpointIndexs = checkpointNum.index(checkpoints+1)
				# print (checkpointIndexs)
			for search in range(0, len(checkpointlist)):

				if checkpointlist[search][0]==str(_beaconData[checkpoints][0]):
					# print (_beaconData[checkpoints][0])
					beaconheat.write(str(checkpointlist[search][0]) + ", " + str(checkpointlist[search][1]) + ", " + str(checkpointlist[search][2]) + ", " + str("b" + str(_beaconDev)) + ", " + str(beaconData[checkpoints][2]) + ", " + str(beaconData[checkpoints][3]) + "\n")
			# else:
			# 	for search in range(0, len(checkpointlist)):
			# 		if checkpointlist[search][0]==str(_beaconData[checkpoints][0]):
			# 			beaconheat.write(str(checkpointlist[search][0]) + ", " + str(checkpointlist[search][1]) + ", " + str(checkpointlist[search][2]) + ", " + str("b" + str(_beaconDev)) + ", " + str(beaconData[checkpoints][2]) + ", " + str(beaconData[checkpoints][3]))
	return beaconMean, beaconVariance
# bMean1, bVar1 = compilingResults(beaconData, 1)
# data_dict1 = prepare_dict(checkpointNum, bMean1, bVar1)
# bMean2, bVar2 = compilingResults(beaconData, 2)
# data_dict2 = prepare_dict(checkpointNum, bMean2, bVar2)
# bMean3, bVar3 = compilingResults(beaconData, 3)
# data_dict3 = prepare_dict(checkpointNum, bMean3, bVar3)
# bMean4, bVar4 = compilingResults(beaconData, 4)
# data_dict4 = prepare_dict(checkpointNum, bMean4, bVar4)
# bMean5, bVar5 = compilingResults(beaconData, 5)
# data_dict5 = prepare_dict(checkpointNum, bMean5, bVar5)
bMean6, bVar6 = compilingResults(beaconData, 6)
# data_dict6 = prepare_dict(checkpointNum, bMean6, bVar6)
# data_dict_compiled = prepare_dict2(checkpointNum, bMean1, bMean2, bMean3, bMean4, bMean5, bMean6)

# source_Mean = ColumnDataSource(data=dict(x=checkpointNum,
# 										y=beaconLabel,
# 										value=beaconLabel))

# hover1 = HoverTool(tooltips=[
#     ("Checkpoint", "$x"),
#     ("Beacon Error", "$y"),
# ])

# hover2 = HoverTool(tooltips=[
#     ("Checkpoint", "$x"),
#     ("Beacon Error", "$y"),
# ])

# hover3 = HoverTool(tooltips=[
#     ("Checkpoint", "$x"),
#     ("Beacon Error", "$y"),
# ])

# hover4 = HoverTool(tooltips=[
#     ("Checkpoint", "$x"),
#     ("Beacon Error", "$y"),
# ])

# hover5 = HoverTool(tooltips=[
#     ("Checkpoint", "$x"),
#     ("Beacon Error", "$y"),
# ])

# hover6 = HoverTool(tooltips=[
#     ("Checkpoint", "$x"),
#     ("Beacon Error", "$y"),
# ])

# hover7 = HoverTool(tooltips=[
#     ("Checkpoint", "$x"),
#     ("Beacon Error", "$y"),
# ])
# print (beaconMean2)

# # print (robotMean_Variance)
# for checkpoints_robot in range(0, len(robotMean_Variance)):
# 	if robotMean_Variance[checkpoints_robot][1]!='No Mean':
# 		robotMean.append(float(robotMean_Variance[checkpoints_robot][1]))
# 		robotVariance.append(float(robotMean_Variance[checkpoints_robot][2]))
# 	else:
# 		robotMean.append(robotMean_Variance[checkpoints_robot][1])
# 		robotVariance.append(robotMean_Variance[checkpoints_robot][2])	
# 	# print (checkpoints_robot)
	# if checkpoints_robot!=len(robotMean_Variance)-1:
# 		# robotcheckpointIndex = checkpointNum.index(checkpoints_robot+1)
	# 	for searchrobo in range(0, len(checkpointlist)):
	# 		if checkpointlist[searchrobo][0]==str(checkpoints_robot+1):
	# 			robo_heatmap.write(str(checkpointlist[searchrobo][0]) + ", " + str(checkpointlist[searchrobo][1]) + ", " + str(checkpointlist[searchrobo][2]) + ", " + str(robotMean_Variance[checkpoints_robot][1]) + ", " + str(robotMean_Variance[checkpoints_robot][2]) + "\n")
	# else:
	# 	for searchrobo in range(0, len(checkpointlist)):
	# 		if checkpointlist[searchrobo][0]==str(checkpoints_robot+1):
	# 			robo_heatmap.write(str(checkpointlist[searchrobo][0]) + ", " + str(checkpointlist[searchrobo][1]) + ", " + str(checkpointlist[searchrobo][2]) + ", " + str(robotMean_Variance[checkpoints_robot][1]) + ", " + str(robotMean_Variance[checkpoints_robot][2]))
# print (beaconMean)
# print (beaconVariance)
# for subjects in range(0, len(checkpointNum)):
# 	for indexes in range(0, len(robotOverall)):
# 		if int(robotOverall[indexes][0])==checkpointNum[subjects]:
# 			roboterrorX = float(robotOverall[indexes][1])
# 			roboterrorY = float(robotOverall[indexes][2])
# 			break
# 	for h in range(0, len(beaconOverall)):
# 		if int(beaconOverall[h][0])==checkpointNum[subjects]:
# 			if beaconOverall[h][1]!='Empty':
# 				beaconerrorX = float(beaconOverall[indexes][1])
# 				beaconerrorY = float(beaconOverall[indexes][2])
# 			else:
# 				beaconerrorX = 'NA'
# 				beaconerrorY = beaconerrorX	
# 			break		

# 	if beaconerrorX!='NA' or beaconerrorY!='NA':
# 		errorDist = math.sqrt((pow((roboterrorX-beaconerrorX), 2) + pow((roboterrorY-beaconerrorY),2)))
# 	else:
# 		errorDist = 'Not applicable'	

# 	if subjects!=len(checkpointNum)-1:
# 		heatmap_error.write(str(checkpointNum[subjects]) + ", " + str(errorDist) + "\n")
# 	else:
# 		heatmap_error.write(str(checkpointNum[subjects]) + ", " + str(errorDist))

# robot_box = {
# 				'Stations': robotDev,
# 				'x': robotLng,
# 				'y': robotLat
# }

# beacon_box = {
# 				'Stations': beaconDev,
# 				'x': beaconLng,
# 				'y': beaconLat
# }

# data_dict = prepare_dict(checkpointNum, beaconMean, beaconVariance)
# robo_data_dict = prepare_dict(checkpointNum, robotMean, robotVariance)
# robot_box2 = {
# 				'Stations': robotDev2,
# 				'x': robotLng2,
# 				'y': robotLat2
# }
# print (robotDev2)
# beacon_box2 = {
# 				'Stations': beaconDev2,
# 				'x': beaconLng2,
# 				'y': beaconLat2
# }

# output_file("MD6 Data Analytics.html")
# labels_mean_variance = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-30, y_offset=-6, source=source_Mean, render_mode='canvas')                  
# labels_mean_variance.text_color = 'black'  
# labels_mean_variance.text_font_style = 'italic' 
# hm12 = Bar(data_dict1, values='value', label='checkpoints', group='group-name', legend='top_left', title='Error Mean and Variance for Beacons b1', width = 1100, plot_height = 700, tools=[hover1])
# hm13 = Bar(data_dict2, values='value', label='checkpoints', group='group-name', legend='top_left', title='Error Mean and Variance for Beacons b2', width = 1100, plot_height = 700, tools=[hover2])
# hm14 = Bar(data_dict3, values='value', label='checkpoints', group='group-name', legend='top_left', title='Error Mean and Variance for Beacons b3', width = 1100, plot_height = 700, tools=[hover3])
# hm15 = Bar(data_dict4, values='value', label='checkpoints', group='group-name', legend='top_left', title='Error Mean and Variance for Beacons b4', width = 1100, plot_height = 700, tools=[hover4])
# hm16 = Bar(data_dict5, values='value', label='checkpoints', group='group-name', legend='top_left', title='Error Mean and Variance for Beacons b5', width = 1100, plot_height = 700, tools=[hover5])
# hm17 = Bar(data_dict6, values='value', label='checkpoints', group='group-name', legend='top_left', title='Error Mean and Variance for Beacons b6', width = 1100, plot_height = 700, tools=[hover6])
# hm13 = BoxPlot(robot_box, values='x', label='Stations', legend=False, title='Experiment1 Robot X-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm14 = BoxPlot(robot_box, values='y', label='Stations', legend=False, title='Experiment1 Robot Y-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm15 = BoxPlot(beacon_box, values='x', label='Stations', legend=False, title='Experiment1 Beacon X-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm16 = BoxPlot(beacon_box, values='y', label='Stations', legend=False, title='Experiment1 Beacon Y-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm18 = Bar(data_dict_compiled, values='value', label='checkpoints', group='group-name', legend='top_left', title='Error Mean and Variance for Robot Experiment 2', width = 1100, plot_height = 700, tools=[hover7])
# hm17 = BoxPlot(robot_box2, values='x', label='Stations', legend=False, title='Experiment2 Robot X-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm18 = BoxPlot(robot_box2, values='y', label='Stations', legend=False, title='Experiment2 Robot Y-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm19 = BoxPlot(beacon_box2, values='x', label='Stations', legend=False, title='Experiment2 Beacon X-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm20 = BoxPlot(beacon_box2, values='y', label='Stations', legend=False, title='Experiment2 Beacon Y-Values Error Distance Boxplot', width = 600, plot_height=600)
# hm12.add_layout(labels_mean_variance)

# show(hm12)
# l = layout([[hm12],
# 			[hm13],
# 			[hm14],
# 			[hm15],
# 			[hm16],
# 			[hm17],
# 			[hm18]])
# show(l)
# center = ward5_POI()

# query_ward5 = 'query{map (id:"ward5678") {image}}'
# query_coordinates = 'query{map (id:"ward5678") {coordinates}}'
# r = requests.get("http://137.132.165.139/graphql", {"query":query_ward5})
# s = requests.get("http://137.132.165.139/graphql", {"query":query_coordinates})
# coor = s.text
# cod = json.loads(coor)
# image = r.text
# img = json.loads(image)
# imgdata = base64.b64decode(img['data']['map']['image'])
# filename = 'ward5.png'
# with open(filename, 'wb') as f:
# 	f.write(imgdata)
# for i in range(0, len(cod['data']['map']['coordinates'])):
# 	temp = cod['data']['map']['coordinates'].split("],")
# for i in range(0, len(temp)):
# 	temp[i] = temp[i].split(",")
# 	for j in range(0, 2):
# 		while "[" in temp[i][j]:
# 			temp[i][j] = temp[i][j].strip("[")
# 		while "]" in temp[i][j]:
# 			temp[i][j] = temp[i][j].strip("]")	
# 	temp[i][0] = float(temp[i][0])*float(map_scale)
# 	temp[i][1] = float(temp[i][1])*float(map_scale)
# 	coord_lng_list.append(temp[i][0])
# 	coord_lat_list.append(temp[i][1])
# 	coord_total_list = coord_lng_list + coord_lat_list	
# min_pt, max_pt = findMinimum_Maximum(coord_total_list)
# min_x, max_x = findMinimum_Maximum(coord_lng_list)
# min_y, max_y = findMinimum_Maximum(coord_lat_list)

# p = figure(x_range=(min_pt, max_pt), y_range=(min_pt, max_pt))
# p.image_url(url=['https://image.ibb.co/eAuMNk/ward5.png'], x=min_x, y=min_y, w=(max_x - min_x), h=(max_y - min_y), anchor="bottom_left")
# # p.circle(18.0153163928,7.08397844299, size=15, color="red", alpha=0.5)
# # for index in range(0, len(checkpointlist)):
# # 	p.circle(float(checkpointlist[index][1]), float(checkpointlist[index][2]), size=15, color="red", alpha=0.5)
# p.axis.visible = False
# p.xgrid.grid_line_color = None
# p.xgrid.grid_line_color = None
# output_file('Checkpoints.html')
# show(p)