#!/bin/python3
# Plugin Munin pour ThermoHome
# https://github.com/AntoineVe/ThermoHome
import urllib.request
import argparse
serveur = "10.8.0.18"
url = "http://" + serveur + ":8000/temp2munin.txt"
reponse = urllib.request.urlopen(url)
temp = reponse.read()
parser = argparse.ArgumentParser()
parser.add_argument("config", nargs="?")
args = parser.parse_args()
if(args.config == "config"):
    print('''graph_title Temperature interieure
graph_vlabel oC
graph_scale no
graph_args --lower-limit 15 --upper-limit 30
graph_category sensors
Temp.label Temperature''')
else:
    print(temp.decode('utf-8'))
# vim :set tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab
