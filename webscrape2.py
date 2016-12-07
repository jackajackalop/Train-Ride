import json
import googlemaps
import googleplaces
from geolocation.main import GoogleMaps
import requests
import webscrape

key ='AIzaSyDVfV_V7nCQ9Dt4BHdcQTmBDbjdODEUuCo'

def checkLocation(loc):
	gmaps = googleplaces.GooglePlaces(key)
	try:
		info = gmaps.nearby_search(location=loc)
		return True
	except:
		return None

def steps(info): #helps infoParse()
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
	gmaps = googlemaps.Client(key =key)
	try:
		response = gmaps.directions(start,end)[0]
		infoDict = infoParse(response)
		return infoDict,surroundings(infoDict["legs"]["start_location"])
	except: return None,None

def surroundings(loc):
	#referenced https://github.com/slimkrazy/python-google-places
	geoTerms = ["river","mountain","mountains","plains","hills","lake","woods","forest"]
	found = []
	gmaps = googleplaces.GooglePlaces(key)
	info = gmaps.nearby_search(lat_lng=loc,radius=5000,types=["natural_feature"])
	for place in info.places:
		place.get_details()
		for term in geoTerms:
			if(term in place.name.lower()):
				found.append(term)
	locCity = city(loc['lat'],loc['lng'])
	if(locCity!=None):
		found+=webscrape.infoGrab(locCity)
	return set(found)

def city(latitude,longitude):
	try:
		gmaps = GoogleMaps(key)
		info = gmaps.search(lat=latitude, lng = longitude).first()
		city ="%s"%info.city
		return city.split('\'')[1]
	except:
		return None

def climateInfo(loc):
	APIURL="http://www.ncdc.noaa.gov/cdo-web/api/v2/data"
	response = requests.post(APIURL,params=loc,
							 headers={'token': 'pqVesrVGzgJUYuNuyMRuMffMACVuKZZp'},
							 )
	return response.text

if __name__ == '__main__':
	# print(climateInfo({"datasetid":"EVAPo","station":"GHCND:AEM00041217","startdate":"2010-05-01","enddate":"2010-05-01"}))
	# print(climateInfo({'lng': -104.9902503, 'lat': 39.7392353}))
	print(infoGet("pittsburgh","houston"))
	# print(surroundings({'lng': -104.9902503, 'lat': 39.7392353}))
	# print(city(39.7392353,-104.9902503))

