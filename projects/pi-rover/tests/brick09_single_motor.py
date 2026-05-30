"""Brick 9: Single Motor Spin — verify one motor spins forward and backward.

Pass condition: motor spins forward 2s, stops 1s, backward 2s, stops.
Hardware: ONE motor connected to L298N_L Channel A.
  GPIO5  -> IN1
  GPIO6  -> IN2
  GPIO12 -> ENA (PWM)
  Motor  -> OUT1/OUT2
  4xAA battery -> L298N 12V/GND
  Pi GND -> L298N GND
"""

import sys
import time

# GPIO pin assignments for L298N_L Channel A
ENA = 12  # PWM speed control
IN1 = 5   # direction
IN2 = 6   # direction

DRY_RUN = False


def main():
    global DRY_RUN
    try:
        import RPi.GPIO as GPIO
    except (ImportError, RuntimeError):
        print("RPi.GPIO not available — running in DRY RUN mode")
        DRY_RUN = True
        return dry_run()

    return run_motor_test(GPIO)


def run_motor_test(GPIO):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)

    pwm = GPIO.PWM(ENA, 1000)  # 1kHz PWM frequency
    pwm.start(0)

    try:
        # Forward
        print("FORWARD at 70% speed...")
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        pwm.ChangeDutyCycle(70)
        time.sleep(2)

        # Stop
        print("STOP")
        pwm.ChangeDutyCycle(0)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        time.sleep(1)

        # Backward
        print("BACKWARD at 70% speed...")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        pwm.ChangeDutyCycle(70)
        time.sleep(2)

        # Stop
        print("STOP")
        pwm.ChangeDutyCycle(0)
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)

        print("\nPASS: Motor completed forward/stop/backward/stop sequence")
        return True

    finally:
        pwm.stop()
        GPIO.cleanup()


def dry_run():
    """Simulate motor test without GPIO hardware."""
    print("FORWARD at 70% speed...")
    print(f"  IN1=HIGH  IN2=LOW  ENA=70%")
    time.sleep(1)

    print("STOP")
    print(f"  IN1=LOW   IN2=LOW  ENA=0%")
    time.sleep(0.5)

    print("BACKWARD at 70% speed...")
    print(f"  IN1=LOW   IN2=HIGH ENA=70%")
    time.sleep(1)

    print("STOP")
    print(f"  IN1=LOW   IN2=LOW  ENA=0%")

    print("\nPASS (DRY RUN): Motor sequence simulated")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
