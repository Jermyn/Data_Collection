import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse
import operator
import datetime
import csv
import json
from pprint import pprint
import math
import urllib3
import pandas as pd
import json, requests, time


from bokeh.charts import HeatMap, Bar, BoxPlot
from bokeh.layouts import column, gridplot, row, layout
from bokeh.palettes import RdYlGn6, RdYlGn9, YlOrRd9
from bokeh.sampledata.autompg import autompg as df
from bokeh.sampledata.unemployment1948 import data
from bokeh.models import LogColorMapper, LogTicker, ColorBar, HoverTool, ColumnDataSource, LabelSet, BoxSelectTool
from bokeh.io import curdoc, show, output_file
from bokeh.models.widgets import Select, Button, TextInput, RadioButtonGroup
from storePOI import actlab_POI
# from Main_server import pull_data
import operator


avg_lat = 0.0
avg_lng = 0.0
count = 0
scalenum = 0
actual = []
CoList = []
devList = []
data_cal = []
data_bary = []
data_oys = []
data_y2 = []
bar_cal = []
bar_bary = []
bar_oys = []
bar_y2 = []
contact = []
errorList = []
final_list = []
temp = []
Algo = []
error = []
dev_cal = []
dev_bary = []
dev_oys = []
dev_y2 = []
callat = []
callng = []
barylat = []
barylng = []
oyslat = []
oyslng = []
y2lat = []
y2lng = []
devices_cal = []
devices_bary = []
devices_oys = []
devices_y2 = []
update_list = []
device = []
data_dict = {}
calPath = "/Users/jermz/Desktop/Python/Auto-cal/Mean.csv"
baryPath = "/Users/jermz/Desktop/Python/Barycentric/Mean.csv"
oysPath = "/Users/jermz/Desktop/Python/Nlsql_oys/Mean.csv"
y2Path = "/Users/jermz/Desktop/Python/Nlsql_y2/Mean.csv"


# history_write = open('/Users/jermz/Desktop/Python/Auto-cal/history_compiled.csv', 'w')
# history_write.write("deviceId, lat, lng\n")
# print df

def getScale():
	query_scale = 'query{map (id:"actlab") {scale}}'
	r = requests.get("http://137.132.165.139/graphql", {"query":query_scale})
	scale = r.text
	scale_json = json.loads(scale)
	return int(scale_json['data']['map']['scale'])

def extract_write_file(filename):
	with open(filename,'r') as csvfile:
		next(csvfile)
		plots = csv.reader(csvfile, delimiter=',')
		for row in plots:
			for k in range(0, 3):
				#next(csvfile)
				actual.append((row[k].replace(' ', '')))		
			# x.append((row[0]))
			# y.append((row[1]))  
		# print actual	
		for j in range(0, len(actual)):
				if j%3==0:
					devList.append(actual[j])		  	
# extract_write_file('TP_Actual.txt')	

def file_to_list(filename):
	reader_pre = csv.reader(open(filename), delimiter=",")
	next(reader_pre)
	sortedlist = sorted(reader_pre, key=operator.itemgetter(0), reverse=False)
	return sortedlist

# auto_cal_list = file_to_list(calPath)
# barycentric_list = file_to_list(baryPath)
# Nlsql_oys_list = file_to_list(oysPath)
# Nlsql_y2_list = file_to_list(y2Path)

def store_rawdata(raw_list, datalat_list, datalng_list):
	deviceslist = []
	for i in range(0, len(raw_list)):
		datalat_list.append(float("{0:.3f}".format(float(raw_list[i][1])*scalenum)))
		datalng_list.append(float("{0:.3f}".format(float(raw_list[i][2])*scalenum)))
		deviceslist.append(raw_list[i][0])
	return deviceslist	
# devices_cal = store_rawdata(auto_cal_list, callat, callng)
# devices_bary = store_rawdata(barycentric_list, barylat, barylng)
# devices_oys = store_rawdata(Nlsql_oys_list, oyslat, oyslng)
# devices_y2 = store_rawdata(Nlsql_y2_list, y2lat, y2lng)	
# print devices_cal


def write_file( _list, pathname):
	global avg_lat
	global avg_lng

	index =0
	prevCount=0
	for i in range(0, len(_list)):
		strDev = _list[i][0].replace(' ', '')
		if i==0:
			if strDev==devList[index]:
				currentDevice = strDev
				index+=1

		if strDev==currentDevice:
			avg_lat+=float(_list[i][1])
			avg_lng+=float(_list[i][2])
		else:
			#calculation
			avg_lat/=(i-prevCount)
			avg_lng/=(i-prevCount)
			for j in range(0, len(actual)):
				if j%3==0:
					if currentDevice==actual[j]:
						actual_lat=float(actual[j+1])
						actual_lng=float(actual[j+2])
						error_dist=math.sqrt((pow((actual_lat-avg_lat),2)+pow((actual_lng-avg_lng),2)))*scalenum
			# history_write.write(currentDevice + ", " + repr(error_dist) + "\n")
			if "Auto-cal" in pathname:
				strInsert = currentDevice + ", " + repr(error_dist) + ", Auto-cal"
			elif "Barycentric" in pathname:
				strInsert = currentDevice + ", " + repr(error_dist) + ", Barycentric"
			elif "oys" in pathname:
				strInsert = currentDevice + ", " + repr(error_dist) + ", Nlsql_oys"
			else:
				strInsert = currentDevice + ", " + repr(error_dist) + ", Nlsql_y2"
			errorList.append(strInsert.split(", "))

			# history_write.write(strInsert)
			if int(strDev)>200:
				break

			if strDev==devList[index]:
				currentDevice = strDev
				prevCount=i
				index+=1
				avg_lat = 0
				avg_lng = 0	
				i-=1
	# return errorList			
# write_file(auto_cal_list, calPath)
# write_file(barycentric_list, baryPath)
# write_file(Nlsql_y2_list, y2Path)
# write_file(Nlsql_oys_list, oysPath)
# print errorList[0][2]

def compile_list(final):
	devices = []
	for i in range(0, len(final)):
		# list1.append(final[i][1])
		# list2.append(final[i][2])
		devices.append(final[i][0])
	return devices	
# devices = compile_list(error, Algo, devices, errorList)
# print Algo

def rearrange_list_algo(_list, strDev1, strDev2):
	temp = []
	index = 0
	for i in range(0, len(_list)):
		if _list[i][0] == strDev1:
			index = i
		if _list[i][0] == strDev2:
			_list[index], _list[i] = _list[i], _list[index]
	return _list		

def rearrange(_list, list_arranged):
	arrange1 = 0
	arrange2 = 0
	list_arranged = rearrange_list_algo(errorList, '100', '103')
	list_arranged = rearrange_list_algo(errorList, '101', '102')
	list_arranged = rearrange_list_algo(errorList, '108', '111')
	list_arranged = rearrange_list_algo(errorList, '109', '110')
	list_arranged = rearrange_list_algo(errorList, '120', '123')
	list_arranged = rearrange_list_algo(errorList, '121', '122')
	list_arranged = rearrange_list_algo(errorList, '124', '127')
	list_arranged = rearrange_list_algo(errorList, '125', '126')
	return list_arranged	
# final_list = rearrange(devList, temp)
# print final_list



def compute_write_file(_list):
	# with open(filename,'r') as csvfile:
	# 	next(csvfile)
	# 	plots = csv.reader(csvfile, delimiter=',')
	# 	for row in plots:
	for i in range(0, len(_list)):
		if _list[i][2] == "Auto-cal":
			data_cal.append(float("{0:.3f}".format(float(_list[i][1]))))
			error.append(float("{0:.1f}".format(float(_list[i][1]))))
			dev_cal.append(_list[i][0])
		elif _list[i][2] == "Barycentric":
			data_bary.append(float("{0:.3f}".format(float(_list[i][1]))))
			error.append(float("{0:.1f}".format(float(_list[i][1]))))
			dev_bary.append(_list[i][0])
		elif _list[i][2] == "Nlsql_y2":
			data_y2.append(float("{0:.3f}".format(float(_list[i][1]))))
			error.append(float("{0:.1f}".format(float(_list[i][1]))))		
			dev_y2.append(_list[i][0])
		else:
			data_oys.append(float("{0:.3f}".format(float(_list[i][1]))))
			error.append(float("{0:.1f}".format(float(_list[i][1]))))
			dev_oys.append(_list[i][0])
		Algo.append(_list[i][2])
# 	print (len(data_cal))	
		# devices.append(_list[i][0])	
