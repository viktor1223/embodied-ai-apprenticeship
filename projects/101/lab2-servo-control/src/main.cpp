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
  // Average multiple reads — 850k pot has high impedance, single reads are noisy
  long sum = 0;
  for (int i = 0; i < 10; i++) {
    sum += analogRead(potPin);
    delay(2);
  }
  potValue = sum / 10;

  angle = map(potValue, 0, 1023, 0, 180);
  myservo.write(angle);

  Serial.print("pot = ");
  Serial.print(potValue);
  Serial.print("\t angle = ");
  Serial.println(angle);

  delay(15);
}
