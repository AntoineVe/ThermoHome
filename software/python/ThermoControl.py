#!/usr/bin/python3
import serial #Importe la bibliothèque de communication série
import time #Importe la bibliothèque pour gérer le temps
import threading #Multithreading
import bottle #Serveur web Bottle

webrun = 0 
ARDUINO = serial.Serial('/dev/ttyACM0', 9600) # ouvre le port série. Attention cela envoie un "reset" à l'arduino

progjour = "LJJJJLNNNNNNNNNNNNNOPONL" #Journée par défaut (cf calcul de température par l'arduino)

# Pour rappel :
# TempObj = 2100 - (((80 - serialin) * 100) / 2); // Petit algorithme pour le calcul de la température
# Départ de 21°, et modifie la valeur selon la valeur ASCII du caractère reçu, le nul correspondant
# à "P". "Monter" d'une lettre ajout 0,5°, "descendre" d'une lettre retranche 0,5°.

def speak2arduino(): #Fonction de communication avec l'arduino
	time.sleep(5) #Les 5 secondes permettent de s'assurer que l'arduino est disponible
	ARDUINO.flush() #Vide le tampon de l'arduino
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
	bottle.run(host='0.0.0.0', port='8000', debug=True) #commande lançant le serveur bottle

while(True):
	speak2arduino()
	@bottle.route('/temp2munin.txt') #Sert le fichier pour munin
	def temp2munin(temp=Temp):
		return bottle.template('Temp.value {{temp}}', temp=temp)
	@bottle.route('/thermostat.html') #Page de monitoring et de programmation
	def thermostat(temp=Temp, moy=TempMoy, obj=TempObj, prog=progjour):
		heure = time.strftime("%H:%M")
		return bottle.template('thermostat', temp=temp, moy=moy, obj=obj, heure=heure, prog=prog)
	@bottle.route('/thermostat-prog.html', method='POST') #Page d'attente post programmation. Réaffiche la page de monitoring au bout de 8 secondes (temps de mise à jour du programme et de l'arduino)
	def do_thermostat():
		global progjour
		def ogla(code):
			code = float(code)
			a = 80 + (code * 10 - 210) / 5
			a = int(a)
			return chr(a)
		h0 = ogla(bottle.request.forms.get('prog_h0'))
		h1 = ogla(bottle.request.forms.get('prog_h1'))
		h2 = ogla(bottle.request.forms.get('prog_h2'))
		h3 = ogla(bottle.request.forms.get('prog_h3'))
		h4 = ogla(bottle.request.forms.get('prog_h4'))
		h5 = ogla(bottle.request.forms.get('prog_h5'))
		h6 = ogla(bottle.request.forms.get('prog_h6'))
		h7 = ogla(bottle.request.forms.get('prog_h7'))
		h8 = ogla(bottle.request.forms.get('prog_h8'))
		h9 = ogla(bottle.request.forms.get('prog_h9'))
		h10 = ogla(bottle.request.forms.get('prog_h10'))
		h11 = ogla(bottle.request.forms.get('prog_h11'))
		h12 = ogla(bottle.request.forms.get('prog_h12'))
		h13 = ogla(bottle.request.forms.get('prog_h13'))
		h14 = ogla(bottle.request.forms.get('prog_h14'))
		h15 = ogla(bottle.request.forms.get('prog_h15'))
		h16 = ogla(bottle.request.forms.get('prog_h16'))
		h17 = ogla(bottle.request.forms.get('prog_h17'))
		h18 = ogla(bottle.request.forms.get('prog_h18'))
		h19 = ogla(bottle.request.forms.get('prog_h19'))
		h20 = ogla(bottle.request.forms.get('prog_h20'))
		h21 = ogla(bottle.request.forms.get('prog_h21'))
		h22 = ogla(bottle.request.forms.get('prog_h22'))
		h23 = ogla(bottle.request.forms.get('prog_h23'))
		progjour = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8 + h9 + h10 + h11 + h12 + h13 + h14 + h15 + h16 + h17 + h18 + h19 + h20 + h21 + h22 + h23
		return bottle.template('''
		<html>
		<head>
		<title>Gestion de la température</title>
		<meta http-equiv="refresh" content="8;url=thermostat.html">
		</head>
		<body>
		<h1>Mise à jour...</h1>
		<p>{{progjour}}</p>
		</body>
		</html>
		''', progjour=progjour)
	if(webrun == 0):
		threading.Thread(target = httpserver).start() #Lance le serveur web bottle dans un thread pour continuer le programme
		webrun = 1 #Évite de relancer le thread
