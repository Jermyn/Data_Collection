import csv
import operator
import requests
import pandas as pd
import codecs
import dateutil.relativedelta
from datetime import datetime
from contextlib import closing
from bokeh.io import curdoc
from bokeh.io import output_file, show
from bokeh.models.widgets import Select, Button, TextInput, RadioButtonGroup
from bokeh.layouts import row, column, layout
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, Toggle, HTMLTemplateFormatter
from bokeh.charts import Scatter



devList = []
selectList = []
dict_contact = {}
real_data = {}
changed_data = {}
sortedlist = []

sort_list = []					
timeline = []
datesList = []
dateEndList = []			

count = 0
diff = 0
def download_csv():
	contact_csv = open('contacttable.csv', 'w')
	global count, diff, timeline
	csv_url = 'http://137.132.165.139/api/contacts'
	
	with closing(requests.get(csv_url, stream=True)) as r:
		reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8'), delimiter=',', quotechar='"')
		next(reader)
		for row in reader:
			# count += 1
			timeline.append(row[5])
			# timeline = sorted(timeline)
			
			time = datetime.datetime.fromtimestamp(int(row[5])/1000).strftime("%Y-%m-%d %H:%M:%S")
			second_time = datetime.datetime.fromtimestamp(int(row[6])/1000).strftime("%Y-%m-%d %H:%M:%S")
			row[5] = str(time)
			row[6] = str(second_time)
			if len(timeline) > 2:
				timeline = sorted(timeline)
				latest_time = datetime.datetime.fromtimestamp(int(timeline[0])/1000)
				first_time = datetime.datetime.fromtimestamp(int(timeline[len(timeline)-1])/1000)
				print ("Latest:" + str(latest_time) + "\nFirst:" + str(first_time))
				rd = dateutil.relativedelta.relativedelta (first_time, latest_time)
				diff = rd.days
				# diff = ((int(timeline[len(timeline)-1])/1000) - (int(timeline[1])/1000))/5184000
				# print (diff)
				print ("Days:" + str(rd.days) + "\n")
				
			# print (row)
		# decoded_content = download.content.decode('utf-8')
		# cr = csv.reader(decoded_content.splitlines(), delimiter=',')
		# my_list = list(cr)
		
		# for row in my_list:
			# print ("Starting..\n")
			contact_csv.write(str(", ".join(str(e) for e in row)).strip('"\'"') + "\n")
			if diff == 1:
				break
			# if count == 999:
			# 	break
			

# download_csv()
def compile_table():
	global devList, sortedlist, datesList
	# contactFile = open(filename, 'w')

	reader = csv.reader(open("contacttable.csv"), delimiter=",")
	# next(reader)
	sortedlist = sorted(reader, key=operator.itemgetter(7), reverse=True)	
	# print (sortedlist)
	initial_dev = sortedlist[0][1]
	# print (initial_dev + "\n")
	# devList.append("Select device...")
	devList.append(initial_dev.replace(" ", ""))
	# print (devList)
	for i in range(1, len(sortedlist)):
		# print ("listDev:" + sortedlist[i][1])
		# print ("device:" + initial_dev)
	# 	# sortedlist[i][1] = str(sortedlist[i][1]).replace(' ', '')
	# 	# temp = float(sortedlist[i][2]) * (277 * pow(10, (-9)))
	# 	# sortedlist[i][2] = str(float("{0:.3f}".format(temp)))
		if (sortedlist[i][1].replace(" ", "")) not in devList:
			initial_dev = sortedlist[i][1]
			devList.append(str(initial_dev).replace(" ", ""))
		
	devList = sorted(devList)
	devList.insert(0, "Select device...")
	strList = sortedlist[0][5].split(" ")
	strInitial_Date = strList[1]
	datesList.append(strInitial_Date)
	strEndList = sortedlist[0][6].split(" ")
	strEndDate = strEndList[1]
	# strList = []
	for j in range(1, len(sortedlist)):
		strList = sortedlist[j][5].split(" ")
		strEndList = sortedlist[j][6].split(" ")
		if strList[1] not in datesList:
			datesList.append(strList[1])
		if strEndList[1] not in dateEndList:
			dateEndList.append(strEndList[1])	
	# contactFile.write("Device, ")
	# for j in range(0, len(devList)):
	# 	dict_contact[devList[j]] = {}
	# 	strDev = devList[j]
	# 	if j != len(devList)-1:
	# 		contactFile.write(str(strDev) + ", ")
	# 	else:
	# 		contactFile.write(str(strDev) + "\n")
	
	# for i in range(0, len(sortedlist)):
		
	# 	if sortedlist[i][0]!=initial_dev:
	# 		initial_dev = sortedlist[i][0]
			

	# 	dict_contact[initial_dev][sortedlist[i][1]] = sortedlist[i][2]	
		

	# for j in range(0, len(devList)):		
	# 	dict_contact[str(devList[j])][str(devList[j])] = 'NA'
	
	# for k in range(0, len(devList)):
	# 	contactFile.write(str(devList[k]) + ", ")
	# 	for n in range(0, len(devList)):
	# 		if devList[k] == devList[n]:
	# 			contactFile.write(str(dict_contact[str(devList[k])][str(devList[n])]) + ", ")
	# 		else:
				
	# 			if n != len(devList)-1:
	# 				try:
	# 					contactFile.write(str(dict_contact[str(devList[k])][str(devList[n])]) + ", ")
	# 				except:
	# 					dict_contact[str(devList[k])][str(devList[n])] = 'Empty'
	# 					contactFile.write(str(dict_contact[str(devList[k])][str(devList[n])]) + ", ")
	# 			else:
	# 				try:
	# 					contactFile.write(str(dict_contact[str(devList[k])][str(devList[n])]) + "\n")
	# 				except:
	# 					dict_contact[str(devList[k])][str(devList[n])] = 'Empty'
	# 					contactFile.write(str(dict_contact[str(devList[k])][str(devList[n])]) + "\n")

