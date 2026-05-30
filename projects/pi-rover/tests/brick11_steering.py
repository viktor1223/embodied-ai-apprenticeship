"""Brick 11: Steering Patterns — forward, backward, turn left, turn right.

Pass condition: rover executes each maneuver in sequence.
Verify the chassis moves in the expected direction for each.
Hardware: all 4 motors wired, chassis assembled.

Differential steering model:
  Forward:    all motors forward
  Backward:   all motors backward
  Turn left:  right motors forward, left motors stopped (or reversed)
  Turn right: left motors forward, right motors stopped (or reversed)
"""

import sys
import time

MOTORS = {
    "FL": {"en": 12, "in1": 5,  "in2": 6},
    "RL": {"en": 13, "in1": 19, "in2": 26},
    "FR": {"en": 16, "in1": 20, "in2": 21},
    "RR": {"en": 25, "in1": 8,  "in2": 7},
}

LEFT_MOTORS = ["FL", "RL"]
RIGHT_MOTORS = ["FR", "RR"]

DRIVE_TIME = 2.0
PAUSE_TIME = 1.0
SPEED = 60


def main():
    try:
        import RPi.GPIO as GPIO
    except (ImportError, RuntimeError):
        print("RPi.GPIO not available — running in DRY RUN mode")
        return dry_run()

    return run_test(GPIO)


class MotorDriver:
    """Simple wrapper for L298N motor control via GPIO."""

    def __init__(self, GPIO):
        self.GPIO = GPIO
        self.pwm = {}

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for name, pins in MOTORS.items():
            GPIO.setup(pins["en"], GPIO.OUT)
            GPIO.setup(pins["in1"], GPIO.OUT)
            GPIO.setup(pins["in2"], GPIO.OUT)
            pwm = GPIO.PWM(pins["en"], 1000)
            pwm.start(0)
            self.pwm[name] = pwm

    def set_motor(self, name, speed):
        """Set motor speed: positive=forward, negative=backward, 0=stop."""
        pins = MOTORS[name]
        if speed > 0:
            self.GPIO.output(pins["in1"], self.GPIO.HIGH)
            self.GPIO.output(pins["in2"], self.GPIO.LOW)
        elif speed < 0:
            self.GPIO.output(pins["in1"], self.GPIO.LOW)
            self.GPIO.output(pins["in2"], self.GPIO.HIGH)
        else:
            self.GPIO.output(pins["in1"], self.GPIO.LOW)
            self.GPIO.output(pins["in2"], self.GPIO.LOW)
        self.pwm[name].ChangeDutyCycle(abs(speed))

    def forward(self, speed):
        for m in MOTORS:
            self.set_motor(m, speed)

    def backward(self, speed):
        for m in MOTORS:
            self.set_motor(m, -speed)

    def turn_left(self, speed):
        for m in LEFT_MOTORS:
            self.set_motor(m, 0)
        for m in RIGHT_MOTORS:
            self.set_motor(m, speed)

    def turn_right(self, speed):
        for m in LEFT_MOTORS:
            self.set_motor(m, speed)
        for m in RIGHT_MOTORS:
            self.set_motor(m, 0)

    def stop(self):
        for m in MOTORS:
            self.set_motor(m, 0)

    def cleanup(self):
        self.stop()
        for pwm in self.pwm.values():
            pwm.stop()
        self.GPIO.cleanup()


def run_test(GPIO):
    driver = MotorDriver(GPIO)

    maneuvers = [
        ("FORWARD",    driver.forward),
        ("BACKWARD",   driver.backward),
        ("TURN LEFT",  driver.turn_left),
        ("TURN RIGHT", driver.turn_right),
    ]

    try:
        print("Steering Patterns Test")
        print("=" * 40)
        print("Place the rover on a flat surface with room to move.\n")

        for name, func in maneuvers:
            print(f"  {name} at {SPEED}% for {DRIVE_TIME}s...")
            func(SPEED)
            time.sleep(DRIVE_TIME)

            print(f"  STOP for {PAUSE_TIME}s")
            driver.stop()
            time.sleep(PAUSE_TIME)

        print("\n" + "=" * 40)
        print("PASS: All steering patterns executed")
        print("Verify the rover moved correctly for each maneuver.")
        return True

    finally:
        driver.cleanup()


def dry_run():
    maneuvers = [
        ("FORWARD",    "all motors forward"),
        ("BACKWARD",   "all motors backward"),
        ("TURN LEFT",  "right motors forward, left stopped"),
        ("TURN RIGHT", "left motors forward, right stopped"),
    ]

    print("Steering Patterns Test (DRY RUN)")
    print("=" * 40)
    for name, desc in maneuvers:
        print(f"  {name}: {desc}")
        time.sleep(0.5)
        print(f"  STOP")
    print("\nPASS (DRY RUN): Steering sequence simulated")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
