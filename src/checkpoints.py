import base64
import requests
# import urllib3
import json
from bokeh.charts import BoxPlot
from bokeh.layouts import row, layout
from bokeh.plotting import figure, show, output_file
from storePOI import office_POI, ward5_POI, actlab_POI
from storeScale import getScale
import csv, operator
from datetime import datetime
from bokeh.io import curdoc
from bokeh.models import HoverTool
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
beaconAcc = []
robotDev = []
beaconDev = []
checkpointNum = []
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
beaconX_avg = 0.0
beaconY_avg = 0.0
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
count = 0
timestamp = 0
mindiff = 0
robotLat = []
robotLng = []
beaconLat = []
modifiedbeacon = []
beaconLng = []
stations = 0

robo_boxplot = open('robot_boxplot.csv', 'w')
beacon_boxplot = open('beacon_boxplot.csv', 'w')
heatmap_error = open('heatmap_error.csv', 'w')
robo_boxplot.write("Checkpoint, RobotX, RobotY\n")
beacon_boxplot.write("Checkpoint, BeaconX, BeaconY\n")
heatmap_error.write("Checkpoint, ErrorDistance\n")
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

map_scale = getScale("ward5678")
reader = csv.reader(open("robot_path_experiment1.csv"), delimiter=",")
beacon_reader = csv.reader(open("beacon_path_experiment1.csv"), delimiter=",")
checkpoint_reader = csv.reader(open("Checkpoints.csv"), delimiter=",")
next(reader)
next(beacon_reader)
next(checkpoint_reader)
checkpointlist = sorted(checkpoint_reader, key=operator.itemgetter(0), reverse=False)
robotlist = sorted(reader, key=operator.itemgetter(0), reverse=False)
beaconlist = sorted(beacon_reader, key=operator.itemgetter(0, 5), reverse=False)
for item in range(0, len(beaconlist)):
	if beaconlist[item][3]==" ward5678":
		beaconlist[item][1] = float(beaconlist[item][1])*float(map_scale)
		beaconlist[item][2] = float(beaconlist[item][2])*float(map_scale)
		modifiedbeacon.append(beaconlist[item])
for num in range(0, len(robotlist)):
	robotlist[num][0] = datetime.fromtimestamp(int(robotlist[num][0])).strftime("%Y-%m-%d %H:%M:%S")
for number in range(0, len(checkpointlist)):
	checkpointNum.append(int(checkpointlist[number][0]))
	checkptStart = dateutil.parser.parse(checkpointlist[number][3])
	checkptEnd = dateutil.parser.parse(checkpointlist[number][4])
	for num in range(0, len(robotlist)):
		robotTime = dateutil.parser.parse(robotlist[num][0])
		if robotTime>=checkptStart and robotTime<=checkptEnd:
			robo_boxplot.write(str(number+1) + "," + str(robotlist[num][1]) + "," + str(robotlist[num][2]) + "\n")
	for beacon in range(0, len(modifiedbeacon)):
		beaconStart = dateutil.parser.parse(modifiedbeacon[beacon][5])
		beaconEnd = dateutil.parser.parse(modifiedbeacon[beacon][6])
		if ((beaconStart>=checkptStart and beaconEnd<=checkptEnd) or ((beaconStart>=checkptStart and beaconStart<=checkptEnd) and (beaconEnd>=checkptEnd))):
			beacon_boxplot.write(str(number+1) + "," + str(modifiedbeacon[beacon][2]) + "," + str(modifiedbeacon[beacon][1]) + "\n")
robo_boxplot.close()
beacon_boxplot.close()

checkpointNum = sorted(checkpointNum)
index = 0
indexj = 0
indexi = 0
prevCount = 0
roboCt = 0
diff = 0
tempX = 0.0
tempY = 0.0
tempX_avg = 0.0
tempY_avg = 0.0
pre_count = 0
robot_reader = csv.reader(open("robot_boxplot.csv"), delimiter=",")
beacon_read = csv.reader(open("beacon_boxplot.csv"), delimiter=",")
next(robot_reader)
next(beacon_read)
robotAcc = list(robot_reader)
beaconAcc = list(beacon_read)
for i in range(0, len(robotAcc)):
	robotDev.append(int(robotAcc[i][0]))
	robotLng.append(float(robotAcc[i][1]))
	robotLat.append(float(robotAcc[i][2]))
while indexi != len(robotAcc):
	strChkpt = int(robotAcc[indexi][0])
	if indexi==0:
		if strChkpt==checkpointNum[index]:
			currentChkpt = strChkpt
			index += 1
	# if (strChkpt==currentChkpt) and (strChkpt==1):
	# 	tempX += float(robotAcc[indexi][1])
	# 	tempY += float(robotAcc[indexi][2])
	# 	pre_count += 1
	if 	(strChkpt==currentChkpt) or (indexi==len(robotAcc)-1):
		robotX_avg += float(robotAcc[indexi][1])
		robotY_avg += float(robotAcc[indexi][2])
		roboCt += 1
		if indexi==len(robotAcc)-1:
			robotX_avg /= (roboCt)
			robotY_avg /= (roboCt)
			strStored = str(currentChkpt) + ", " + str(robotX_avg) + ", " + str(robotY_avg)
			robotOverall.append(strStored.split(", "))
			index = 0
			prevCount = 0
			break

	else:
		diff = strChkpt - currentChkpt
		if (robotX_avg==0.0 and robotY_avg==0.0) and (diff==1):
			robotX_avg = float(robotAcc[indexi-1][1])
			robotY_avg = float(robotAcc[indexi-1][2])
			count = 1
		robotX_avg /= (roboCt)
		robotY_avg /= (roboCt)
		strStored = str(currentChkpt) + ", " + str(robotX_avg) + ", " + str(robotY_avg)
		robotOverall.append(strStored.split(", "))

		if strChkpt==checkpointNum[index]:
			currentChkpt = strChkpt
			prevCount = i
			index += 1
			robotX_avg = 0.0
			robotY_avg = 0.0
			indexi -= 1
			roboCt = 0
	indexi += 1

