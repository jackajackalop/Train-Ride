import pygame
import requests

def infoGrab(city):
	info = requests.get("https://en.wikipedia.org/wiki/"+city)
	info = info.text
	if("search instead" in info or "the city" not in info):
		return None
	geoKW = geoSearch(info)
	# tempKW = tempSearch(info)
	# climKW = climateSearch(info)
	return geoKW#,tempKW

def geoSearch(info):
	geoTerms = ["river","mountain","mountains","plains",
	"hills","desert","wood","woods","forest"]
	found = []
	words = info.split()
	for term in geoTerms:
		if(term in info): found.append(term)
	return found

def tempSearch(info):
	info = info.replace("<"," ")
	info = info.replace(","," ")
	sentences = info.split(". ")
	months = ["January","February","March","April","May","June",
		"July","August","September","October","November","December"]
	tempKW = {}
	for sentence in sentences:
		if(";°C" in sentence):
			for month in months:
				if(month+" " in sentence):
					words =sentence.split()
					for word in words:
						if(";°C" in word):
							cut1 = word.find("(")
							cut2 = word.find('&')
							if(month not in tempKW):
								tempKW[month] = word[cut1+1:cut2]

	return tempKW


def climateSearch(info):
	climateTerms = ["snow","snowfall","rain","percipitation","rainfall"]

if __name__ == '__main__':
	print(infoGrab("Detroit"))