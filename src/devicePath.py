import base64
import requests
# import urllib3
import json
from bokeh.plotting import figure, show, output_file
from storePOI import office_POI, ward5_POI, actlab_POI
from storeScale import getScale, getCoordinates, getImage
import csv, operator
from datetime import datetime
from bokeh.io import curdoc
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
robot_list = []
coord_total_list = []
path_list = []
sortedlist = []
path_x = []
path_y = []
predicted_time = []
devList = []
strDate = 0
distance = 0.0
i = 1
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

# history_file = open('temp.csv', 'w')

def download_csv():
	count = 0
	beacon_csv = open('beacon_path_experiment2.csv', 'w')
	csv_url = 'http://137.132.165.139/api/history'
	with requests.Session() as s:
		download = s.get(csv_url)

	decoded_content = download.content.decode('utf-8')

	cr = csv.reader(decoded_content.splitlines(), delimiter=',')
	# next(cr)
	for row in cr:
		if count >= 1:
			time = datetime.fromtimestamp(int(row[5])/1000).strftime("%Y-%m-%d %H:%M:%S")
			second_time = datetime.fromtimestamp(int(row[6])/1000).strftime("%Y-%m-%d %H:%M:%S")
			row[5] = str(time)
			row[6] = str(second_time)
		count += 1	
		beacon_csv.write(str(", ".join(str(e) for e in row)).strip('"\'"') + "\n")

# download_csv()
# print (history_list)
def findMinimum_Maximum(_list):
	minimum = float("{0:.3f}".format(float(_list[0])))
	maximum = float("{0:.3f}".format(float(_list[0])))
	for a in range(1, len(_list)):
		temp = float("{0:.3f}".format(float(_list[a])))
		if temp<minimum:
			minimum = temp
		elif temp>maximum:   
			maximum = temp
	return minimum, maximum

def midpoint(x1, x2, y1, y2, divisor):
	midx = (x1 + x2)/divisor
	midy = (y1 + y2)/divisor
	return midx, midy

