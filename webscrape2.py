# AIzaSyDjlO8TQYdtE9IbR90pdPm9vfSlL32hxmM
import json
import googlemaps

def infoParse(info): #turns json list into dictionary
	keep = {"distance","duration","legs","steps","start_location","end_location"}
	if(len(info)==0):
		print("info",info)
		return info
	else:
		for element in info:
			if(element in keep):
				if(isinstance(info[element],list) and len(info[element])>0):
					print(info[element][0])
					return infoParse(info[element][0]) 
				elif(isinstance(info[element],dict)):
					print(info[element])
					return infoParse(info[element])

def infoGet(start,end): #used https://github.com/googlemaps/google-maps-services-python/blob/master/README.md
	gmaps = googlemaps.Client(key ='AIzaSyDjlO8TQYdtE9IbR90pdPm9vfSlL32hxmM')
	response = gmaps.directions(start,end)
	formattedDump(response)
	response= json.dumps(response, sort_keys=True, indent=4)
	response = json.loads(response)[0]
	# for element in response:
	# 	print(element)
	# 	if(isinstance(response[element],list) and len(response[element])>0):
	# 		response[element] = (response[element][0])
	# 		# print(response[element])
	# 		print(response[element])
	# return (response['legs']['duration'])
	return infoParse(response)

def formattedDump(response):
	print(json.dumps(response, sort_keys=True, indent=4),"AAAAAAAAAAAAAAA")


print(infoGet("chicago", "pittsburgh"))
