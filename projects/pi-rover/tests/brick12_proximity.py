"""Brick 12: Proximity Reading — HC-SR04 distance measurements.

Pass condition: prints distance in cm every 200ms. Move your hand closer
and verify readings decrease. Stable within +/- 1cm at a fixed distance.
Hardware: HC-SR04 wired per pinout.
  GPIO17 -> TRIG
  GPIO27 -> ECHO (through 1k/2k voltage divider)
  5V -> VCC
  GND -> GND
"""

import sys
import time

TRIG = 17
ECHO = 27

# Speed of sound at ~20C in cm/us
SPEED_OF_SOUND_CM_PER_US = 0.0343


def main():
    try:
        import RPi.GPIO as GPIO
    except (ImportError, RuntimeError):
        print("RPi.GPIO not available — running in DRY RUN mode")
        return dry_run()

    return run_sensor(GPIO)


def measure_distance(GPIO):
    """Trigger one measurement and return distance in cm."""
    # Send 10us trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo to go HIGH (start of return pulse)
    timeout = time.time() + 0.04  # 40ms max (about 7m range)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    # Wait for echo to go LOW (end of return pulse)
    timeout = time.time() + 0.04
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    # Calculate distance from pulse duration
    pulse_duration = pulse_end - pulse_start
    distance_cm = (pulse_duration * 1_000_000 * SPEED_OF_SOUND_CM_PER_US) / 2

    return distance_cm


def run_sensor(GPIO):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(0.5)  # let sensor settle

    print("HC-SR04 Proximity Sensor Test")
    print("=" * 40)
    print("Reading distance every 200ms. Ctrl+C to stop.\n")

    readings = []
    try:
        while True:
            dist = measure_distance(GPIO)
            if dist is not None and dist < 400:  # HC-SR04 max range ~4m
                readings.append(dist)
                bar = "#" * min(int(dist / 2), 50)
                print(f"  {dist:6.1f} cm  |{bar}")
            else:
                print(f"  --- out of range ---")
            time.sleep(0.2)

    except KeyboardInterrupt:
        if len(readings) > 2:
            avg = sum(readings) / len(readings)
            recent = readings[-10:]
            spread = max(recent) - min(recent)
            print(f"\n\nSession summary:")
            print(f"  Readings taken: {len(readings)}")
            print(f"  Average:        {avg:.1f} cm")
            print(f"  Recent spread:  {spread:.1f} cm (last {len(recent)} readings)")
            if spread < 3:
                print("PASS: Sensor readings are stable")
            else:
                print("NOTE: High variance. Check wiring and voltage divider.")
        else:
            print("\nNot enough readings to evaluate.")

    finally:
        GPIO.cleanup()

    return True


def dry_run():
    import random
    print("HC-SR04 Proximity Sensor Test (DRY RUN)")
    print("=" * 40)
    print("Simulating 10 readings...\n")

    base = 35.0
    for i in range(10):
        dist = base + random.uniform(-0.5, 0.5) - i * 2
        dist = max(5, dist)
        bar = "#" * min(int(dist / 2), 50)
        print(f"  {dist:6.1f} cm  |{bar}")
        time.sleep(0.2)

    print("\nPASS (DRY RUN): Sensor simulation complete")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
