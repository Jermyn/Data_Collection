import base64
import requests
# import urllib3
import json
from bokeh.plotting import figure, show, output_file
from storePOI import office_POI, ward5_POI, actlab_POI
from storeScale import getScale
import csv, operator
import datetime
from bokeh.io import curdoc
from bokeh.models.sources import ColumnDataSource
import csv, operator
import pandas as pd
from bokeh.models.widgets import Select
from bokeh.layouts import layout


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
circle2_y = []
coord_total_list = []
path_list = []
sortedlist = []
path_x = []
path_y = []
devList = []
i = 1

def download_csv():
	csv_url = 'http://137.132.165.139/api/history'
	with requests.Session() as s:
		download = s.get(csv_url)

	decoded_content = download.content.decode('utf-8')

	cr = csv.reader(decoded_content.splitlines(), delimiter=',')
	next(cr)
	my_list = list(cr)
	for i in range(0, len(my_list)):
		my_list[i][5] = datetime.datetime.fromtimestamp(int(my_list[i][5])/1000).strftime("%Y-%m-%d %H:%M:%S")
		my_list[i][6] = datetime.datetime.fromtimestamp(int(my_list[i][6])/1000).strftime("%Y-%m-%d %H:%M:%S")
	return my_list
		

# sortedlist = download_csv()
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


def actlab_Path():
	global path_list, history_list, xlist, ylist, sortedlist
	center = ward5_POI()
	# print (center)
	map_scale = getScale("ward5")
	# print (map_scale)
	reader = csv.reader(open("ward5_1.csv"), delimiter=",")
	next(reader)
	history_list = sorted(reader, key=operator.itemgetter(0), reverse=False)
	for i in range(0, len(sortedlist)):
		if sortedlist[i][3]=="ward5":
			path_list.append(sortedlist[i])
	path_list = sorted(path_list, key=operator.itemgetter(0, 5), reverse=False)
	# print (path_list)
	for j in range(0, len(history_list)):
		history_list[j][0] = datetime.datetime.fromtimestamp(int(history_list[j][0])).strftime("%Y-%m-%d %H:%M:%S")
		history_list[j][1] = (float(history_list[j][1]) / float(map_scale))
		history_list[j][2] = (float(history_list[j][2]) / float(map_scale))
	for s in range(0, len(path_list)):
		path_list[s][1] = float(path_list[s][1]) / float(map_scale)
		path_list[s][2] = float(path_list[s][2]) / float(map_scale)
	# print (history_list)
	for k in range(0, len(history_list)):
		xlist.append("{0:.3f}".format(float(history_list[k][1])))
		ylist.append("{0:.3f}".format(float(history_list[k][2])))
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
	line1 = ColumnDataSource(data=dict(x1=xlist, y1=ylist))
# 	print (path_list)
	query_ward5 = 'query{map (id:"ward5") {image}}'
	query_coordinates = 'query{map (id:"ward5") {coordinates}}'
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
		coord_lng_list.append(temp[i][0])
		coord_lat_list.append(temp[i][1])
		coord_total_list = coord_lng_list + coord_lat_list	
	min_pt, max_pt = findMinimum_Maximum(coord_total_list)
	min_x, max_x = findMinimum_Maximum(coord_lng_list)
	min_y, max_y = findMinimum_Maximum(coord_lat_list)
	return min_pt, max_pt, min_x, max_x, min_y, max_y, x1, y1, line1
 
min_pt, max_pt, min_x, max_x, min_y, max_y, x1, y1, line1 = actlab_Path()	
select1 = Select(title="DeviceID:", value=devList[0], options=devList, width=100)
# output_file('Actlab.html')
p = figure(x_range=(min_pt, max_pt), y_range=(min_pt, max_pt))
p.image_url(url=['http://i.imgur.com/G52LVgB.png'], x=min_x, y=min_y, w=(max_x - min_x), h=(max_y - min_y), anchor="bottom_left")
# p.line(xlist, ylist, line_width=3)

def update():
	global i
	circle_x = []
	circle_y = []
	# circle2_x = []
	# circle2_y = []
	c = select1.value
	# print ("1: " + str(dz.data))
	
	circle_x.append(float("{0:.3f}".format(float(xlist[i]))))
	circle_y.append(float("{0:.3f}".format(float(ylist[i]))))
	for q in range(0, len(path_list)):
		if c==path_list[q][0]:
			path_x.append("{0:.3f}".format(float(path_list[q][2])))
			path_y.append("{0:.3f}".format(float(path_list[q][1])))
	# print (path_y)
	# print ("2: " + str(dz.data))
	# if (path_x!=[]) and (path_y!=[]):
	# 	circle2_x.append(float("{0:.3f}".format(float(path_x[0]))))
	# 	circle2_y.append(float("{0:.3f}".format(float(path_y[0]))))	
		# print (circle2_x)
	# print ("3: " + str(dz.data))
	# for j in range(0, len(path_x)):
		
		# circle2_x.append(float("{0:.3f}".format(float(path_x[j]))))
	# print ("4: " + str(dz.data))
	# for k in range(0, len(path_y)):	
		
		# circle2_y.append(float("{0:.3f}".format(float(path_y[k]))))
	new_x = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
	# print (circle2_x)
	# print ("5: " + str(dz.data))
	# new_y = ColumnDataSource(data=dict(x1=circle2_x, y1=circle2_y))
	# new_line = ColumnDataSource(data=dict(x1=path_x, y1=path_y))
	ds.data = new_x.data
	# print ("6: " + str(dz.data))
	# dz.data = new_y.data
	# da.data = new_line.data
	# print (da.data)
	# print ("7: " + str(dz.data))
	# print (dz.data)
	i += 1
	# print ("8: " + str(dz.data))
	if (i == len(xlist) - 1) or (i == len(ylist) - 1):
		i = 0
# print (y1.data)
p.circle('x1', 'y1', size=15, color="navy", alpha=0.5, name="robot_circle", source=x1)
p.circle('x1', 'y1', size=15, color="red", alpha=0.5, name="predicted_circle", source=y1)
p.line('x1', 'y1', line_width=3, color="red", name="predicted_line", source=line1)

renderer = p.select(dict(name="robot_circle"))
enderer = p.select(dict(name="predicted_circle"))
derer = p.select(dict(name="predicted_line"))
ds = renderer[0].data_source
dz = enderer[0].data_source
da = derer[0].data_source
# print (dz.data)
l = layout([select1],
			[p])
curdoc().add_root(l)
curdoc().add_periodic_callback(update, 100)


# show(p)





