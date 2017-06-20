'''
Created on 29 May 2017

@author: jermz
'''
from bokeh.plotting import Figure
from bokeh.models.layouts import VBox
from bokeh.models.widgets import RadioGroup
from bokeh.io import curdoc

fig1 = Figure()
fig1.circle(x=[1,2], y=[3,4])

fig2 = Figure()
fig2.circle(x=[100,200], y=[200, 1000])

def switch_plots(selected_plot):
    main_box.children = layouts[selected_plot]

layout_picker = RadioGroup(labels=['Layout1', 'Layout2'])
layout_picker.on_click(switch_plots)

layout1 = VBox(children=[fig1])
layout2 = VBox(children=[fig2])
layouts = [[layout1], [layout2]]

main_box = VBox(children=[layout1])

curdoc().add_root(main_box)
curdoc().add_root(layout_picker)