import json
import googlemaps
# from googleplaces import GooglePlaces, types, lang
import googleplaces

def checkLocation(loc):
	gmaps = googleplaces.GooglePlaces('AIzaSyDVfV_V7nCQ9Dt4BHdcQTmBDbjdODEUuCo')
	try:
		info = gmaps.nearby_search(location=loc)
		return True
	except:
		return None

def steps(info):
	sectionInfo = []
	for step in info:
		sectionInfo.append(infoParse(step))
	return sectionInfo

def infoParse(info): #turns json list into dictionary
	keep = {"distance","duration","legs","steps","start_location","end_location","lat","lng","text","value"}
	parsed = {}
	if(not isinstance(info,list) and not isinstance(info,dict)):
		return info
	else:
		for element in info:
			if(element in keep):
				if(isinstance(info[element],list)):
					if(element=="steps"):
						parsed[element] = steps(info[element])
					else:
						parsed[element] = infoParse(info[element][0])
				else:
					parsed[element]=infoParse(info[element])
	return parsed

def infoGet(start,end): #used https://github.com/googlemaps/google-maps-services-python/blob/master/README.md
	gmaps = googlemaps.Client(key ='AIzaSyDVfV_V7nCQ9Dt4BHdcQTmBDbjdODEUuCo')
	try:
		response = gmaps.directions(start,end)[0]
		infoDict = infoParse(response)
		# print(infoDict['legs']['steps'][0])
		return infoDict,surroundings(infoDict["legs"]["start_location"])
	except: return None,None

def surroundings(loc):
	#referenced https://github.com/slimkrazy/python-google-places
	geoTerms = ["river","mountain","mountains","plains","hills","lake","woods","forest"]
	found = []
	gmaps = googleplaces.GooglePlaces('AIzaSyDVfV_V7nCQ9Dt4BHdcQTmBDbjdODEUuCo')
	info = gmaps.nearby_search(lat_lng=loc,radius=5000,types=["natural_feature"])
	for place in info.places:
		place.get_details()
		for term in geoTerms:
			if(term in place.name.lower()):
				found.append(term)
	return set(found)

 
if __name__ == '__main__':
	print(infoGet("duquesne","houston"))
	# print(surroundings({'lng': -104.9902503, 'lat': 39.7392353}))