# compute_write_file(final_list)
# print data_cal
# print devices

def prepare_dict(dev):
	errdict = {	
			'Auto-cal' : data_cal,
			'Barycentric' : data_bary,
			'Nlsql_oys' : data_oys,
			'Nlsql_y2' : data_y2
	}

	
	data_dict['devices'] = []
	data_dict['value'] = []
	data_dict['group-name'] = []

	for group, group_list in errdict.items():
		index = 0
		for item in group_list:
			# print dev[index]
			data_dict['devices'].append(dev[index])
			data_dict['value'].append(item)
			data_dict['group-name'].append(group)
			index += 1
	return data_dict					


# main_write = open('/Users/jermz/Desktop/eclipse-workspace/Data_Collection/heatmap_app/data.csv', 'w')
# main_write.write("deviceId, lat, lng\n")
file = []
# print devList
def query_server():
    query_id = '{devices{id}}'
    query_lat = '{devices{lat}}'
    query_lng = '{devices{lng}}'
    r = requests.get("http://137.132.165.139/graphql", {"query":query_id})
    s = requests.get("http://137.132.165.139/graphql", {"query":query_lat})
    z = requests.get("http://137.132.165.139/graphql", {"query":query_lng})
    
    strid = r.text
    strlat = s.text
    strlng = z.text
    id = json.loads(strid)
    lat = json.loads(strlat)
    lng = json.loads(strlng)
    
    for i in range(0, len(id['data']['devices'])):
        for j in range(0, len(devList)):
            if str(id['data']['devices'][i]['id']) == devList[j]:
                strData = str(id['data']['devices'][i]['id']) + ", " + str(lat['data']['devices'][i]['lat']) + ", " + str(lng['data']['devices'][i]['lng'])
                file.append(strData.split(", "))
#                 history_write.write(str(id['data']['devices'][i]['id']) + ", " + str(lat['data']['devices'][i]['lat']) + ", " + str(lng['data']['devices'][i]['lng']) + "\n")
    return file
def wait_second():
    time.sleep(1)
def pull_data(duration):
	main_write = open('data.csv', 'w')
	main_write.write("deviceId, lat, lng\n")
	data = []
	_data = []
	print ("Pulling data...")
	for i in range(0, duration):
	    data.append(query_server())
	    wait_second()
	_data = sorted(data[0])
	print ("Pull finish...")
	for j in range(0, len(_data)):
	    for k in range(0, 3):
	        if k<2:
	            main_write.write(_data[j][k] + ", ")
	        else:
	            main_write.write(_data[j][k] + "\n")    
# pull_data(5)

# def run(filename):
# 	calPath = "/Users/jermz/Desktop/Python/Auto-cal/Mean.csv"
# 	baryPath = "/Users/jermz/Desktop/Python/Barycentric/Mean.csv"
# 	oysPath = "/Users/jermz/Desktop/Python/Nlsql_oys/Mean.csv"
# 	y2Path = "/Users/jermz/Desktop/Python/Nlsql_y2/Mean.csv"
scalenum = getScale()
devList = actlab_POI()
# extract_write_file('TP_actual.txt')	
auto_cal_list = file_to_list(calPath)
barycentric_list = file_to_list(baryPath)
Nlsql_oys_list = file_to_list(oysPath)
Nlsql_y2_list = file_to_list(y2Path)
devices_cal = store_rawdata(auto_cal_list, callat, callng)
devices_bary = store_rawdata(barycentric_list, barylat, barylng)
devices_oys = store_rawdata(Nlsql_oys_list, oyslat, oyslng)
devices_y2 = store_rawdata(Nlsql_y2_list, y2lat, y2lng)	
write_file(auto_cal_list, calPath)
write_file(barycentric_list, baryPath)
write_file(Nlsql_y2_list, y2Path)
write_file(Nlsql_oys_list, oysPath)
device = compile_list(errorList)
final_list = rearrange(devList, temp)
compute_write_file(final_list)
actual_dict = prepare_dict(device)
final_range = int(len(final_list)/4)
	# compile_heatmap(final_range, final_list, actual_dict, device, data_cal, data_bary, data_oys, data_y2, bar_cal, bar_bary, bar_oys, bar_y2, devices_cal, devices_bary, devices_oys, devices_y2, callat, callng, barylat, barylng, oyslat, oyslng, y2lat, y2lng)
	# return final_range
	