compile_table()
# print (devList)
# data_list = []

		# strInitial_Date = strList[1]
	# print (sortedlist[j][5])
# print (dateEndList)
# strData = ""
# real_data['devices'] = [devList[i] for i in range(len(devList))]
# selectList.append("Select all...")

# for k in range(0, len(devList)):
# 	real_data['distances_' + str(devList[k])] = []
# 	selectList.append(str(devList[k]))
	
# for i in range(1, len(selectList)):
# 	for a in range(1, len(selectList)):
# 		if a !=len(selectList):
# 			strData += str(dict_contact[selectList[a]][selectList[i]]) +", "
# 		else:
# 			strData = str(dict_contact[selectList[a]][selectList[i]]) + "\n"
  
# 	data_list.append(strData.split(", "))
# 	real_data['distances_' + selectList[i]] = strData.split(", ")
# 	strData = ""	

# source = ColumnDataSource(real_data)
# template="""
# <div style="background:<%= 
#     (function colorfromint(){
#         if(value < 2){
#             return("blue")}
#         else{return("red")}
#         }()) %>; 
#     color: white"> 
# <%= value %></div>
# """

# formater =  HTMLTemplateFormatter(template=template)
       
# columns = [
# 	TableColumn(field="devices", title="Devices")]

# for i in range(1, len(selectList)):
# 	columns.append(TableColumn(field="distances_" + selectList[i], title = selectList[i]))
   
select1 = Select(title="DeviceID:", value=devList[0], options=devList, width=100)
select2 = Select(title="DeviceID:", value=devList[0], options=devList, width=100)
select3 = Select(title="Start Date:", value=datesList[0], options=datesList, width=100)
select4 = Select(title="End Date:", value=dateEndList[0], options=dateEndList, width=100)
radio_button_group = RadioButtonGroup(
        labels=["One to One", "All in contact"], active=1)
   
labelValue=" "

   
def callback():
	dev1list = []
	dev2list = []
	latlist = []
	lnglist = []
	stimelist = []
	etimelist = []
	duration = []
	strDevice = ""
	strFixed = ""
	r = select1.value
	c = select2.value
	d = select3.value
	print (r)
	print (c)
	print (radio_button_group.active)
	# if (r == "Select all...") or (c == "Select all..."):
	# 	data_table.width = 2200
	# 	data_table.columns = columns
	# 	data_table.source = source
		
	
	# text_input.value = dict_contact[str(r)][str(c)]
	if radio_button_group.active == 0:
		for i in range(0, len(sortedlist)):
			if (r==sortedlist[i][1].replace(" ", "")) and (c==sortedlist[i][2].replace(" ", "")):
				# input_date = datetime.strptime((d + " , '%Y-%m-%d %H:%M:%S')
				strDate = sortedlist[i][5]
				dev1list.append(r)
				dev2list.append(c)
				temp = float(sortedlist[i][3].replace(" ", ""))*27
				latlist.append("{0:.3f}".format(temp))
				temp = float(sortedlist[i][4].replace(" ", ""))*27
				lnglist.append("{0:.3f}".format(temp))
				temp = 0
				stimelist.append(sortedlist[i][5])
				etimelist.append(sortedlist[i][6])
				duration.append(sortedlist[i][7].replace(" ", ""))
		# # print (duration)		
		data = {'First Device': dev1list,
				'Second Device': dev2list,
				'Latitude': latlist,
				'Longtitude': lnglist,
				'Start Time': stimelist,
				'End Time': etimelist,
				'Duration': duration}
		df = pd.DataFrame(data, columns = ['First Device', 'Second Device', 'Latitude', 'Longtitude', 'Start Time', 'End Time', 'Duration'])	
		print (df)	
		# new_columns = [TableColumn(field="devices", title="Devices")]
		# new_columns.append(TableColumn(field="distances_" + str(c), title=str(c)))
		# data_table.source = source
		# data_table.columns = new_columns
		# new_columns = []
		# data_table.width = 1200
	# else:
		
		
	# 	for i in range(0, len(devList)):
	# 		if i != len(devList):
	# 			strDevice += "-, "
	# 			strFixed += "-, "
	# 		if r == devList[i]:
	# 			strDevice += str(r) + ", "
	# 			strFixed += str(dict_contact[str(r)][str(c)]) + ", "
	# 		else:
	# 			strDevice += "-"	
	# 			strFixed += "-"
	# 		changed_data['devices'] = strDevice.split(", ")	
	# 		changed_data['distances_' + str(c)] = []
	# 		changed_data['distances_' + str(c)] = strFixed.split(", ")
		
	# 	new_source = ColumnDataSource(data=changed_data)
		
	# 	one_columns = [TableColumn(field="devices", title="Device")]
	# 	one_columns.append(TableColumn(field="distances_" + str(c), title=str(c)))
		
	# 	data_table.source = new_source
	# 	data_table.columns = one_columns
	# 	one_columns = []
	# 	data_table.width = 1200
  	
