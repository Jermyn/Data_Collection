import base64
import requests
# import urllib3
import json
from bokeh.plotting import figure, show, output_file
from storePOI import office_POI, ward5_POI, actlab_POI
from storeScale import getScale
import csv, operator
from datetime import datetime
from bokeh.io import curdoc
from bokeh.models.sources import ColumnDataSource
import csv, operator
import pandas as pd
from bokeh.models.widgets import Select, TextInput
from bokeh.layouts import layout
import dateutil.relativedelta
import time
import dateutil.parser
import math


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
distance = 0.0
i = 1
predict = 1
currTime = 1
startTime = 0
duration = 0
time_now = 0
midx = 0.0
mid_y = 0.0
predictedStart = 0
predict_duration = 0

def download_csv():
	beacon_csv = open('beacon_path.csv', 'w')
	csv_url = 'http://137.132.165.139/api/history'
	with requests.Session() as s:
		download = s.get(csv_url)

	decoded_content = download.content.decode('utf-8')

	cr = csv.reader(decoded_content.splitlines(), delimiter=',')
	next(cr)
	for row in cr:
		time = datetime.fromtimestamp(int(row[5])/1000).strftime("%Y-%m-%d %H:%M:%S")
		second_time = datetime.fromtimestamp(int(row[6])/1000).strftime("%Y-%m-%d %H:%M:%S")
		row[5] = str(time)
		row[6] = str(second_time)
		beacon_csv.write(str(", ".join(str(e) for e in row)).strip('"\'"') + "\n")

download_csv()
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
	center = ward5_POI()
	# print (center)
	map_scale = getScale("ward5678")
	# print (map_scale)
	reader = csv.reader(open("robot_path_parsed.csv"), delimiter=",")
	beacon_reader = csv.reader(open("beacon_path.csv"), delimiter=",")
	next(reader)
	next(beacon_reader)
	sortedlist = sorted(beacon_reader, key=operator.itemgetter(0, 5), reverse=False)
	history_list = sorted(reader, key=operator.itemgetter(0), reverse=False)
	for i in range(0, len(sortedlist)):
		if sortedlist[i][3]==" ward5678":
			sortedlist[i][1] = float(sortedlist[i][1])*float(map_scale)
			sortedlist[i][2] = float(sortedlist[i][2])*float(map_scale)
			path_list.append(sortedlist[i])
			predicted_time.append(sortedlist[i][5])
	path_list = sorted(path_list, key=operator.itemgetter(0, 5), reverse=False)
	# print (path_list)
	for j in range(0, len(history_list)):
		history_list[j][0] = datetime.fromtimestamp(int(history_list[j][0])).strftime("%Y-%m-%d %H:%M:%S")
		# history_list[j][1] = (float(history_list[j][1]) / float(map_scale))
		# history_list[j][2] = (float(history_list[j][2]) / float(map_scale))
	# for s in range(0, len(path_list)):
		# path_list[s][1] = float(path_list[s][1]) / float(map_scale)
		# path_list[s][2] = float(path_list[s][2]) / float(map_scale)
	# print (sortedlist)
	for k in range(0, len(history_list)):
		xlist.append("{0:.3f}".format(float(history_list[k][1])))
		ylist.append("{0:.3f}".format(float(history_list[k][2])))
		if k!=len(history_list)-1:
			x1 = float(history_list[k][1])
			y1 = float(history_list[k][2])
			x2 = float(history_list[k+1][1])
			y2 = float(history_list[k+1][2])
			distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
			print (distance)
			if distance > 0.2:
				diff_distance = (distance - 0.2)
				mid_x, mid_y = midpoint(x1, x2, y1, y2, (2.0))
				xlist.append("{0:.3f}".format(mid_x))
				ylist.append("{0:.3f}".format(mid_y))
		robot_time.append(history_list[k][0])
	# print (robot_time)
	time_now = datetime.now()
	startTime = dateutil.parser.parse(robot_time[0])
	predictedStart = dateutil.parser.parse(predicted_time[0])
	nextTime = dateutil.parser.parse(robot_time[1])
	predictedNext = dateutil.parser.parse(predicted_time[1])
	print (startTime)
	print (predictedStart)
	rd = dateutil.relativedelta.relativedelta (nextTime, startTime)
	rs = dateutil.relativedelta.relativedelta (predictedNext, predictedStart)
	predict_duration = rs.seconds
	duration = rd.seconds
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
# 	print (path_list)
	query_ward5 = 'query{map (id:"ward5678") {image}}'
	query_coordinates = 'query{map (id:"ward5678") {coordinates}}'
	r = requests.get("http://137.132.165.139/graphql", {"query":query_ward5})
	s = requests.get("http://137.132.165.139/graphql", {"query":query_coordinates})
	coor = s.text
	cod = json.loads(coor)
	image = r.text
	img = json.loads(image)
	imgdata = base64.b64decode(img['data']['map']['image'])
	filename = 'ward5.png'
	with open(filename, 'wb') as f:
		f.write(imgdata)
	for i in range(0, len(cod['data']['map']['coordinates'])):
		temp = cod['data']['map']['coordinates'].split("],")
	for i in range(0, len(temp)):
		temp[i] = temp[i].split(",")
		for j in range(0, 2):
			while "[" in temp[i][j]:
				temp[i][j] = temp[i][j].strip("[")
			while "]" in temp[i][j]:
				temp[i][j] = temp[i][j].strip("]")	
		temp[i][0] = float(temp[i][0])*float(map_scale)
		temp[i][1] = float(temp[i][1])*float(map_scale)
		coord_lng_list.append(temp[i][0])
		coord_lat_list.append(temp[i][1])
		coord_total_list = coord_lng_list + coord_lat_list	
	min_pt, max_pt = findMinimum_Maximum(coord_total_list)
	min_x, max_x = findMinimum_Maximum(coord_lng_list)
	min_y, max_y = findMinimum_Maximum(coord_lat_list)
	return min_pt, max_pt, min_x, max_x, min_y, max_y, x1, y1, line1, time_now, startTime, duration, predictedStart, predict_duration
 
