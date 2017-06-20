import requests, json


def getScale(location):
	if location=="actlab":
		query_scale = 'query{map (id:"actlab") {scale}}'
	elif location=="office":
		query_scale = 'query{map (id:"office") {scale}}'
	else:
		query_scale = 'query{map (id:"ward5678") {scale}}'	
	r = requests.get("http://137.132.165.139/graphql", {"query":query_scale})
	scale = r.text
	scale_json = json.loads(scale)
	return float(scale_json['data']['map']['scale'])
# numScale = getScale("office")	