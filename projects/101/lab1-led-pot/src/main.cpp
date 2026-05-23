#include <Arduino.h>

const int analogInPin = A0;   // Potentiometer wiper
const int analogOutPin = 9;   // LED on PWM pin

int sensorValue = 0;
int outputValue = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  sensorValue = analogRead(analogInPin);             // Read pot: 0–1023
  outputValue = map(sensorValue, 0, 1023, 0, 255);  // Scale to PWM: 0–255
  analogWrite(analogOutPin, outputValue);            // Drive LED brightness

  Serial.print("sensor = ");
  Serial.print(sensorValue);
  Serial.print("\t output = ");
  Serial.println(outputValue);

  delay(2);
}