def actlab_Path():
	global path_list, history_list, xlist, ylist, sortedlist, mid_y, mid_x
	# center = ward5_POI()
	# print (center)
	map_scale = getScale("MD6")
	# print (map_scale)
	reader = csv.reader(open("robot_path_experiment4.csv"), delimiter=",")
	beacon_reader = csv.reader(open("beacon_path_experiment4.csv"), delimiter=",")
	# next(reader)
	# next(beacon_reader)
	sortedlist = sorted(beacon_reader, key=operator.itemgetter(0), reverse=False)
	robot_list = sorted(reader, key=operator.itemgetter(0), reverse=False)
	initial_date = "2017-07-28 12:55:32"
	final_date = "2017-07-28 13:17:42"
	initial_date = datetime.strptime(initial_date, "%Y-%m-%d %H:%M:%S")
	final_date = datetime.strptime(final_date, "%Y-%m-%d %H:%M:%S")
	for i in range(0, len(sortedlist)):
		# if sortedlist[i][3]==" ward5678":
		sortedlist[i][2] = float(sortedlist[i][2])
		sortedlist[i][3] = float(sortedlist[i][3])
		sortedlist[i][1] = datetime.fromtimestamp((int(sortedlist[i][1])/1000)).strftime("%Y-%m-%d %H:%M:%S")
		if (sortedlist[i][1] >= str(initial_date)) and (sortedlist[i][1] <= str(final_date)):
			path_list.append(sortedlist[i])
			# predicted_time.append(sortedlist[i][5])
	path_list = sorted(path_list, key=operator.itemgetter(0, 1), reverse=False)
	# for convertTime in range(0, len(path_list)):
	# 	path_list[convertTime][1] = datetime.fromtimestamp((int(path_list[convertTime][1])/1000)).strftime("%Y-%m-%d %H:%M:%S")
		# print (path_list[convertTime][1]<path_list[convertTime+1][1])
	for j in range(0, len(robot_list)):
		robot_list[j][0] = datetime.fromtimestamp(int(robot_list[j][0])).strftime("%Y-%m-%d %H:%M:%S")
		if (robot_list[j][0] >= str(initial_date)) and (robot_list[j][0] <= str(final_date)):
			history_list.append(robot_list[j])
		# history_file.write(str(history_list[j]) + "\n")
		# history_list[j][1] = (float(history_list[j][1]) / float(map_scale))
		# history_list[j][2] = (float(history_list[j][2]) / float(map_scale))
	# for s in range(0, len(path_list)):
		# path_list[s][1] = float(path_list[s][1]) / float(map_scale)
		# path_list[s][2] = float(path_list[s][2]) / float(map_scale)
	# print (sortedlist)
	# print (history_list)
	# print (len(history_list))
	for k in range(0, len(history_list)):	
		xlist.append("{0:.3f}".format((float(history_list[k][1]))/float(map_scale)))
		ylist.append("{0:.3f}".format((float(history_list[k][2]))/float(map_scale)))
		# if k!=len(history_list)-1:
		# 	x1 = float(history_list[k][1])
		# 	y1 = float(history_list[k][2])
		# 	x2 = float(history_list[k+1][1])
		# 	y2 = float(history_list[k+1][2])
		# 	distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
		# 	# print (distance)
		# 	if distance > 0.2:
		# 		diff_distance = (distance - 0.2)
		# 		mid_x, mid_y = midpoint(x1, x2, y1, y2, (2.0))
		# 		xlist.append("{0:.3f}".format(mid_x))
		# 		ylist.append("{0:.3f}".format(mid_y))
		robot_time.append(history_list[k][0])
	# print (robot_time)
	# for k in range(0, len(robot_time)):
	# 	history_file.write(str(robot_time[k]) + "\n")
	rtime_now = datetime.now()
	ctime_now = datetime.now()
	startTime = dateutil.parser.parse(robot_time[0])
	# predictedStart = dateutil.parser.parse(predicted_time[0])
	nextTime = dateutil.parser.parse(robot_time[1])
	# if c
	# predictedNext = dateutil.parser.parse(predicted_time[1])
	# print (startTime)
	# print (predictedStart)
	rd = dateutil.relativedelta.relativedelta (nextTime, startTime)
	# rs = dateutil.relativedelta.relativedelta (predictedNext, predictedStart)
	# predict_duration = rs.seconds/10
	duration = rd.seconds/10
	# print (duration)
	devList.append("Select device...")
	# devList.append(path_list[0][0])
	for m in range(0, len(path_list)):
		if path_list[m][0] not in devList:
			devList.append(path_list[m][0])
	# for b in range(0, len(devList)):
	# 	if devList[b]==path_list[b][0]:
	# 		path_x.append("{0:.3f}".format(float(path_list[m][2])))
	# 		path_y.append("{0:.3f}".format(float(path_list[m][1])))


	# print (ylist)
	circle_x.append(float("{0:.3f}".format(float(xlist[0]))))
	circle_y.append(float("{0:.3f}".format(float(ylist[0]))))
	# circle2_x.append(float("{0:.3f}".format(float(path_x[0]))))
	# circle2_y.append(float("{0:.3f}".format(float(path_y[0]))))
	x1 = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
	y1 = ColumnDataSource(data=dict(x1=circle2_x, y1=circle2_y))
	line1 = ColumnDataSource(data=dict(x1=path_x, y1=path_y))
	map_coordinates = getCoordinates("MD6")
	for i in range(0, len(map_coordinates)):
		coord_lng_list.append(map_coordinates[i][0])
		coord_lat_list.append(map_coordinates[i][1])
	coord_total_list = coord_lng_list + coord_lat_list	
	min_pt, max_pt = findMinimum_Maximum(coord_total_list)
	min_x, max_x = findMinimum_Maximum(coord_lng_list)
	min_y, max_y = findMinimum_Maximum(coord_lat_list)
	# print (min_y)
	# print (max_y)
	return min_pt, max_pt, min_x, max_x, min_y, max_y, x1, y1, line1, rtime_now, ctime_now, startTime, duration, predictedStart, predict_duration
 
min_pt, max_pt, min_x, max_x, min_y, max_y, x1, y1, line1, rtime_now, ctime_now, startTime, duration, predictedStart, predict_duration = actlab_Path()	
# print (xlist)
# print (ylist)
labelValue=" "
select1 = Select(title="DeviceID:", value=devList[0], options=devList, width=120)
timestamp_robot = TextInput(value=labelValue, title="Robot Timestamp:", width = 100)
timestamp_Beacon = TextInput(value=labelValue, title="Beacon Timestamp:", width = 20)
seconds_checkbox = CheckboxGroup(
        labels=["Seconds"], active=[0, 1])
average_checkbox = CheckboxGroup(
        labels=["Average"], active=[0, 1])
# output_file('Actlab.html')
p = figure(x_range=(min_pt, max_pt), y_range=(min_pt, max_pt))
image_link = getImage("MD6")
p.image_url(url=[image_link], x=min_x, y=min_y, w=(max_x - min_x), h=(max_y - min_y), anchor="bottom_left")
p.line(xlist, ylist, line_width=3, color="navy")