min_pt, max_pt, min_x, max_x, min_y, max_y, x1, y1, line1, time_now, startTime, duration, predictedStart, predict_duration = actlab_Path()	
labelValue=" "
select1 = Select(title="DeviceID:", value=devList[0], options=devList, width=100)
timestamp = TextInput(value=labelValue, title="Timestamp:")
# output_file('Actlab.html')
p = figure(x_range=(min_pt, max_pt), y_range=(min_pt, max_pt))
p.image_url(url=['https://image.ibb.co/eAuMNk/ward5.png'], x=min_x, y=min_y, w=(max_x - min_x), h=(max_y - min_y), anchor="bottom_left")
p.line(xlist, ylist, line_width=3, color="navy")
timestamp.value = str(startTime)

def update():
	global i, predict, currTime, startTime, duration, time_now, predict_duration, predictedStart
	circle_x = []
	circle_y = []
	path_x = []
	path_y = []
	circle2_x = []
	circle2_y = []
	print (duration)
	print (predict_duration)
	print (time_now)
	print (datetime.now())
	rd = dateutil.relativedelta.relativedelta (datetime.now(), time_now)
	current_dur = rd.seconds
	print ("current: " + str(current_dur))
	c = select1.value
	for q in range(0, len(path_list)):
		if c==path_list[q][0]:
			path_x.append("{0:.3f}".format(float(path_list[q][2])))
			path_y.append("{0:.3f}".format(float(path_list[q][1])))
			# if q!=len(path_list)-1:
			# 	x1 = float(path_list[q][1])
			# 	y1 = float(path_list[q][2])
			# 	x2 = float(path_list[q+1][1])
			# 	y2 = float(path_list[q+1][2])
			# 	distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
			# 	print ("distance: " + str(distance))
			# 	if distance > 2.0:
			# 		diff_distance = (distance - 1.0)
			# 		mid_x, mid_y = midpoint(x1, x2, y1, y2, (5.0 + diff_distance))
			# 		path_x.append("{0:.3f}".format(mid_x))
			# 		path_y.append("{0:.3f}".format(mid_y))
	# circle2_x.append(float("{0:.3f}".format(float(path_x[0]))))
	# circle2_y.append(float("{0:.3f}".format(float(path_y[0]))))
	new_line = ColumnDataSource(data=dict(x1=path_x, y1=path_y))
	da.data = new_line.data
	if c=="Select device...":
		while (current_dur==duration):
			print ("duration: " + str(duration))
			print("predict: " + str(predict_duration))
			if i!=len(xlist)-1:
				x1 = float(xlist[i])
				y1 = float(ylist[i])
				x2 = float(xlist[i+1])
				y2 = float(ylist[i+1])
				distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
				print ("distance: " + str(distance))
			# print ("x: " + str(xlist[i]))
			# print("y: " + str(ylist[i]))
			
			print ("1")
			
			circle_x.append(float("{0:.3f}".format(float(xlist[i]))))
			print ("2")
			circle_y.append(float("{0:.3f}".format(float(ylist[i]))))
			print ("3")
			
			print ("4")
			# print (path_y)
			# print ("2: " + str(dz.data))
			# print (len(xlist))
			# if c=="128":
			# 	print (len(path_x))
			# if c=="899":
			# 	print (len(path_x))
			# if c=="901":
			# 	print (len(path_x))	
			# if (path_x!=[]) and (path_y!=[]):
			# 	circle2_x.append(float("{0:.3f}".format(float(path_x[predict]))))	
			# 	circle2_y.append(float("{0:.3f}".format(float(path_y[predict]))))
			print ("7")
				# print (circle2_x)
			print ("5")
			# print (path_x)
			# print ("3: " + str(dz.data))
			# for j in range(0, len(path_x)):
				
			
			print ("6")
			
			# print ("4: " + str(dz.data))
			# for k in range(0, len(path_y)):	
				
			
			new_x = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
			print ("8")
			# print (circle2_x)
			# print ("5: " + str(dz.data))
			# new_y = ColumnDataSource(data=dict(x1=circle2_x, y1=circle2_y))
			print ("9")
			
			ds.data = new_x.data
			# print ("6: " + str(dz.data))
			print ("10")
			# dz.data = new_y.data
			print ("11")
			
			# print (da.data)
			# print ("7: " + str(dz.data))
			# print (dz.data)
			i += 1
			# predict += 1
			# print ("8: " + str(dz.data))
			if ((i == len(xlist) - 1) or (i == len(ylist) - 1)):
				i = 0
			# if ((predict == len(path_x)-1) or (predict == len(path_y)-1)):
			# 	predict = 0	
			startTime = dateutil.parser.parse(robot_time[currTime])
			# predictedStart = dateutil.parser.parse(predicted_time[currTime])
			currTime += 1
			nextTime = dateutil.parser.parse(robot_time[currTime])
			# predictedNext = dateutil.parser.parse(predicted_time[currTime])
			rd = dateutil.relativedelta.relativedelta (nextTime, startTime)
			# rs = dateutil.relativedelta.relativedelta (predictedNext, predictedStart)
			duration = rd.seconds
			timestamp.value = str(startTime)
			# predict_duration = rs.seconds
			print ("duration: " + str(duration))
			if currTime==(len(robot_time)-1):
				currTime = 0
			time_now = datetime.now()
	else:
		while (current_dur==duration) or (current_dur==predict_duration):
			print ("duration: " + str(duration))
			print("predict: " + str(predict_duration))
			if i!=len(xlist)-1:
				x1 = float(xlist[i])
				y1 = float(ylist[i])
				x2 = float(xlist[i+1])
				y2 = float(ylist[i+1])
				distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
				print ("distance: " + str(distance))
			# print ("x: " + str(xlist[i]))
			# print("y: " + str(ylist[i]))
			
			print ("1")
			
			circle_x.append(float("{0:.3f}".format(float(xlist[i]))))
			print ("2")
			circle_y.append(float("{0:.3f}".format(float(ylist[i]))))
			print ("3")
			
			print ("4")
			# print (path_y)
			# print ("2: " + str(dz.data))
			# print (len(xlist))
			if c=="128":
				print (len(path_x))
			# if c=="899":
			# 	print (len(path_x))
			# if c=="901":
			# 	print (len(path_x))	
			if (path_x!=[]) and (path_y!=[]):
				circle2_x.append(float("{0:.3f}".format(float(path_x[predict]))))	
				circle2_y.append(float("{0:.3f}".format(float(path_y[predict]))))
			print ("7")
				# print (circle2_x)
			print ("5")
			# print (path_x)
			# print ("3: " + str(dz.data))
			# for j in range(0, len(path_x)):
				
			
			print ("6")
			
			# print ("4: " + str(dz.data))
			# for k in range(0, len(path_y)):	
				
			
			new_x = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
			print ("8")
			# print (circle2_x)
			# print ("5: " + str(dz.data))
			new_y = ColumnDataSource(data=dict(x1=circle2_x, y1=circle2_y))
			print ("9")
			
			ds.data = new_x.data
			# print ("6: " + str(dz.data))
			print ("10")
			dz.data = new_y.data
			print ("11")
			
			# print (da.data)
			# print ("7: " + str(dz.data))
			# print (dz.data)
			i += 1
			predict += 1
			# print ("8: " + str(dz.data))
			if ((i == len(xlist) - 1) or (i == len(ylist) - 1)):
				i = 0
			if ((predict == len(path_x)-1) or (predict == len(path_y)-1)):
				predict = 0	
			startTime = dateutil.parser.parse(robot_time[currTime])
			predictedStart = dateutil.parser.parse(predicted_time[currTime])
			currTime += 1
			nextTime = dateutil.parser.parse(robot_time[currTime])
			predictedNext = dateutil.parser.parse(predicted_time[currTime])
			rd = dateutil.relativedelta.relativedelta (nextTime, startTime)
			rs = dateutil.relativedelta.relativedelta (predictedNext, predictedStart)
			duration = rd.seconds
			predict_duration = rs.seconds
			print ("duration: " + str(duration))
			if currTime==(len(robot_time)-1):
				currTime = 0
			time_now = datetime.now()
# print (y1.data)

p.circle('x1', 'y1', size=15, color="red", alpha=0.5, name="robot_circle", source=x1)
p.circle('x1', 'y1', size=15, color="navy", alpha=0.5, name="predicted_circle", source=y1)
p.line('x1', 'y1', line_width=3, color="red", name="predicted_line", source=line1)

renderer = p.select(dict(name="robot_circle"))
enderer = p.select(dict(name="predicted_circle"))
derer = p.select(dict(name="predicted_line"))
ds = renderer[0].data_source
dz = enderer[0].data_source
da = derer[0].data_source
p.axis.visible = False
p.xgrid.grid_line_color = None
p.xgrid.grid_line_color = None
# print (dz.data)
l = layout([select1, timestamp],
			[p])
curdoc().add_root(l)
curdoc().add_periodic_callback(update, 500)


# show(p)