for j in range(0, len(beaconAcc)):
	beaconDev.append(int(beaconAcc[j][0]))
	beaconLng.append(float(beaconAcc[j][1]))
	beaconLat.append(float(beaconAcc[j][2]))
while indexj!=len(beaconAcc):
	strChkpt = int(beaconAcc[indexj][0])
	# if (strChkpt==currentChkpt) and (strChkpt==33):
	# 	tempX += float(beaconAcc[indexj][1])
	# 	tempY += float(beaconAcc[indexj][2])
	# 	pre_count += 1

	if indexj==0:
		if strChkpt==checkpointNum[index]:
			currentChkpt = strChkpt
			index += 1
	if 	(strChkpt==currentChkpt) or (indexj==len(beaconAcc)-1):
		beaconX_avg += float(beaconAcc[indexj][1])
		beaconY_avg += float(beaconAcc[indexj][2])
		
		count += 1		
		if indexj==len(beaconAcc)-1:
			beaconX_avg /= (count)
			beaconY_avg /= (count)
			strStored = str(currentChkpt) + ", " + str(beaconX_avg) + ", " + str(beaconY_avg)
			beaconOverall.append(strStored.split(", "))
			index = 0
			prevCount = 0
			break

	else:
		diff = strChkpt - currentChkpt
		if (beaconX_avg==0.0 and beaconY_avg==0.0) and (diff==1):
			beaconX_avg = float(beaconAcc[indexj-1][1])
			beaconY_avg = float(beaconAcc[indexj-1][2])
			count = 1
		beaconX_avg /= (count)
		beaconY_avg /= (count)
		strStored = str(currentChkpt) + ", " + str(beaconX_avg) + ", " + str(beaconY_avg)
		beaconOverall.append(strStored.split(", "))

		if strChkpt==checkpointNum[index]:
			currentChkpt = strChkpt
			prevCount = j
			index += 1
			beaconX_avg = 0.0
			beaconY_avg = 0.0
			indexj -= 1
			count = 0

		elif diff == 2:
			strStored = str(checkpointNum[index]) + ", Empty"
			beaconOverall.append(strStored.split(", "))
			index += 2
			currentChkpt = strChkpt
			prevCount = j
			beaconX_avg = 0.0
			beaconY_avg = 0.0
			indexj -= 1
			count = 0

		elif diff>2:
			while currentChkpt!=strChkpt-1:
				strStored = str(checkpointNum[index]) + ", Empty"
				beaconOverall.append(strStored.split(", "))
				index += 1
				currentChkpt += 1
			index += 1	
			beaconX_avg = 0.0
			beaconY_avg = 0.0
			currentChkpt = strChkpt
			prevCount = j
			indexj -= 1	
			count = 0
	indexj += 1
# print (pre_count)			
# tempX_avg = tempX/(pre_count)
# tempY_avg = tempY/(pre_count)
# print (tempX_avg)
# print (tempY_avg)
# print (beaconOverall)
roboterrorX = 0
roboterrorY = 0
beaconerrorX = 0
beaconerrorY = 0
errorX = 0
errorY = 0
errorDist = 0
for subjects in range(0, len(checkpointNum)):
	for indexes in range(0, len(robotOverall)):
		if int(robotOverall[indexes][0])==checkpointNum[subjects]:
			roboterrorX = float(robotOverall[indexes][1])
			roboterrorY = float(robotOverall[indexes][2])
			break
	for h in range(0, len(beaconOverall)):
		if int(beaconOverall[h][0])==checkpointNum[subjects]:
			if beaconOverall[h][1]!='Empty':
				beaconerrorX = float(beaconOverall[indexes][1])
				beaconerrorY = float(beaconOverall[indexes][2])
			else:
				beaconerrorX = 'NA'
				beaconerrorY = beaconerrorX
			break		

	if beaconerrorX!='NA' or beaconerrorY!='NA':
		errorDist = math.sqrt((pow((roboterrorX-beaconerrorX), 2) + pow((roboterrorY-beaconerrorY),2)))
	else:
		errorDist = 'Not applicable'	

	if subjects!=len(checkpointNum)-1:
		heatmap_error.write(str(checkpointNum[subjects]) + ", " + str(errorDist) + "\n")
	else:
		heatmap_error.write(str(checkpointNum[subjects]) + ", " + str(errorDist))

robot_box = {
				'Stations': robotDev,
				'x': robotLng,
				'y': robotLat
}

beacon_box = {
				'Stations': beaconDev,
				'x': beaconLng,
				'y': beaconLat
}

output_file("MD6 Data Analytics.html")
hm13 = BoxPlot(robot_box, values='x', label='Stations', legend=False, title='Robot X-Values Error Distance Boxplot', width = 600, plot_height=600)
hm14 = BoxPlot(robot_box, values='y', label='Stations', legend=False, title='Robot Y-Values Error Distance Boxplot', width = 600, plot_height=600)
hm15 = BoxPlot(beacon_box, values='x', label='Stations', legend=False, title='Beacon X-Values Error Distance Boxplot', width = 600, plot_height=600)
hm16 = BoxPlot(beacon_box, values='y', label='Stations', legend=False, title='Beacon Y-Values Error Distance Boxplot', width = 600, plot_height=600)
l = layout([hm13, hm14],
			[hm15, hm16])
show(l)
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