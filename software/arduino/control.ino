#include <OneWire.h>
const int DS18B20 = 12;
const int Bleu = 2;
const int Vert = 4;
const int Rouge = 7;
const int Relais = 3;
float TempObj = 20.00;
int RelaisActif = 0;
int t = 0;
int Temperature[60];
float TempMoy = 0.00;
float TempSum = 0.00;
OneWire	ds(DS18B20);
void setup(void) {
	Serial.begin(9600);
	pinMode(DS18B20, INPUT);
	pinMode(Bleu, OUTPUT);
	pinMode(Vert, OUTPUT);
	pinMode(Rouge, OUTPUT);
	pinMode(Relais, OUTPUT);
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
	float Temp = (getTemp() - 1.70);
	if(TempMoy == 0.00) {
		TempMoy = Temp;
	}
	if(t < 60) { // temps pour la moyenne (selon le delay())
		Temperature[t] = Temp * 100;
		for(int i = 0; i < t; i = i + 1) {
			TempMoy = ((Temperature[i] / 100.00) + TempMoy) / 2;
		}
		t = t + 1;
	}
	else {
		t = 0;
		TempSum = 0.00;
		if(TempMoy <= (TempObj)) {
			digitalWrite(Bleu, HIGH);
			digitalWrite(Vert, LOW);
			digitalWrite(Rouge, LOW);
			digitalWrite(Relais, HIGH);
			RelaisActif = 1;
		}
		else if(TempMoy >= (TempObj + 1)) {
			digitalWrite(Bleu, LOW);
			digitalWrite(Vert, LOW);
			digitalWrite(Rouge, HIGH);
			digitalWrite(Relais, LOW);
			RelaisActif = 0;
		}
		else {
			digitalWrite(Bleu, LOW);
			digitalWrite(Vert, HIGH);
			digitalWrite(Rouge, LOW);
			digitalWrite(Relais, LOW);
			RelaisActif = 0;
		}
	}
	delay(2000);
}