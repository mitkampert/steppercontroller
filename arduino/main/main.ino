#include <Wire.h>


int DIR_PI = 2;
int ENA_PI = 3;
int MANUAL = 4;
int DIR = 9;
int PUL = 10;
int ENA = 11;


int throt = 0;
long steps = 0;

void setup() {
  pinMode(DIR, OUTPUT);
  pinMode(PUL, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
  pinMode(ENA_PI, INPUT);
  pinMode(DIR_PI, INPUT);
  pinMode(MANUAL, INPUT);

  Serial.begin(9600);
}

void(* resetFunc) (void) = 0;

void loop() {
  digitalWrite(LED_BUILTIN, LOW);
  throt = 0;
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

  digitalWrite(ENA, LOW);

  digitalWrite(LED_BUILTIN, HIGH);
  steps = 0;
  while (digitalRead(MANUAL) == 1) {
    steps = Serial.parseInt();

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
    steps = 0;
  }                    
}