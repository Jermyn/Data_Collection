import base64
import urllib3
import json
import sys
import math

http = urllib3.PoolManager()
r = http.request('GET', 'http://137.132.165.139/api/devices')
# dev1_x = json.loads(r.data.decode('utf-8'))[repr(int('11'))]['lat']
# dev1_y = json.loads(r.data.decode('utf-8'))[repr(int('11'))]['lng']
dev1_x = json.loads(r.data.decode('utf-8'))[repr(int(sys.argv[1]))][sys.argv[2]]
dev1_y = json.loads(r.data.decode('utf-8'))[repr(int(sys.argv[3]))][sys.argv[4]]

dev2_x = json.loads(r.data.decode('utf-8'))[repr(int(sys.argv[5]))][sys.argv[6]]
dev2_y = json.loads(r.data.decode('utf-8'))[repr(int(sys.argv[7]))][sys.argv[8]]

# print (dev1_x + "\n")
# print (dev1_y + "\n")

# print dev2_x + "\n"
# print dev2_y + "\n"

dist = math.sqrt((pow((float(dev1_x)-float(dev2_x)),2)+pow((float(dev1_y)-float(dev2_y)),2)))
# print repr(dist) + "\n"

scale = 10/dist
print (repr(scale) + "\n")

# print sys.argv[1] + "\n"
# print sys.argv[2] + "\n"
# print sys.argv[3] + "\n"
# print sys.argv[4] + "\n"


