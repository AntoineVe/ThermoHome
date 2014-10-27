#!/usr/bin/python3
import serial #Importe la bibliothèque de communication série
import time #Importe la bibliothèque pour gérer le temps
import bottle #Serveur web Bottle
import argparse #Parser d'arguments
import sqlite3 #Importe la gestion des bases sqlite3

parser = argparse.ArgumentParser()
parser.add_argument("--module", dest="modules", nargs="*", default="none", help="Liste de modules à ajouter")
parser.add_argument("--base", dest="db", nargs=1, default="./thermo.db", type=str, help="Nom de la base sqlite")
parser.add_argument("--port", dest="port", nargs=1, default="/dev/ttyACM0", type=str, help="Port de l'Arduino (/dev/ttyACM0)")
parser.add_argument("--web-port", dest="webport", nargs=1, default="8000", type=int, help="Port pour le serveur web")
parser.add_argument("--temp-only", dest="temponly", action="store", type=int, nargs="?", const=1, help="Affiche la température relevée et quitte")

args = parser.parse_args()

db = "./thermo.db"

ARDUINO = serial.Serial('/dev/ttyUSB0', 9600) # ouvre le port série. Attention cela envoie un "reset" à l'arduino
time.sleep(5) #Les 5 secondes permettent de s'assurer que l'arduino est disponible

defprogjour = "HHHHHHHHPPNNNNNNNNNPPPNL" #Journée par défaut (cf calcul de température par l'arduino)

#H 17  L 19  P 21
#I     M
#J 18  N 20
#K     O 

# Pour rappel :
# TempObj = 2100 - (((80 - serialin) * 100) / 2); // Petit algorithme pour le calcul de la température
# Départ de 21°, et modifie la valeur selon la valeur ASCII du caractère reçu, le nul correspondant
# à "P". "Monter" d'une lettre ajout 0,5°, "descendre" d'une lettre retranche 0,5°.

def speak2arduino(): #Fonction de communication avec l'arduino
    global Temp
    global TempObj
    global progjour
    heure = time.strftime("%H")
    heure = int(heure)
    obj = str.encode(progjour[heure])
    ARDUINO.write(obj) #Envoie l'objectif de température
    time.sleep(1)
    ARDUINO.flushOutput()
    releves = ARDUINO.readline() #Récupère les informations de température
    time.sleep(1)
    ARDUINO.flushInput()
    releves = releves.decode("utf-8")
    releves = releves.split('&')
    Temp = int(releves[0]) / 100
#    TempMoy = int(releves[1]) / 100
    TempObj = int(releves[2]) / 100

if(args.temponly == 1):
    speak2arduino()
    print(str(Temp) + "°C")
    quit()

def checkdb(date):
    global defprogjour
    global progjour
    global db
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT progjour FROM requested WHERE date = ?", (date,))
    dbprog = c.fetchone()
    progjour = defprogjour
    if dbprog:
        progjour = dbprog[0]
    conn.close()
    return progjour

def recorddb(temp):
    global db
    datetime = time.strftime("%d-%m-%Y_%H-%M")
    record = (datetime, temp)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO recorded VALUES(?,?)", (record))
    conn.commit()
    conn.close()

def courbe(date):
    global db
    svg_courbe = ""
    date = date + '%'
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("SELECT date FROM recorded WHERE date LIKE ? ORDER BY date ASC", (date,))
    timepoint = c.fetchall()
    if timepoint:
        delai = abs(int([timepoint[0] for timepoint in timepoint][0].split('-')[3])-int([timepoint[0] for timepoint in timepoint][1].split('-')[3]))
        timepoint = [timepoint[0] for timepoint in timepoint]
    for horloge in timepoint:
        jour = horloge.split('_')[0]
        heure = int(horloge.split('_')[1].split('-')[0])
        minute = int(horloge.split('_')[1].split('-')[1])
        heureminute = minute + heure*60
        c.execute("SELECT recjour FROM recorded WHERE date = ?", (horloge,))
        start_temp = c.fetchone()[0]
        start_time = heureminute
        end_time = start_time + delai
        end_heure = end_time // 60
        end_minute = end_time % 60
        end_heure = str(end_heure).zfill(2)
        end_minute = str(end_minute).zfill(2)
        end_horloge = jour + '_' + end_heure + '-' + end_minute
        c.execute("SELECT recjour FROM recorded WHERE date = ?", (end_horloge,))
        end_temp = c.fetchone()
        if end_temp:
            end_temp = end_temp[0]
            svg_courbe += ('<path d="M' + str(start_time / 2) + ',' + str(abs(start_temp*10 - 300)) + ' C' + str((start_time + end_time) / 4) + ',' + str(abs(start_temp*10 - 300)) + ' ' + str((start_time + end_time) / 4) + ',' + str(abs(end_temp*10 - 300)) + ' ' + str(end_time / 2) + ',' + str(abs(end_temp*10 - 300)) + '" fill="none" stroke-width="2.5" stroke="#073642" />')
    return svg_courbe

checkdb(time.strftime("%d-%m-%Y")) #Vérifie la base de données au démarrage
speak2arduino() #Lance une première fois pour initialiser la variable Temp

@bottle.get('/getTemp.txt')
def getTemp():
    today = time.strftime("%d-%m-%Y")
    checkdb(today)
    speak2arduino()
    recorddb(Temp)
    return bottle.template('{{temp}}', temp=Temp)
@bottle.get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return bottle.static_file(filename, root='static')
@bottle.get('/<filename:re:.*\.js>')
def stylesheets(filename):
    return bottle.static_file(filename, root='static')
@bottle.route('/thermostat.html') #Page de monitoring et de programmation
def thermostat():
    date = time.strftime("%d-%m-%Y")
    httpdate = bottle.request.query.date
    if httpdate:
        date = httpdate
    checkdb(date)
    heure = time.strftime("%H:%M")
    speak2arduino()
    svg_courbe = courbe(date)
    return bottle.template('thermostat', temp=Temp, obj=TempObj, heure=heure, prog=progjour, date=date, courbe=svg_courbe)
@bottle.route('/thermostat-prog.html', method='POST') #Page d'attente post programmation. Réaffiche la page de monitoring au bout de 8 secondes (temps de mise à jour du programme et de l'arduino)
def do_thermostat():
    global progjour
    global db
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
    date = bottle.request.forms.get('date')
    dbstore = (date, progjour)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO requested VALUES(?,?)", (dbstore))
    conn.commit()
    conn.close()
    return bottle.template('thermostat_update.tpl', progjour=progjour, date=date)

bottle.run(host='0.0.0.0', port=args.webport, debug=True) #commande lançant le serveur bottle

#vim tabstop=4 shiftwidth=4 softtabstop=4 noexpandtab
