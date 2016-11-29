import pygame
import requests


def infoGrab(city):
	info = requests.get("https://en.wikipedia.org/wiki/"+city)