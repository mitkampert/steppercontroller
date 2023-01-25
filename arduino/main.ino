#include <Wire.h>


int PUL = 10;
int DIR_PI = 2;
int DIR = 9;
int ENA_PI = 3;
int ENA = 11;

int throt = 0;

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR_PI, INPUT);
  pinMode(DIR, OUTPUT);
  pinMode(ENA_PI, INPUT);
  pinMode(ENA, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if (Serial.available() > 0) {
    throt = Serial.read() - 33;
  }

  if (digitalRead(ENA_PI) == 1 && throt < 8) {
    digitalWrite(ENA, HIGH);
  }
  else {
    digitalWrite(ENA, LOW);
  }

  if (digitalRead(DIR_PI) == 0) {
    digitalWrite(DIR, LOW);
  }
  else if (digitalRead(DIR_PI) == 1) {
    digitalWrite(DIR, HIGH);
  }

  if (throt >= 8) {
    digitalWrite(PUL, HIGH);   
    delayMicroseconds(50000/throt);               
    digitalWrite(PUL, LOW);    
    delayMicroseconds(50000/throt); 
  }                     
}