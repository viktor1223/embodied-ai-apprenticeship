#include <Arduino.h>
#include <Servo.h>

Servo myservo;

const int potPin = A0;
const int servoPin = 7;

int potValue = 0;
int angle = 0;

void setup() {
  myservo.attach(servoPin);
  Serial.begin(9600);
}

void loop() {
  potValue = analogRead(potPin);           // Read pot: 0–1023
  angle = map(potValue, 0, 1023, 0, 180);  // Convert to servo angle: 0–180
  myservo.write(angle);                     // Send angle to servo

  Serial.print("pot = ");
  Serial.print(potValue);
  Serial.print("\t angle = ");
  Serial.println(angle);

  delay(15);  // Give servo time to move
}
