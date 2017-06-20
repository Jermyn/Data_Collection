from bokeh.charts import Bar, output_file, show
import pandas as pd

my_simple_dict = {
    'Group 1': [22,33,44,55],
    'Group 2': [44,66,0,24],
    'Group 3': [2,99,33,51]
}

my_data_transformed_dict = {}

my_data_transformed_dict['x-axis'] = []
my_data_transformed_dict['value'] = []
my_data_transformed_dict['group-name'] = []
for group, group_list in my_simple_dict.iteritems():
    x_axis = 0
    for item in group_list:
        x_axis += 1
        my_data_transformed_dict['x-axis'].append(x_axis)
        my_data_transformed_dict['value'].append(item)
        my_data_transformed_dict['group-name'].append(group)
print my_data_transformed_dict        

# my_bar = Bar(my_data_transformed_dict, values='value',label='x-axis',group='group-name',legend='top_right')

# output_file("grouped_bar.html")

# show(my_bar)