# range_f = run('TP_Actual.txt')	
# print range_f
# def compile_heatmap(numDev, flist, act_dict, list_device, data_c, data_b, data_o, data_y, bar_c, bar_b, bar_o, bar_y, cal1, bary1, oys1, y21, clat, clng, blat, blng, olat, olng, ylat, ylng):
region = []
xlist = []
ylist = []
area = []
temp_list = []
algorithm = []

algorithm.append('Nlsql_oys')
algorithm.append('Nlsql_y2')
algorithm.append('Barycentric')
algorithm.append('Auto-cal')

# range_f = int(len(final_list)/4)

prev_heatmap_reg = 1
heatmap_x = 0
heatmap_y = 0

for i in range(0, final_range):
	temp_list.append(final_list[i][0])
	if prev_heatmap_reg > 0:
		if (prev_heatmap_reg < heatmap_y) or (prev_heatmap_reg == 1):	
			if (final_range%prev_heatmap_reg) == 0:
				heatmap_x = prev_heatmap_reg
				heatmap_y = int(final_range/heatmap_x)
			prev_heatmap_reg += 1
		else:
			prev_heatmap_reg = 0	
	
	
for k in range(0, heatmap_y):
	for j in range(0, heatmap_x):
		strpost = chr(65 + k)
		strpre = chr(65 + j)
		region.append('region' + strpost)
		area.append('beacon' + strpre)
		xlist.append(k+1)
		ylist.append(j+1)

Cal = pd.DataFrame()
Cal['region'] = region
Cal['data'] = data_cal
Cal['area'] = area									

Bary = pd.DataFrame()
Bary['region'] = region
Bary['data'] = data_bary
Bary['area'] = area	

oys = pd.DataFrame()
oys['region'] = region
oys['data'] = data_oys
oys['area'] = area	

y2 = pd.DataFrame()
y2['region'] = region
y2['data'] = data_y2
y2['area'] = area

box = {
					'Algorithm' : Algo,
					'Error Distance' : error,
					'z' : device
}

box_callat = {
					'Devices' : devices_cal,
					'Error Distance' : callat
}

box_callng = {
					'Devices' : devices_cal,
					'Error Distance' : callng
}

box_barylat = {
					'Devices' : devices_bary,
					'Error Distance' : barylat
}

box_barylng = {
					'Devices' : devices_bary,
					'Error Distance' : barylng
}

box_oyslat = {
					'Devices' : devices_oys,
					'Error Distance' : oyslat
}

box_oyslng = {
					'Devices' : devices_oys,
					'Error Distance' : oyslng
}

box_y2lat = {
					'Devices' : devices_y2,
					'Error Distance' : y2lat
}

box_y2lng = {
					'Devices' : devices_y2,
					'Error Distance' : y2lng
}

source_cal = ColumnDataSource(data=dict(x=xlist,
										y=ylist,
										value=data_cal))
source_bary = ColumnDataSource(data=dict(x=xlist,
										y=ylist,
										value=data_bary))
source_oys = ColumnDataSource(data=dict(x=xlist,
										y=ylist,
										value=data_oys))
source_y2 = ColumnDataSource(data=dict(x=xlist,
									   y=ylist,
									   value=data_y2))
source_dev1 = ColumnDataSource(data=dict(x=xlist,
										 y=ylist,
										 value=temp_list))

select1 = Select(title="Algorithm:", value=algorithm[0], options=algorithm, width=100)

def callback():
	global calPath, data_cal
	algor = str(select1.value)
	pull_data(5)
	print ("Starting...")
	
	# print (calPath)
	# print (algor)
	if algor in calPath:
		calPath = "/Users/jermz/Desktop/eclipse-workspace/Data_Collection/heatmap_app/data.csv"
		data_cal = []
		auto_cal_list = file_to_list(calPath)
		print (1)
		devices_cal = store_rawdata(auto_cal_list, callat, callng)
# 		print (len(data_cal))
		print (2)
		write_file(auto_cal_list, calPath)
		print (3)