date = time.strptime(str(startTime), "%Y-%m-%d %H:%M:%S")
if seconds_checkbox.active==[]:
	strDate = str(date.tm_mday) + "-" + str(calendar.month_name[date.tm_mon]) + "-" + str(date.tm_year) + " " + str(date.tm_hour) + ":" + str(date.tm_min)
else:
	strDate = str(date.tm_mday) + "-" + str(calendar.month_name[date.tm_mon]) + "-" + str(date.tm_year) + " " + str(date.tm_hour) + ":" + str(date.tm_min) + ":" + str(date.tm_sec)
timestamp_robot.value = str(strDate)

def seeLocation():
	global timestamp, mindiff
	circle_x = []
	circle_y = []
	timeIndex = 0
	converted_time = datetime.fromtimestamp(int(timestamp)/1000).strftime("%Y-%m-%d %H:%M:%S")
	initial_diff = dateutil.relativedelta.relativedelta (converted_time, robot_time[0])
	mindiff = initial_diff.seconds
	for index in range(0, len(robot_time)):
		diff = dateutil.relativedelta.relativedelta (converted_time, robot_time[index])
		if converted_time==robot_time[index]:
			circle_x.append(float("{0:.3f}".format(float(xlist[index]))))
			circle_y.append(float("{0:.3f}".format(float(ylist[index]))))
			mindiff = 0
			break
		else:
			timediff = diff.seconds
			if timediff<mindiff and timediff>0:
				mindiff = timediff
				timeIndex = index
	if circle_x==[] and circle_y ==[]:
		circle_x.append(float("{0:.3f}".format(float(xlist[timeIndex]))))
		circle_y.append(float("{0:.3f}".format(float(ylist[timeIndex]))))		
	new_x = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
	ds.data = new_x.data





