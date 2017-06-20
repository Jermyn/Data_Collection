import base64
import requests
# import urllib3
import json
from bokeh.plotting import figure, show, output_file
from storePOI import office_POI, ward5_POI
from storeScale import getScale
import csv, operator
import datetime
from bokeh.io import curdoc
from bokeh.models.sources import ColumnDataSource
import pandas as pd
from bokeh.models.tools import HoverTool

coord_lat_list = []
coord_lng_list = []
temp = []
center = []
xlist = []
ylist = []
circle_x = []
circle_y = []
coord_total_list = []
i = 1

center = ward5_POI()
map_scale = getScale("ward5")
# reader = csv.reader(open("parsed.csv"), delimiter=",")
# next(reader)
# sortedlist = sorted(reader, key=operator.itemgetter(0), reverse=False)
# for i in range(0, len(sortedlist)):
# 	sortedlist[i][0] = datetime.datetime.fromtimestamp(int(sortedlist[i][0])).strftime("%Y-%m-%d %H:%M:%S")
# 	sortedlist[i][1] = (float(sortedlist[i][1]) - (float(center[0][1]) * int(map_scale))) / int(map_scale)
# 	sortedlist[i][2] = (float(sortedlist[i][2]) - (float(center[0][2]) * int(map_scale))) / int(map_scale)
# print (sortedlist)    
query_image = 'query{map (id:"ward5") {image}}'
query_coordinates = 'query{map (id:"ward5") {coordinates}}'
r = requests.get("http://137.132.165.139/graphql", {"query":query_image})
s = requests.get("http://137.132.165.139/graphql", {"query":query_coordinates})
coor = s.text
cod = json.loads(coor)
image = r.text
img = json.loads(image)
# print (img['data']['map']['image'])
# print (image)

imgdata = base64.b64decode(img['data']['map']['image'])
filename = 'ward5Image.png'
with open(filename, 'wb') as f:
	f.write(imgdata)
# fh.close()

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
#  	for k in range(0, len(coord_lng_list)):
	coord_total_list = coord_lng_list + coord_lat_list
# 
# # print (coord_total_list)
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
min_pt, max_pt = findMinimum_Maximum(coord_total_list)
min_x, max_x = findMinimum_Maximum(coord_lng_list)
min_y, max_y = findMinimum_Maximum(coord_lat_list)
# # min_pt = min(coord_total_list)
# # max_pt = max(coord_total_list)
# # min_pt = float("{0:.3f}".format(float(min_pt)))
# # max_pt = float("{0:.3f}".format(float(max_pt)))
# max_y = max(coord_lat_list)
# min_y = min(coord_lat_list)
# max_x = max(coord_lng_list)
# min_x = min(coord_lng_list)
# max_y = float("{0:.3f}".format(float(max_y)))	
# max_x = float("{0:.3f}".format(float(max_x)))
# min_x = float("{0:.3f}".format(float(min_x)))
# min_y = float("{0:.3f}".format(float(min_y)))
# print (min_pt)
# for k in range(0, len(sortedlist)):
# 	xlist.append("{0:.3f}".format(float(sortedlist[k][1])))
# 	ylist.append("{0:.3f}".format(float(sortedlist[k][2])))
# # print (ylist)
output_file('ward5_1.html')
p = figure(x_range=(min_pt, max_pt), y_range=(min_pt, max_pt))
p.image_url(url=['http://i.imgur.com/G52LVgB.png'], x=min_x, y=min_y, w=(max_x - min_x), h=(max_y - min_y), anchor="bottom_left")
# p.line(xlist, ylist, line_width=3)
# circle_x.append(float("{0:.3f}".format(float(xlist[0]))))
# circle_y.append(float("{0:.3f}".format(float(ylist[0]))))
# x1 = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
# 
# # print (x1)
# # x1 = float("{0:.3f}".format(float(xlist[0])))
# # y1 = float("{0:.3f}".format(float(ylist[0])))
# x2 = float("{0:.3f}".format(float(xlist[len(xlist) - 1])))
# y2 = float("{0:.3f}".format(float(ylist[len(ylist) - 1])))
# 
def update():
	global i
	circle_x = []
	circle_y = []
	circle_x.append(float("{0:.3f}".format(float(xlist[i]))))
	circle_y.append(float("{0:.3f}".format(float(ylist[i]))))
	new_x = ColumnDataSource(data=dict(x1=circle_x, y1=circle_y))
	ds.data = new_x.data
	i += 1
	if (i == len(xlist) - 1) or (i == len(ylist) - 1):
		i = 0
 
# p.circle('x1', 'y1', size=15, color="navy", alpha=0.5, name="start_circle", source=x1)
# # p.circle(x2, y2, size=10, color="red", alpha=0.5, name="end_circle", source=y1)
# renderer = p.select(dict(name="start_circle"))
# # print (renderer)
# 
# ds = renderer[0].data_source
# # print (ds.data)
# # print (ds)
# curdoc().add_root(p)
# # curdoc().add_periodic_callback(update, 100)
show(p)


