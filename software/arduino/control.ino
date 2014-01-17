// Le programme déclanche un relais et allume une LED (Jaune) quand la température moyenne 
// sur un temps définie (2 minutes ici) est en dessous d'un objectif de température (TempObj)
// Quand la température est correcte, une LED (Verte) est allumée.

// Librairie disponible sur http://www.pjrc.com/teensy/td_libs_OneWire.html
#include <OneWire.h>

// Définition des ports I/O sur l'arduino
const int Relais = 2;
const int DS18B20 = 3;
cosnt int Bleue = 4

// Dans tout le programme, on travaille (un maximum) avec des entiers, donc en "centidegré Celsius"
int TempObj = 2000; // Définie l'objectif de température
int t = 0; // Variable utilisée pour le compteur-minuterie
int Temperature[60]; // Tableau dans lequel sera enregistré les températures du capteur
int TempMoy = 0; // Déclare la variable pour la température moyenne
OneWire	ds(DS18B20); // Déclare le capteur DS18B20

void setup(void) {
	Serial.begin(9600);
	pinMode(DS18B20, INPUT);
	pinMode(Relais, OUTPUT);
	pinMode(Bleue, OUTPUT);
}

float getTemp() {
	//Code from http://bildr.org/2011/07/ds18b20-arduino/
	//And http://www.pjrc.com/teensy/td_libs_OneWire.html
	
	byte data[12];
	byte addr[8];

	if ( !ds.search(addr)) {
		//no more sensors on chain, reset search
		ds.reset_search();
		return -1000;
	}

	if ( OneWire::crc8( addr, 7) != addr[7]) {
		Serial.println("CRC is not valid!");
		return -1000;
	}

	if ( addr[0] != 0x10 && addr[0] != 0x28) {
		Serial.print("Device is not recognized");
		return -1000;
	}

	ds.reset();
	ds.select(addr);
	ds.write(0x44,1); // start conversion, with parasite power on at the end

	byte present = ds.reset();
	ds.select(addr);
	ds.write(0xBE); // Read Scratchpad


	for (int i = 0; i < 9; i++) { // we need 9 bytes
		data[i] = ds.read();
	}

	ds.reset_search();

	byte MSB = data[1];
	byte LSB = data[0];

	float tempRead = ((MSB << 8) | LSB); //using two's compliment
	float TemperatureSum = tempRead / 16;

	return TemperatureSum;
}

void loop(void) {
	int Temp = round(getTemp() * 10) * 10; // Précision à 0,1°C
	Temp = Temp - 200; // Soustrait l'autoéchauffement  (mesuré)
	if(TempMoy == 0) {
		TempMoy = Temp; // Utile pour le premier calcul de moyenne
	}
	if(t < 60) { // temps pour la moyenne (selon le delay())
		Temperature[t] = Temp;
		for(int i = 0; i < t; i = i + 1) { // Cette boucle permet de récupérer les valeurs
			TempMoy = (Temperature[i] + TempMoy) / 2; // et de calculer la moyenne
		}
		t = t + 1;
	}
	else {
		t = 0; // Replace le compteur de la minuterie à zéro
		if(TempMoy < TempObj) { // Si la température est inférieure à l'objectif
			digitalWrite(Relais, HIGH);
		}
		else {
			digitalWrite(Relais, LOW);
		}
	}
	Serial.print(Temp);
	Serial.print('&');
	Serial.print(TempMoy);
	Serial.print('&');
	Serial.println(TempObj);
	if(TempMoy < TempObj) {
		digitalWrite(Bleue, HIGH);
	}
	else {
		digitalWrite(Bleue, LOW);
	}
	delay(2000);
}
