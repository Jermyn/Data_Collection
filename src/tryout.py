# import pandas as pd
import csv

from bokeh.charts import HeatMap, bins, output_file, show, Bar, BoxPlot
from bokeh.layouts import column, gridplot
from bokeh.palettes import RdYlGn6, RdYlGn9, YlOrRd9, GnRd9
from bokeh.sampledata.autompg import autompg
from bokeh.sampledata.unemployment1948 import data
from bokeh.models import LogColorMapper, LogTicker, ColorBar, HoverTool, ColumnDataSource, LabelSet, BoxSelectTool
import operator
data = []
error = []
contact = []

# csvfile = open('temp.csv', 'w')
# typefile = open('type.csv', 'w')
def extract_write_file(filename):
  count = 0
  with open(filename,'r') as csvfile:
    next(csvfile)
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if count==28:
          break  
        data.append(float("{0:.3f}".format(float(row[1]))))
        error.append(float("{0:.1f}".format(float(row[1]))))
        count+=1    
extract_write_file("history_compiled.csv")
#     #print data    

# def sortList(list_sort):
#   initial=0
#   dev_i = int(list_sort[0][0])
#   for index in range(0, len(list_sort)):
#     dev = int(list_sort[index][0])
#     if dev<128:
#       if dev_i==dev:
#         if index==initial:
#           initial = index
#       elif dev!=dev_i:  
#         end = index
#         # print str(initial) + ", " + str(end) + "\n"
#         list_sort[initial:end] = sorted(list_sort[initial:end])
#         initial=index
#         dev_i=dev
#   return list_sort 

# def prepareData(list_prep):
#   dataList = []
#   for index in range(0, 784):
#     if index%28==0:
#       dataList.insert(index, "checkpoint")
#   for i in range(0, len(list_prep)):
#     for j in range(100, 128):
#       if int(list_prep[i][1])==j:
#         if list_prep[i][0]=='100':
#           dataList.insert((j%100), list_prep[i][2])
#         elif list_prep[i][0]=='101':
#           dataList.insert(((j%100)+28), list_prep[i][2])
#         else:
#           dataList.insert(((int(list_prep[i][0])%100)*28+(j%100)), list_prep[i][2])   
#   for m in range(0, len(dataList)):
#     print typefile.write(str(dataList[m]) + "\n")




# reader_contact = csv.reader(open("contacttable.csv"), delimiter=",")
# next(reader_contact)
# sortedlist = sorted(reader_contact, key=operator.itemgetter(0), reverse=False)
# sortedlist = sortList(sortedlist)
# for index in range(0, len(sortedlist)):
#   contact_time = float(sortedlist[index][2])/1000.0
#   sortedlist[index][2] = contact_time
#   csvfile.write(str(sortedlist[index]) + "\n")

# # for i in range(0, len(sortedlist)):
# #   print sortedlist[i]
# # sort = sorted(sortedlist[0:3])
# # for i in range(0, len(sort)):
# #   print sort[i]
# prepareData(sortedlist)

# setup data sources
# data = data.copy()
# data['Year'] = data['Year'].astype(str)
# unempl = pd.melt(data, var_name='Month', value_name='Unemployment', id_vars=['Year'])

# fruits = {'fruit': ['apples', 'apples', 'apples', 'apples', 'apples',
#                     'pears', 'pears', 'pears', 'pears', 'pears',
#                     'bananas', 'bananas', 'bananas', 'bananas', 'bananas'],
#           'fruit_count': [4, 5, 8, 12, 4, 6, 5, 4, 8, 7, 1, 2, 4, 8, 12],
#           'year': [2009, 2010, 2011, 2012, 2013, 2009, 2010, 2011, 2012, 2013, 2009, 2010,
#                    2011, 2012, 2013]}
# print autompg
reader_pre = csv.reader(open("history_compiled.csv"), delimiter=",")
next(reader_pre)

test = {'region' : ['region A', 'region A', 'region A', 'region A', 
                    'region B', 'region B', 'region B', 'region B',
                    'region C', 'region C', 'region C', 'region C',
                    'region D', 'region D', 'region D', 'region D',
                    'region E', 'region E', 'region E', 'region E',
                    'region F', 'region F', 'region F', 'region F',
                    'region G', 'region G', 'region G', 'region G'], 
         'data' : data,           
        #'data'  : [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84],
        'area' : ['beacon A', 'beacon B', 'beacon C', 'beacon D', 'beacon A', 'beacon B', 'beacon C', 'beacon D', 
                  'beacon A', 'beacon B', 'beacon C', 'beacon D', 'beacon A', 'beacon B', 'beacon C', 'beacon D',
                  'beacon A', 'beacon B', 'beacon C', 'beacon D', 'beacon A', 'beacon B', 'beacon C', 'beacon D',
                  'beacon A', 'beacon B', 'beacon C', 'beacon D']}