def update():
	global i, predict, count, currTime, startTime, duration, rtime_now, ctime_now, predict_duration, predictedStart, strDate, predict_time, pre_current_dur, predicted_time
	circle_x = []
	counter = 0
	circle_y = []
	path_x = []
	path_y = []
	circle2_x = []
	circle2_y = []
	temp_x = []
	temp_y = []
	predictedNext = 0
	iterations = 0
	totalYSum = 0
	totalXAvg = 0
	totalYAvg = 0
	totalXSum = 0
	print (duration)
	print (predict_duration)
	# print (seconds_checkbox.active)
	# print (time_now)
	# print (datetime.now())
	# print ("robot: " + str(duration))
	# print ("Beacon: " + str(predict_duration))
	rd = dateutil.relativedelta.relativedelta (datetime.now(), rtime_now)
	# rz = dateutil.relativedelta.relativedelta (datetime.now(), ctime_now)
	current_dur = rd.seconds
	# pre_current_dur = rz.seconds
	print ("current: " + str(current_dur))
	print ("Pre-current: " + str(pre_current_dur))

	c = select1.value
	for q in range(0, len(path_list)):
		if c==path_list[q][0]:
			temp_x.append("{0:.3f}".format(float(path_list[q][2])))
			temp_y.append("{0:.3f}".format(float(path_list[q][3])))
	for s in range(0, len(temp_x)):		
		diff = len(temp_x) - counter
		if diff > 5:
			totalXAvg = (float(temp_x[counter]) + float(temp_x[counter+1]) + float(temp_x[counter+2]) + float(temp_x[counter+3]) + float(temp_x[counter+4]))/5.0
			totalYAvg = (float(temp_y[counter]) + float(temp_y[counter+1]) + float(temp_y[counter+2]) + float(temp_y[counter+3]) + float(temp_y[counter+4]))/5.0
			counter += 5
		else:
			while iterations!=diff:
				totalXSum += (float(temp_x[counter+iterations]))
				totalYSum += (float(temp_y[counter+iterations]))
				iterations += 1
			totalXAvg = totalXSum/diff
			totalYAvg = totalYSum/diff	
		totalXSum = 0
		totalYSum = 0
		path_x.append("{0:.3f}".format(float(totalXAvg)))
		path_y.append("{0:.3f}".format(float(totalYAvg)))
			
	if average_checkbox.active!=[]:
		new_line = ColumnDataSource(data=dict(x1=path_x, y1=path_y))
	else:
		new_line = ColumnDataSource(data=dict(x1=temp_x, y1=temp_y))
	da.data = new_line.data
	if c=="Select device...":
		if (current_dur>=duration):
			print ("duration: " + str(duration))
			timestamp_Beacon.title = "Beacon Timestamp"
			timestamp_Beacon.value = ""
			# print ("1")
			
			circle_x.append(float("{0:.3f}".format(float(xlist[i]))))
			# print ("2")
			circle_y.append(float("{0:.3f}".format(float(ylist[i]))))
			# print ("3")
			
			# print ("4")
			new_x = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
			# print ("8")
			# print (circle2_x)
			# print ("5: " + str(dz.data))
			new_y = ColumnDataSource(data=dict(x1=circle2_x, y1=circle2_y))
			# print ("9")
			
			ds.data = new_x.data
			# print ("6: " + str(dz.data))
			# print ("10")
			dz.data = new_y.data
			# print ("11")
			
			# print (da.data)
			# print ("7: " + str(dz.data))
			# print (dz.data)
			i += 1
			# predict += 1
			# print ("8: " + str(dz.data))
			if ((i == len(xlist) - 1) or (i == len(ylist) - 1)):
				i = 0
			startTime = dateutil.parser.parse(robot_time[currTime])
			# predictedStart = dateutil.parser.parse(predicted_time[currTime])
			currTime += 1
			nextTime = dateutil.parser.parse(robot_time[currTime])
			# predictedNext = dateutil.parser.parse(predicted_time[currTime])
			rd = dateutil.relativedelta.relativedelta (nextTime, startTime)
			# rs = dateutil.relativedelta.relativedelta (predictedNext, predictedStart)
			duration = rd.seconds/10
			date = time.strptime(str(startTime), "%Y-%m-%d %H:%M:%S")
			if seconds_checkbox.active==[]:
				strDate = str(date.tm_mday) + "-" + str(calendar.month_name[date.tm_mon]) + "-" + str(date.tm_year) + " " + str(date.tm_hour) + ":" + str(date.tm_min)
			else:
				strDate = str(date.tm_mday) + "-" + str(calendar.month_name[date.tm_mon]) + "-" + str(date.tm_year) + " " + str(date.tm_hour) + ":" + str(date.tm_min) + ":" + str(date.tm_sec)
			timestamp_robot.value = str(strDate)
			# predict_duration = rs.seconds
			# print ("duration: " + str(duration))
			if currTime==(len(robot_time)-1):
				currTime = 0
			rtime_now = datetime.now()
	else:
		rz = dateutil.relativedelta.relativedelta (datetime.now(), ctime_now)
		pre_current_dur = rz.seconds
		for j in range(0, len(sortedlist)):
			if (sortedlist[j][0]==c):
				predicted_time.append(sortedlist[j][1])
		if count==0:
			predictedStart = dateutil.parser.parse(predicted_time[0])
			predictedNext = dateutil.parser.parse(predicted_time[1])
			Beacon_date = time.strptime(str(predictedStart), "%Y-%m-%d %H:%M:%S")
			if seconds_checkbox.active==[]:
				strDate = str(Beacon_date.tm_mday) + "-" + str(calendar.month_name[Beacon_date.tm_mon]) + "-" + str(Beacon_date.tm_year) + " " + str(Beacon_date.tm_hour) + ":" + str(Beacon_date.tm_min)
			else:
				strDate = str(Beacon_date.tm_mday) + "-" + str(calendar.month_name[Beacon_date.tm_mon]) + "-" + str(Beacon_date.tm_year) + " " + str(Beacon_date.tm_hour) + ":" + str(Beacon_date.tm_min) + ":" + str(Beacon_date.tm_sec)
			timestamp_Beacon.value = str(strDate)
			timestamp_Beacon.title = "Beacon " + str(c) + " Timestamp"
		if (current_dur>=duration):
			print ("Robot move")
			count += 1
			# print ("1")
			circle_x.append(float("{0:.3f}".format(float(xlist[i]))))
			# print ("2")
			circle_y.append(float("{0:.3f}".format(float(ylist[i]))))
			# print ("3")
			
			# print ("4")
			new_x = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
			# print ("8")
			# print (circle2_x)
			# print ("5: " + str(dz.data))
			# new_y = ColumnDataSource(data=dict(x1=circle2_x, y1=circle2_y))
			# print ("9")
			
			ds.data = new_x.data
			# print ("6: " + str(dz.data))
			# print ("10")
			# dz.data = new_y.data
			# print ("11")
			
			# print (da.data)
			# print ("7: " + str(dz.data))
			# print (dz.data)
			i += 1
			# predict += 1
			# print ("8: " + str(dz.data))
			if ((i == len(xlist) - 1) or (i == len(ylist) - 1)):
				i = 0
			startTime = dateutil.parser.parse(robot_time[currTime])
			# predictedStart = dateutil.parser.parse(predicted_time[currTime])
			currTime += 1
			nextTime = dateutil.parser.parse(robot_time[currTime])
			# predictedNext = dateutil.parser.parse(predicted_time[currTime])
			rd = dateutil.relativedelta.relativedelta (nextTime, startTime)
			# rs = dateutil.relativedelta.relativedelta (predictedNext, predictedStart)
			duration = rd.seconds/10
			date = time.strptime(str(startTime), "%Y-%m-%d %H:%M:%S")
			if seconds_checkbox.active==[]:
				strDate = str(date.tm_mday) + "-" + str(calendar.month_name[date.tm_mon]) + "-" + str(date.tm_year) + " " + str(date.tm_hour) + ":" + str(date.tm_min)
			else:
				strDate = str(date.tm_mday) + "-" + str(calendar.month_name[date.tm_mon]) + "-" + str(date.tm_year) + " " + str(date.tm_hour) + ":" + str(date.tm_min) + ":" + str(date.tm_sec)
			timestamp_robot.value = str(strDate)
			# predict_duration = rs.seconds
			# print ("duration: " + str(duration))
			if currTime==(len(robot_time)-1):
				currTime = 0
			rtime_now = datetime.now()
		if (pre_current_dur>=predict_duration):
			print ("Beacon Move")
			if average_checkbox.active!=[]:
				if (path_x!=[]) and (path_y!=[]):
					circle2_x.append(float("{0:.3f}".format(float(path_x[predict]))))	
					circle2_y.append(float("{0:.3f}".format(float(path_y[predict]))))
			else:
				if (temp_x!=[]) and (temp_y!=[]):
					circle2_x.append(float("{0:.3f}".format(float(temp_x[predict]))))	
					circle2_y.append(float("{0:.3f}".format(float(temp_y[predict]))))		
			new_y = ColumnDataSource(data=dict(x1=circle2_x, y1=circle2_y))	
			dz.data = new_y.data
			predict += 1
			if ((predict == len(path_x)-1) or (predict == len(path_y)-1)):
				predict = 0	
			predictedStart = dateutil.parser.parse(predicted_time[predict_time])
			predict_time += 1
			predictedNext = dateutil.parser.parse(predicted_time[predict_time])
			rs = dateutil.relativedelta.relativedelta (predictedNext, predictedStart)
			predict_duration = rs.seconds/10
			Beacon_date = time.strptime(str(predictedStart), "%Y-%m-%d %H:%M:%S")
			if seconds_checkbox.active==[]:
				strDate = str(Beacon_date.tm_mday) + "-" + str(calendar.month_name[Beacon_date.tm_mon]) + "-" + str(Beacon_date.tm_year) + " " + str(Beacon_date.tm_hour) + ":" + str(Beacon_date.tm_min)
			else:
				strDate = str(Beacon_date.tm_mday) + "-" + str(calendar.month_name[Beacon_date.tm_mon]) + "-" + str(Beacon_date.tm_year) + " " + str(Beacon_date.tm_hour) + ":" + str(Beacon_date.tm_min) + ":" + str(Beacon_date.tm_sec)
			timestamp_Beacon.value = str(strDate)
			if (predict_time==(len(predicted_time)-1)) or (select1.value!=c):
				predict_time = 0
				count = 0
				print ("Counter: " + str(count))
			ctime_now = datetime.now()

p.circle('x1', 'y1', size=15, color="red", alpha=0.5, name="robot_circle", source=x1)
p.circle('x1', 'y1', size=15, color="navy", alpha=0.5, name="predicted_circle", source=y1)
p.line('x1', 'y1', line_width=3, color="red", name="predicted_line", source=line1)

renderer = p.select(dict(name="robot_circle"))
enderer = p.select(dict(name="predicted_circle"))
derer = p.select(dict(name="predicted_line"))
ds = renderer[0].data_source
dz = enderer[0].data_source
da = derer[0].data_source
# p.axis.visible = False
p.xgrid.grid_line_color = None
p.xgrid.grid_line_color = None
# print (dz.data)
l = layout([select1, timestamp_robot, timestamp_Beacon],
			[seconds_checkbox, average_checkbox],
			[p])
curdoc().add_root(l)
curdoc().add_periodic_callback(update, 1000)
# curdoc().add_periodic_callback(seeLocation, 1000)


# show(p)





