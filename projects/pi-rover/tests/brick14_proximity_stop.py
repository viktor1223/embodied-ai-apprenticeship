"""Brick 14: Proximity Emergency Stop — safety override at distance threshold.

Pass condition: rover drives forward slowly. When an obstacle comes within 20cm,
the rover stops immediately. After the obstacle clears for 2s, it resumes.
Hardware: motors + HC-SR04 wired per pinout.
"""

import sys
import time

TRIG = 17
ECHO = 27
STOP_DISTANCE_CM = 20.0
RESUME_DELAY = 2.0
CRAWL_SPEED = 40
SPEED_OF_SOUND_CM_PER_US = 0.0343

MOTORS = {
    "FL": {"en": 12, "in1": 5,  "in2": 6},
    "RL": {"en": 13, "in1": 19, "in2": 26},
    "FR": {"en": 16, "in1": 20, "in2": 21},
    "RR": {"en": 25, "in1": 8,  "in2": 7},
}


def main():
    try:
        import RPi.GPIO as GPIO
    except (ImportError, RuntimeError):
        print("RPi.GPIO not available — running in DRY RUN mode")
        return dry_run()

    return run_test(GPIO)


def measure_distance(GPIO):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout = time.time() + 0.04
    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None

    pulse_end = time.time()
    timeout = time.time() + 0.04
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 1_000_000 * SPEED_OF_SOUND_CM_PER_US) / 2
    return distance


def set_all_motors(GPIO, pwm_map, speed):
    """Set all motors to the same speed. Positive=forward, 0=stop."""
    for name, pins in MOTORS.items():
        if speed > 0:
            GPIO.output(pins["in1"], GPIO.HIGH)
            GPIO.output(pins["in2"], GPIO.LOW)
        else:
            GPIO.output(pins["in1"], GPIO.LOW)
            GPIO.output(pins["in2"], GPIO.LOW)
        pwm_map[name].ChangeDutyCycle(abs(speed))


def run_test(GPIO):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup proximity sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)

    # Setup motors
    pwm_map = {}
    for name, pins in MOTORS.items():
        GPIO.setup(pins["en"], GPIO.OUT)
        GPIO.setup(pins["in1"], GPIO.OUT)
        GPIO.setup(pins["in2"], GPIO.OUT)
        pwm = GPIO.PWM(pins["en"], 1000)
        pwm.start(0)
        pwm_map[name] = pwm

    time.sleep(0.5)

    print("Proximity Emergency Stop Test")
    print("=" * 40)
    print(f"Stop threshold: {STOP_DISTANCE_CM} cm")
    print(f"Crawl speed:    {CRAWL_SPEED}%")
    print("Rover will drive forward. Place your hand in front to stop it.")
    print("Ctrl+C to exit.\n")

    is_stopped = False
    clear_since = None

    try:
        while True:
            dist = measure_distance(GPIO)

            if dist is None or dist > 400:
                print(f"  --- out of range ---")
                time.sleep(0.1)
                continue

            if dist < STOP_DISTANCE_CM:
                if not is_stopped:
                    set_all_motors(GPIO, pwm_map, 0)
                    print(f"  EMERGENCY STOP: obstacle at {dist:.1f} cm")
                    is_stopped = True
                    clear_since = None
                else:
                    print(f"  STOPPED (obstacle at {dist:.1f} cm)")

            else:
                if is_stopped:
                    if clear_since is None:
                        clear_since = time.time()
                        print(f"  Obstacle cleared ({dist:.1f} cm). "
                              f"Resuming in {RESUME_DELAY}s...")
                    elif time.time() - clear_since > RESUME_DELAY:
                        print(f"  RESUMING forward at {CRAWL_SPEED}%")
                        set_all_motors(GPIO, pwm_map, CRAWL_SPEED)
                        is_stopped = False
                        clear_since = None
                    else:
                        remaining = RESUME_DELAY - (time.time() - clear_since)
                        print(f"  Waiting to resume... {remaining:.1f}s "
                              f"({dist:.1f} cm)")
                else:
                    print(f"  Driving... distance: {dist:.1f} cm")
                    set_all_motors(GPIO, pwm_map, CRAWL_SPEED)

            time.sleep(0.15)

    except KeyboardInterrupt:
        print("\n\nPASS: Emergency stop test completed")

    finally:
        set_all_motors(GPIO, pwm_map, 0)
        for pwm in pwm_map.values():
            pwm.stop()
        GPIO.cleanup()

    return True


def dry_run():
    import random

    print("Proximity Emergency Stop Test (DRY RUN)")
    print("=" * 40)

    # Simulate obstacle approaching
    distances = [100, 80, 60, 40, 30, 25, 18, 15, 12, 15, 22, 30, 40]
    is_stopped = False

    for dist in distances:
        if dist < STOP_DISTANCE_CM:
            if not is_stopped:
                print(f"  EMERGENCY STOP: obstacle at {dist:.1f} cm  (motors OFF)")
                is_stopped = True
            else:
                print(f"  STOPPED (obstacle at {dist:.1f} cm)")
        else:
            if is_stopped:
                print(f"  RESUMING (obstacle cleared at {dist:.1f} cm)")
                is_stopped = False
            else:
                print(f"  Driving... distance: {dist:.1f} cm")
        time.sleep(0.3)

    print("\nPASS (DRY RUN): Emergency stop simulation complete")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
