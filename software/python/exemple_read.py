#!/usr/bin/python3
import serial #Importe la bibliothèque de communication série
import time #Importe la bibliothèque pour gérer le temps
arduino = serial.Serial('/dev/ttyACM0', 9600) # ouvre le port série. Attention cela envoie un "reset" à l'arduino
a = 0
while(True): #boucle pour la lecture
    tempet = arduino.readline() #lit le port série
#    while(len(tempet) != 16): #vérifie les données reçues. Normalement, il doit lire 16 caractères.
#        tempet = arduino.readline() #Recommence la lecture s'il n'y a pas les 16 caractères.
    tempet = tempet.decode("utf-8") #Transforme la chaine depuis 'bytes' vers 'utf-8' (python 3)
    tempet = tempet.split('&') # Découpe la chaine sur les caractères '&'. 
    Temp = int(tempet[0]) / 100
    TempMoy = int(tempet[1]) / 100
    TempObj = int(tempet[2]) / 100
    print('La température actuelle est de ' + (str(Temp)) + '°C.')
    print('La température moyenne est de ' + (str(TempMoy)) + '°C.')
    print('L\'objectif de température est de ' + (str(TempObj)) + '°C.')
#    a = a+1 #boucle
