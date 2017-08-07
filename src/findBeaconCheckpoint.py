import requests
from bokeh.plotting import figure, show, output_file
from storeScale import getScale, getCoordinates, getImage
import csv, operator
from datetime import datetime
from bokeh.models.widgets import Select, Slider, TextInput
from bokeh.layouts import layout
import dateutil.relativedelta
import time
import dateutil.parser
import math
import calendar
from bokeh.io import curdoc
from bokeh.models.sources import ColumnDataSource

coord_lng_list = []
coord_lat_list = []
coord_total_list = []
checkpointlist = []
path_list = []
devList = []
sortedlist = []
min_pt = 0
max_pt = 0
min_x = 0
max_x = 0
min_y = 0
max_y = 0
stepCt = 0
index1 = 0
index2 = 0

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

def getMap():
	global min_pt, min_x, min_y, max_y, max_x, max_pt, path_list, devList, checkpointlist
	map_scale = getScale("MD6")
	map_coordinates = getCoordinates("MD6")
	beacon_reader = csv.reader(open("beacon_path_experiment4.csv"), delimiter=",")
	checkpoint_reader = csv.reader(open("Checkpoints.csv"), delimiter=",")
	next(checkpoint_reader)
	# initial_date = 1501217732
	# final_date = 1501219062
	# initial_date = datetime.strptime(initial_date, "%Y-%m-%d %H:%M:%S")
	# final_date = datetime.strptime(final_date, "%Y-%m-%d %H:%M:%S")
	sortedlist = sorted(beacon_reader, key=operator.itemgetter(0), reverse=False)
	checkpointlist = sorted(checkpoint_reader, key=operator.itemgetter(0), reverse=False)
	for i in range(0, len(map_coordinates)):
		coord_lng_list.append(map_coordinates[i][0])
		coord_lat_list.append(map_coordinates[i][1])
	coord_total_list = coord_lng_list + coord_lat_list	
	min_pt, max_pt = findMinimum_Maximum(coord_total_list)
	min_x, max_x = findMinimum_Maximum(coord_lng_list)
	min_y, max_y = findMinimum_Maximum(coord_lat_list)
	for j in range(0, len(sortedlist)):
		sortedlist[j][2] = float(sortedlist[j][2])
		sortedlist[j][3] = float(sortedlist[j][3])
		# sortedlist[j][1] = datetime.fromtimestamp((int(sortedlist[j][1])/1000)).strftime("%Y-%m-%d %H:%M:%S")
		# if (int(sortedlist[j][1])/1000 >= initial_date) and (int(sortedlist[j][1])/1000 <= final_date):
		path_list.append(sortedlist[j])
	path_list = sorted(path_list, key=operator.itemgetter(0, 1), reverse=False)
	devList.append("Select device...")
	for m in range(0, len(path_list)):
		if path_list[m][0] not in devList:
			devList.append(path_list[m][0])
getMap()

labelValue=" "
timestamp_beacon = TextInput(value=labelValue, title="Beacon Timestamp:", width = 100)
select1 = Select(title="DeviceID:", value=devList[0], options=devList, width=120)
p = figure(x_range=(min_pt, max_pt), y_range=(min_pt, max_pt))
image_link = getImage("MD6")
p.image_url(url=[image_link], x=min_x, y=min_y, w=(max_x - min_x), h=(max_y - min_y), anchor="bottom_left")
slider = Slider(start=0, value=0, title="TimeStamp")
x1 = ColumnDataSource(data=dict(x1=[], y1=[]))
for numOfCheckpts in range(0, len(checkpointlist)):
	p.circle(float(checkpointlist[numOfCheckpts][1]), float(checkpointlist[numOfCheckpts][2]), size=30, color="red", alpha=0.5)


def update():
	global stepCt
	timeList = []
	beaconPathY = []
	beaconPathX = []
	c = select1.value
	v = slider.value
	if c!="Select device...":
		for z in range(0, len(path_list)):
			if c == path_list[z][0]:
				timeList.append(path_list[z])
		# print (timeList)
		# for s in range(0, len(timeList)):
		# 	if s!=len(timeList)-1:
		# 		stepCt = int(timeList[s+1]) - int(timeList[s])
		# 	else:
		# 		stepCt = int(timeList[s]) - int(timeList[s-1])
		# 	slider.step = 1
		# slider.start = int(timeList[0])
		slider.end = len(timeList)
		slider.step = 1
		if v != len(timeList):
			beaconPathX.append(timeList[v][2])
			beaconPathY.append(timeList[v][3])
			new_beacon = ColumnDataSource(data=dict(x1=beaconPathX, y1=beaconPathY))
			ds.data = new_beacon.data
			timestamp_beacon.value = datetime.fromtimestamp((int(timeList[v][1])/1000)).strftime("%Y-%m-%d %H:%M:%S")
		# slider.value = slider.start
		# for k in range(0, len(path_list)):
		# 	if v==int(path_list[k][1]) and c==path_list[k][0]:
		# 		beaconPathX.append(path_list[k][2])
		# 		beaconPathY.append(path_list[k][3])
		# 		# print ("Hello: " + str(beaconPathX))
		# 		break
		
		

output_file('BeaconCheckpoint.html')
# p.circle('x1', 'y1', size=15, color="red", alpha=0.5, name="beacon_circle", source=x1)
# renderer = p.select(dict(name="beacon_circle"))
# ds = renderer[0].data_source
# l = layout([[select1, slider, timestamp_beacon],
# 			[p]])
# curdoc().add_root(l)
# curdoc().add_periodic_callback(update, 100)
show(p)