# def refresh_csv():
	
# 	text_refresh.value = "Refreshing..."
# 	contact_csv.seek(0)
# 	contact_csv.truncate()
# 	download_csv()
# 	compile_table('contact.csv')
# 	text_refresh.value = "Refresh!"
   	
  	
button = Button(label="Select", button_type="success")
refresh = Button(label="Refresh", button_type="success")
button.on_click(callback)
# refresh.on_click(refresh_csv)
# data_table = DataTable(source=source, columns=columns, width=2200, height=800)
time_sinput = TextInput(value=labelValue, title="Time Start:")
time_einput = TextInput(value=labelValue, title="Time End:")
text_refresh = TextInput(value=labelValue, title="Refresh Bar")

# output_file("Contact.html")
  
l = layout([
  [select1, select2, select3, select4, button, refresh],
  [radio_button_group, time_sinput, time_einput, text_refresh]
 ])

# show(l)

curdoc().add_root(l)
# curdoc().add_periodic_callback(callback,1000)
# for i in range(0, len(devList)):
# 	list_key = [[k,v] for k, v in dict_contact['100'].items()]
# 	key = sorted(list_key)

# def show_table():
	# HTMLFILE = 'HTML_contact_output.html'
	# f = open(HTMLFILE, 'w')

	# htmlcode = HTML.table(gen_rows(29), header_row=['Device', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
													# '111', '112', '113', '114', '115', '116', '117', '118', '119', '120',
														# '121', '122', '123', '124', '125', '126', '127', '128', '200', '201', '777', '999'])
	# print htmlcode
	# f.write(htmlcode)
	# f.write('<p>')
	# print '-'*79      
# csvFile = open('contact.csv')#enter the csv filename
# csvReader = csv.reader(csvFile)
# csvData = list(csvReader) 
# with open('output.html', 'wb') as html: #enter the output filename
# 	html.write('''<!-- Latest compiled and minified CSS -->
# 	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.css">
# 
# 	<!-- Latest compiled and minified CSS -->
# 	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
# ''')    
# 	html.write('<table data-toggle = "table" data-pagination = "true">\r')
# 	r = 0
# 	for row in csvData:
# 		if r == 0:
# 			html.write('\t<thead>\r\t\t<tr>\r')
# 			for col in row:
# 				html.write('\t\t\t<th data-sortable="true">' + str(col) + '</th>\r')
# 			html.write('\t\t</tr>\r\t</thead>\r')
# 			html.write('\t<tbody>\r')
# 		else:
# 			html.write('\t\t<tr>\r')
#            	for col in row:
#            		html.write('\t\t\t<td>' + str(col) + '</td>\r')
#        		html.write('\t\t</tr>\r')
# 
# 		r += 1
# 	html.write('\t</tbody>\r')
# 	html.write('</table>\r')
#     
# 	html.write('''
# # # <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
# # # <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.0/jquery.min.js"></script>
# 
# # # <!-- Latest compiled and minified JavaScript -->
# # # <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
# 
# # # <!-- Latest compiled and minified JavaScript -->
# # # <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-table/1.8.1/bootstrap-table.min.js"></script>
# # # ''')
    	# html.close()

# show_table()	

# def update_table():
#   http = urllib3.PoolManager()
#   r = http.request('GET', 'http://137.132.165.139/api/contacttable')
#   with open('contact.csv', 'wb') as out:
#   	out.write(r.data)	
#   r.release_conn()
#   compile_table('temp.csv')
#   show_table()
# # update_table()

# # curdoc().add_root(show_table)
# curdoc().add_periodic_callback(update_table,1000)