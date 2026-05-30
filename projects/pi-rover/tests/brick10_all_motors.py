"""Brick 10: All Four Motors — spin each motor individually in sequence.

Pass condition: each motor spins one at a time with its name printed.
Verify each physical motor matches its label (FL, RL, FR, RR).
Hardware: all 4 motors wired to both L298N modules per pinout.
"""

import sys
import time

# Pin assignments from pinout-and-wiring.md
MOTORS = {
    "Front-Left (FL)": {"en": 12, "in1": 5,  "in2": 6},   # L298N_L Ch.A
    "Rear-Left (RL)":  {"en": 13, "in1": 19, "in2": 26},  # L298N_L Ch.B
    "Front-Right (FR)":{"en": 16, "in1": 20, "in2": 21},  # L298N_R Ch.A
    "Rear-Right (RR)": {"en": 25, "in1": 8,  "in2": 7},   # L298N_R Ch.B
}

SPIN_TIME = 2.0   # seconds per motor
PAUSE_TIME = 1.0
SPEED = 60         # % duty cycle


def main():
    try:
        import RPi.GPIO as GPIO
    except (ImportError, RuntimeError):
        print("RPi.GPIO not available — running in DRY RUN mode")
        return dry_run()

    return run_test(GPIO)


def run_test(GPIO):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    pwm_channels = {}

    # Set up all pins
    for name, pins in MOTORS.items():
        GPIO.setup(pins["en"], GPIO.OUT)
        GPIO.setup(pins["in1"], GPIO.OUT)
        GPIO.setup(pins["in2"], GPIO.OUT)
        pwm = GPIO.PWM(pins["en"], 1000)
        pwm.start(0)
        pwm_channels[name] = pwm

    try:
        print("All Four Motors Test")
        print("=" * 40)
        print(f"Each motor spins for {SPIN_TIME}s at {SPEED}% speed")
        print("Verify the correct physical motor spins for each label.\n")

        for name, pins in MOTORS.items():
            print(f"  Spinning: {name}...")
            GPIO.output(pins["in1"], GPIO.HIGH)
            GPIO.output(pins["in2"], GPIO.LOW)
            pwm_channels[name].ChangeDutyCycle(SPEED)
            time.sleep(SPIN_TIME)

            # Stop this motor
            pwm_channels[name].ChangeDutyCycle(0)
            GPIO.output(pins["in1"], GPIO.LOW)
            GPIO.output(pins["in2"], GPIO.LOW)
            print(f"  Stopped:  {name}")
            time.sleep(PAUSE_TIME)

        print("\n" + "=" * 40)
        print("PASS: All four motors spun individually")
        print("Verify each motor matched its label above.")
        return True

    finally:
        for pwm in pwm_channels.values():
            pwm.stop()
        GPIO.cleanup()


def dry_run():
    print("All Four Motors Test (DRY RUN)")
    print("=" * 40)
    for name, pins in MOTORS.items():
        print(f"  Spinning: {name}  (EN={pins['en']}, "
              f"IN1={pins['in1']}, IN2={pins['in2']})")
        time.sleep(0.5)
        print(f"  Stopped:  {name}")
    print("\nPASS (DRY RUN): Motor sequence simulated")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
