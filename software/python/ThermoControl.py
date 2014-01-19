#!/usr/bin/python3
import serial #Importe la bibliothèque de communication série
import time #Importe la bibliothèque pour gérer le temps
import threading #Multithreading
from bottle import route, run, template, get, post, request

webrun = 0 
it = 0
ARDUINO = serial.Serial('/dev/ttyACM0', 9600) # ouvre le port série. Attention cela envoie un "reset" à l'arduino

progjour = "LJJJJLNNNNNNNNNNNNNOPONL" #Journée par défaut (cf calcul de température par l'arduino)

# Pour rappel :
# TempObj = 2100 - (((80 - serialin) * 100) / 2); // Petit algorithme pour le calcul de la température
# Départ de 21°, et modifie la valeur selon la valeur ASCII du caractère reçu, le nul correspondant
# à "P". "Monter" d'une lettre ajout 0,5°, "descendre" d'une lettre retranche 0,5°.

def speak2arduino(): #Fonction de communication avec l'arduino
	time.sleep(5) #Les 5 secondes permettent de s'assurer que l'arduino est disponible
	global Temp
	global TempMoy
	global TempObj
	global progjour
	heure = time.strftime("%H")
	heure = int(heure)
	obj = str.encode(progjour[heure])
	ARDUINO.write(obj) #Envoie l'objectif de température
	releves = ARDUINO.readline() #Récupère les informations de température
	releves = releves.decode("utf-8")
	releves = releves.split('&')
	Temp = int(releves[0]) / 100
	TempMoy = int(releves[1]) / 100
	TempObj = int(releves[2]) / 100

def httpserver():
	run(host='0.0.0.0', port='8000', debug=True) #commande lançant le serveur bottle

while(True):
	speak2arduino()
	@route('/temp2munin.txt') #Sert le fichier pour munin
	def temp2munin(temp=Temp):
		return template('Temp.value {{temp}}', temp=temp)
	@route('/thermostat.html') #Page de monitoring et de programmation
	def thermostat(temp=Temp, moy=TempMoy, obj=TempObj, prog=progjour):
		heure = time.strftime("%H:%M")
		return template('''
		<html>
		<head>
		<title>Gestion de la température</title>
		<meta http-equiv="refresh" content="30;url=thermostat.html">
		<body>
		<h2>Température : {{temp}}</h2>
		<h2>Moyenne : {{moy}}</h2>
		<h2>Objectif : {{obj}}</h2>
		<form action="/thermostat-prog.html" method="post">
			Journée : <input name="prog" type="text" size="24" value="{{prog}}" />
			<input valule="Programmer" type="submit" />
		</form>
		<div class="footer">Dernière mise à jour : {{heure}}</div>
		</body>
		</html>
		''', temp=temp, moy=moy, obj=obj, heure=heure, prog=prog)
	@route('/thermostat-prog.html', method='POST') #Page d'attente post programmation. Réaffiche la page de monitoring au bout de 8 secondes (temps de mise à jour du programme et de l'arduino)
	def do_thermostat():
		global progjour
		progjour = request.forms.get('prog')
		return '''
		<html>
		<head>
		<title>Gestion de la température</title>
		<meta http-equiv="refresh" content="8;url=thermostat.html">
		</head>
		<body>
		<h1>Mise à jour...</h1>
		</body>
		</html>
		'''
	if(webrun == 0):
		threading.Thread(target = httpserver).start() #Lance le serveur web bottle dans un thread pour continuer le programme
		webrun = 1 #Évite de relancer le thread