# 		print (len(data_cal))
		device = compile_list(errorList)
		print (4)
		final_list = rearrange(devList, temp)
		print (5)
		compute_write_file(final_list)
		print (6)
		actual_dict = prepare_dict(device)
		print (7)
		Cal['data'] = data_cal
		print (8)
		new_map = HeatMap(Cal, x='region', y='area', values='data', legend=False, stat=None, palette=YlOrRd9, width = 550, plot_height=500, title="Auto-cal Test")
		print (9)
		
		hm11 = new_map
		print (10)
		
# 		print (labels_cal1)
		print (12)
# 		hm11.add_layout(labels_cal1)
		print (13)
# 		new_map.add_layout(labels_dev)
		print (14)
		hm11.axis.visible = False
		print (15)
		heatmaprow1.children[0] = hm11
		source_cal.data['value'] = data_cal
		print (11)
		labels_cal.source = source_cal
		print (16)
		l.children = [widgetrow,
						heatmaprow1,
						heatmaprow2]
# 		print (len(data_cal))
		# final_range = int(len(final_list)/4)
	elif algor in baryPath:
		baryPath = "/Users/jermz/Desktop/eclipse-workspace/Data_Collection/heatmap_app/data.csv"
		barycentric_list = file_to_list(baryPath)
		devices_bary = store_rawdata(barycentric_list, barylat, barylng)
		write_file(barycentric_list, baryPath)
	elif algor in oysPath:
		oysPath = "/Users/jermz/Desktop/eclipse-workspace/Data_Collection/heatmap_app/data.csv"
		Nlsql_oys_list = file_to_list(oysPath)
		devices_oys = store_rawdata(Nlsql_oys_list, oyslat, oyslng)
		write_file(Nlsql_oys_list, oysPath)
	else:
		y2Path = "/Users/jermz/Desktop/eclipse-workspace/Data_Collection/heatmap_app/data.csv"	
		Nlsql_y2_list = file_to_list(y2Path)
		devices_y2 = store_rawdata(Nlsql_y2_list, y2lat, y2lng)
		write_file(Nlsql_y2_list, y2Path)	
	print ("End...")
	# extract_write_file('TP_actual.txt')	
	# auto_cal_list = file_to_list(calPath)
	# barycentric_list = file_to_list(baryPath)
	# Nlsql_oys_list = file_to_list(oysPath)
	# Nlsql_y2_list = file_to_list(y2Path)
	# devices_cal = store_rawdata(auto_cal_list, callat, callng)
	# devices_bary = store_rawdata(barycentric_list, barylat, barylng)
	# devices_oys = store_rawdata(Nlsql_oys_list, oyslat, oyslng)
	# devices_y2 = store_rawdata(Nlsql_y2_list, y2lat, y2lng)	
	# write_file(auto_cal_list, calPath)
	# write_file(barycentric_list, baryPath)
	# write_file(Nlsql_y2_list, y2Path)
	# write_file(Nlsql_oys_list, oysPath)
	# device = compile_list(errorList)
	# final_list = rearrange(devList, temp)
	# compute_write_file(final_list)
	# actual_dict = prepare_dict(device)
	# final_range = int(len(final_list)/4)

labels_cal = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=-8, source=source_cal, render_mode='canvas')                  
labels_cal.text_color = 'black'  
labels_cal.text_font_style = 'italic' 
labels_cal1 = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=-8, source=source_cal, render_mode='canvas')                  
labels_cal1.text_color = 'black'  
labels_cal1.text_font_style = 'italic' 
labels_bary = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=-8, source=source_bary, render_mode='canvas')                  
labels_bary.text_color = 'black'  
labels_bary.text_font_style = 'italic' 
labels_oys = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=-8, source=source_oys, render_mode='canvas')                  
labels_oys.text_color = 'black'  
labels_oys.text_font_style = 'italic' 
labels_y2 = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=-8, source=source_y2, render_mode='canvas')                  
labels_y2.text_color = 'black'  
labels_y2.text_font_style = 'italic' 
labels_dev = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=5, source=source_dev1, render_mode='canvas')    
labels_dev.text_color = 'blue'  
labels_dev.text_font_style = 'italic'
labels_dev1 = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=5, source=source_dev1, render_mode='canvas')    
labels_dev1.text_color = 'blue'  
labels_dev1.text_font_style = 'italic'
labels_dev2 = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=5, source=source_dev1, render_mode='canvas')    
labels_dev2.text_color = 'blue'  
labels_dev2.text_font_style = 'italic'    
labels_dev3 = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=5, source=source_dev1, render_mode='canvas')    
labels_dev3.text_color = 'blue'  
labels_dev3.text_font_style = 'italic'    
labels_dev4 = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=5, source=source_dev1, render_mode='canvas')    
labels_dev4.text_color = 'blue'  
labels_dev4.text_font_style = 'italic'    

hm11 = HeatMap(Cal, x='region', y='area', values='data', legend=False, stat=None, palette=YlOrRd9, width = 550, plot_height=500, title="Auto-cal Test")
hm12 = Bar(data_dict, values='value', label='devices', group='group-name', legend='top_right', title='Error Distance for Respective Regions', width = 1100, plot_height = 700)
hm13 = BoxPlot(box, values='Error Distance', label='Algorithm', legend=False, title='Error Distance Boxplot', width = 900, plot_height=600)
hm14 = HeatMap(Bary, x='region', y='area', values='data', legend=False, stat=None, palette=YlOrRd9, width = 550, plot_height=500, title="Barycentric Test")
hm15 = HeatMap(oys, x='region', y='area', values='data', legend=False, stat=None, palette=YlOrRd9, width = 550, plot_height=500, title="Nlsql_oys Test")
hm16 = HeatMap(y2, x='region', y='area', values='data', legend=False, stat=None, palette=YlOrRd9, width = 550, plot_height=500, title="Nlsql_y2 Test")
hm17 = BoxPlot(box_callat, values='Error Distance', label='Devices', legend=False, title='Auto-cal Latitude Boxplot', width = 550, plot_height=600)
hm18 = BoxPlot(box_callng, values='Error Distance', label='Devices', legend=False, title='Auto-cal Longtitude Boxplot', width = 550, plot_height=600)
hm19 = BoxPlot(box_barylat, values='Error Distance', label='Devices', legend=False, title='Barycentric Latitude Boxplot', width = 550, plot_height=600)
hm20 = BoxPlot(box_barylng, values='Error Distance', label='Devices', legend=False, title='Barycentric Longtitude Boxplot', width = 550, plot_height=600)
hm21 = BoxPlot(box_oyslat, values='Error Distance', label='Devices', legend=False, title='Nlsql_oys Latitude Boxplot', width = 550, plot_height=600)
hm22 = BoxPlot(box_oyslng, values='Error Distance', label='Devices', legend=False, title='Nlsql_oys Longtitude Boxplot', width = 550, plot_height=600)
hm23 = BoxPlot(box_y2lat, values='Error Distance', label='Devices', legend=False, title='Nlsql_y2 Latitude Boxplot', width = 550, plot_height=600)
hm24 = BoxPlot(box_y2lng, values='Error Distance', label='Devices', legend=False, title='Nlsql_y2 Longtitude Boxplot', width = 550, plot_height=600)




refresh = Button(label="Refresh", button_type="success")
refresh.on_click(callback)


hm11.add_layout(labels_cal)
hm11.add_layout(labels_dev1)
hm14.add_layout(labels_bary)
hm14.add_layout(labels_dev2)
hm15.add_layout(labels_oys)
hm15.add_layout(labels_dev3)
hm16.add_layout(labels_y2)
hm16.add_layout(labels_dev4)


# output_file("Heatmap.html")
hm11.axis.visible = False
hm14.axis.visible = False
hm15.axis.visible = False
hm16.axis.visible = False

widgetrow = row(select1, refresh)
heatmaprow1 = row(children=[hm11, hm14])
heatmaprow2 = row(children=[hm15, hm16])
l = layout(children=[[widgetrow],
			[heatmaprow1],
			[heatmaprow2]])
# l = layout([
# 	[select1, refresh],
# 	[hm11, hm14],
# 	[hm15, hm16],
#   	[hm12],
# 	[hm13],
# 	[hm17, hm18],
# 	[hm19, hm20],
# 	[hm21, hm22],
# 	[hm23, hm24]
# ])

# 	return hm11
curdoc().add_root(l)
# 	curdoc().add_periodic_callback(update_data,1000)
# show(l)
# 	show(column(
# 		 gridplot(hm11, hm14, hm15, hm16, hm12, hm13, hm17, hm18, hm19, hm20, hm21, hm22, hm23,
# 							ncols=1, plot_width=400, plot_height=400)
# 	 ))           
# compile_heatmap()
	
# getScale()