data_bar = {
          'region' : ['100', '101', '102', '103', '104', '105', '106', '107',
                        '108', '109', '110', '111', '112', '113', '114', '115',
                          '116', '117', '118', '119', '120', '121', '122', '123',
                            '124', '125', '126', '127'],
          'dist' : error                  
}                  
# contact = {'device_x': ['100', '101', '102', '103', '104', '105', '106', '107',
#                         '108', '109', '110', '111', '112', '113', '114', '115',
#                           '116', '117', '118', '119', '120', '121', '122', '123',
#                             '124', '125', '126', '127'],
#            'contact_data' : [0, ]                }
#source = ColumnDataSource(dict(x='region', y='area'))
source = ColumnDataSource(data=dict(x=[1, 1, 1, 1,
                                      2, 2, 2, 2,
                                      3, 3, 3, 3,
                                      4, 4, 4, 4,
                                      5, 5, 5, 5,
                                      6, 6, 6, 6,
                                      7, 7, 7, 7],
                                    y=[1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4],
                                    value=data))
source_dev = ColumnDataSource(data=dict(x=[1, 1, 1, 1,
                                      2, 2, 2, 2,
                                      3, 3, 3, 3,
                                      4, 4, 4, 4,
                                      5, 5, 5, 5,
                                      6, 6, 6, 6,
                                      7, 7, 7, 7],
                                    y=[1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4,
                                        1, 2, 3, 4],
                                    value=[100, 101, 102, 103,
                                        104, 105, 106, 107,
                                        108, 109, 110, 111,
                                        112, 113, 114, 115,
                                        116, 117, 118, 119,
                                        120, 121, 122, 123,
                                        124, 125, 126, 127]))
source_reg = ColumnDataSource(data=dict(x=['100', '101', '102', '103',
                                            '104', '105', '106', '107',
                                            '108', '109', '110', '111',
                                            '112', '113', '114', '115',
                                            '116', '117', '118', '119',
                                            '120', '121', '122', '123',
                                            '124', '125', '126', '127'],
                                        y=error))
labels = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=-8, source=source, render_mode='canvas')                  
labels.text_color = 'black'  
labels.text_font_style = 'italic' 
labels_dev = LabelSet(x='x', y='y', text='value', level='glyph', x_offset=-20, y_offset=2, source=source_dev, render_mode='canvas')    
labels.text_color = 'blue'  
labels.text_font_style = 'italic'    
label_reg = LabelSet(x='x', y='y', text='y', level='glyph', x_offset=-12, y_offset=0, source=source_reg, render_mode='canvas')       
# fruits['year'] = [str(yr) for yr in fruits['year']]

# hm1 = HeatMap(autompg, x=bins('mpg'), y=bins('displ'))

# hm2 = HeatMap(autompg, x=bins('mpg'), y=bins('displ'), values='cyl', stat='mean')

# hm3 = HeatMap(autompg, x=bins('mpg'), y=bins('displ', bins=15),
#               values='cyl', stat='mean')

# hm4 = HeatMap(autompg, x=bins('mpg'), y='cyl', values='displ', stat='mean')

# hm5 = HeatMap(autompg, y=bins('displ'), x=bins('mpg'), values='cyl', stat='mean',
#               spacing_ratio=0.9)

# hm6 = HeatMap(autompg, x=bins('mpg'), y=bins('displ'), stat='mean', values='cyl',
#               palette=RdYlGn6)

# hm7 = HeatMap(autompg, x=bins('mpg'), y=bins('displ'), stat='mean', values='cyl',
#               palette=RdYlGn9)

# hm8 = HeatMap(autompg, x=bins('mpg'), y=bins('displ'), values='cyl',
#               stat='mean', legend='top_right')

# hm9 = HeatMap(fruits, y='year', x='fruit', values='fruit_count', stat=None)

# hm10 = HeatMap(unempl, x='Year', y='Month', values='Unemployment', stat=None,
#               sort_dim={'x': False}, width=900, plot_height=500)

TOOLS = [BoxSelectTool(), HoverTool()]

hm11 = HeatMap(test, x='region', y='area', values='data', legend=False, stat=None, palette=GnRd9, width = 500, plot_height=500, title="Actlab Region Detection Test", tools=TOOLS)
hm12 = Bar(data_bar, values='dist', label='region', legend=False, title='Error Distance for Respective Regions', width = 800, plot_height = 500)
hm13 = BoxPlot(data_bar, values='dist', label='region', legend=False, title='Error Distance Boxplot', width = 300, plot_height=300)
#hm11.legend.location = 'right'
# data1 = [int(x) for x in data]
# print data1
# hover = HoverTool(tooltips=[
#   ("error", "@data1")])
# hm11.add_tools(hover)  
hm11.add_layout(labels)
hm11.add_layout(labels_dev)
hm12.add_layout(label_reg)
# output_file("heatmap.html")
output_file("Bar.html")
hm11.axis.visible = False
# show(hm11)
# show(hm12)
# show(hm13)



show(column(
   gridplot(hm11, hm12,
            ncols=1, plot_width=400, plot_height=400)
 ))
