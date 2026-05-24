#include <Arduino.h>

// L298N pin assignments (match diagram.json wiring)
#define ENA 9   // PWM — Motor A speed
#define IN1 8   // Motor A direction
#define IN2 7   // Motor A direction
#define IN3 6   // Motor B direction
#define IN4 5   // Motor B direction
#define ENB 10  // PWM — Motor B speed

void setup() {
  Serial.begin(115200);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  Serial.println("Lab 3: DC Motor Control via L298N");
  Serial.println("----------------------------------");
}

// Drive Motor A: speed 0-255, direction true=forward false=reverse
void motorA(int speed, bool forward) {
  digitalWrite(IN1, forward ? HIGH : LOW);
  digitalWrite(IN2, forward ? LOW : HIGH);
  analogWrite(ENA, speed);
}

// Drive Motor B: speed 0-255, direction true=forward false=reverse
void motorB(int speed, bool forward) {
  digitalWrite(IN3, forward ? HIGH : LOW);
  digitalWrite(IN4, forward ? LOW : HIGH);
  analogWrite(ENB, speed);
}

// Stop both motors (brake — both inputs same)
void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

void loop() {
  // Forward at 75% speed
  Serial.println("Both motors FORWARD @ 75%");
  motorA(191, true);
  motorB(191, true);
  delay(2000);

  stopMotors();
  Serial.println("STOPPED");
  delay(1000);

  // Reverse at 50% speed
  Serial.println("Both motors REVERSE @ 50%");
  motorA(127, false);
  motorB(127, false);
  delay(2000);

  stopMotors();
  Serial.println("STOPPED");
  delay(1000);

  // Turn left (A forward, B reverse)
  Serial.println("Turning LEFT (differential drive)");
  motorA(150, true);
  motorB(150, false);
  delay(1500);

  stopMotors();
  Serial.println("STOPPED");
  delay(1000);

  // Turn right (A reverse, B forward)
  Serial.println("Turning RIGHT (differential drive)");
  motorA(150, false);
  motorB(150, true);
  delay(1500);

  stopMotors();
  Serial.println("STOPPED");
  delay(2000);
}
