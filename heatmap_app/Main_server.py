'''
Created on 31 May 2017

@author: jermz
'''
from main import devList
import json, requests, time
from bokeh.io import curdoc

main_write = open('data.csv', 'w')
main_write.write("deviceId, lat, lng\n")
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
    data = []
    _data = []
    for i in range(0, duration):
        data.append(query_server())
        wait_second()   
    _data = sorted(data[0])  
    for j in range(0, len(_data)):
        for k in range(0, 3):
            if k<2:
                main_write.write(_data[j][k] + ", ")
            else:
                main_write.write(_data[j][k] + "\n")    
pull_data(5)
