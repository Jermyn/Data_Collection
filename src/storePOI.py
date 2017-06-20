import json, requests


str_deviceID = []

def actlab_POI():
	poi_list = []
	query_poi = 'query{map (id:"actlab") {graph}}'

	r = requests.get("http://137.132.165.139/graphql", {"query":query_poi})
	str_poi = r.text
	poi = json.loads(str_poi)
	test = json.loads(poi['data']['map']['graph'])
	for i in range(0, len(test['nodes'])):
		if "TP" in test['nodes'][i][0]:
			str_deviceID = (test['nodes'][i][0].split(":"))
			
			str_coordinates = str(test['nodes'][i][1]['coordinates'][1]).strip('"\'"') + ", " + str(test['nodes'][i][1]['coordinates'][0]).strip('"\'"')
			str_points = str_deviceID[2] + ", " + str_coordinates
			poi_list.append(str_points.split(", "))
	poi_list = sorted(poi_list)
	return poi_list
# actlab_POI()

def office_POI():
	poi_list = []
	query_poi = 'query{map (id:"office") {graph}}'

	r = requests.get("http://137.132.165.139/graphql", {"query":query_poi})
	str_poi = r.text
	poi = json.loads(str_poi)
	test = json.loads(poi['data']['map']['graph'])
	for i in range(0, len(test['nodes'])):
		# print (test['nodes'][i][1])
		if "poi" in test['nodes'][i][0]:
			# print (test['nodes'][i][1])
			str_deviceID = (test['nodes'][i][0].split(":"))
			
			str_coordinates = str(test['nodes'][i][1]['coordinates'][1]).strip('"\'"') + ", " + str(test['nodes'][i][1]['coordinates'][0]).strip('"\'"')
			str_points = str_deviceID[1] + ", " + str_coordinates
			poi_list.append(str_points.split(", "))
	poi_list = sorted(poi_list)
	# print (poi_list)
	return poi_list		
# office_POI()

def ward5_POI():
	poi_list = []
	query_poi = 'query{map (id:"ward5") {graph}}'

	r = requests.get("http://137.132.165.139/graphql", {"query":query_poi})
	str_poi = r.text
	poi = json.loads(str_poi)
	test = json.loads(poi['data']['map']['graph'])
	for i in range(0, len(test['nodes'])):
		# print (test['nodes'][i][1])
		if "poi" in test['nodes'][i][0]:
			# print (test['nodes'][i][1])
			str_deviceID = (test['nodes'][i][0].split(":"))
			
			str_coordinates = str(test['nodes'][i][1]['coordinates'][0]).strip('"\'"') + ", " + str(test['nodes'][i][1]['coordinates'][1]).strip('"\'"')
			str_points = str_deviceID[1] + ", " + str_coordinates
			poi_list.append(str_points.split(", "))
	poi_list = sorted(poi_list)
	# print (poi_list)
	return poi_list