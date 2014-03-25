#!/bin/python3
# Plugin Munin pour ThermoHome
# https://github.com/AntoineVe/ThermoHome
import urllib.request
serveur = "10.8.0.18"
url = "http://" + serveur + ":8000/temp2munin.txt"
reponse = urllib.request.urlopen(url)
temp = reponse.read()
print(temp.decode('utf-8'))
# vim :set tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab
