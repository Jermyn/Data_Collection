'''
Created on 29 May 2017

@author: jermz
'''
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

import urllib3, json 
import numpy as np
from bokeh.client.session import push_session
from pydoc import serve
from bokeh.command.subcommands.tests.test_serve import run_bokeh_serve


source = ColumnDataSource(dict(x=[],y=[]))

fig=Figure()
fig.line(source=source, x='x', y='y', line_width=2, alpha=.85, color='red')

ct=0
def update_data():
    global ct
    ct+=1
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://137.132.165.139/api/edges')
    data = json.loads(r.data.decode('utf-8'))
    # data = json.loads(urllib.request.urlopen("http://137.132.165.139/api/edges").read().decode())
    connection = data['106:1']
    # print(connection['mu'])
    new_data = dict(x=[ct],y=[connection['mu']])
    source.stream(new_data,1000)

curdoc().add_root(fig)
curdoc().add_periodic_callback(update_data,1000)
session = push_session(curdoc())
session.show()
session.loop_until_closed()