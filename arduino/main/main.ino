#include <Wire.h>


int DIR_PI = 2;
int ENA_PI = 3;
int MANUAL = 4;
int DIR = 9;
int PUL = 10;
int ENA = 11;


int throt = 0;
int steps = 0;

void setup() {
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT);
  pinMode(ENA, OUTPUT);
  
  pinMode(ENA_PI, INPUT);
  pinMode(DIR_PI, INPUT);
  pinMode(MANUAL, INPUT);

  Serial.begin(9600);
}

void loop() {

  while (digitalRead(MANUAL) == 0) {
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
  while (digitalRead(MANUAL) == 1) {
    if (Serial.available() > 0) {
      steps = Serial.parseInt(SKIP_ALL, '\n');
    }

    if (digitalRead(DIR_PI) == 0) {
      digitalWrite(DIR, LOW);
    }
    else if (digitalRead(DIR_PI) == 1) {
      digitalWrite(DIR, HIGH);
    }

    for (int n = 0; n < steps; n++) {
      digitalWrite(PUL, HIGH);   
      delayMicroseconds(1000);               
      digitalWrite(PUL, LOW);    
      delayMicroseconds(1000);
    }
  }                    
}