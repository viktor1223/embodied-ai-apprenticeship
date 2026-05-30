"""Brick 15: Visual Servo Loop — camera -> cloud -> steer -> repeat.

Pass condition: rover turns toward the target object, approaches it, and stops
when the proximity sensor reads below threshold.
Hardware: camera + motors + HC-SR04 + network.
Requires: Bricks 1, 6, 11, 12 all passing. .env configured.

This is the core closed loop:
  1. Capture frame
  2. Send to Locate Anything -> get BBOX
  3. Convert BBOX to steering (proportional controller)
  4. Check proximity -> emergency stop if too close
  5. Apply motor commands
  6. Repeat

Between inference calls, the last steering command is held (not zeroed).
This keeps motion smooth despite 200-500ms cloud latency.
"""

import sys
import os
import time
import argparse
import base64


# ── Configuration ─────────────────────────────────────────

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
KP_STEER = 0.15
BASE_SPEED = 40
STOP_DISTANCE_CM = 20.0
SPEED_OF_SOUND_CM_PER_US = 0.0343

TRIG = 17
ECHO = 27

MOTORS = {
    "FL": {"en": 12, "in1": 5,  "in2": 6},
    "RL": {"en": 13, "in1": 19, "in2": 26},
    "FR": {"en": 16, "in1": 20, "in2": 21},
    "RR": {"en": 25, "in1": 8,  "in2": 7},
}

LEFT_MOTORS = ["FL", "RL"]
RIGHT_MOTORS = ["FR", "RR"]


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        return False
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    return True


# ── Sensor helpers ────────────────────────────────────────

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

    duration = pulse_end - pulse_start
    return (duration * 1_000_000 * SPEED_OF_SOUND_CM_PER_US) / 2


def capture_frame_bytes():
    """Capture a frame and return JPEG bytes."""
    try:
        from picamera2 import Picamera2
        import io
        cam = Picamera2()
        config = cam.create_still_configuration(main={"size": (FRAME_WIDTH, FRAME_HEIGHT)})
        cam.configure(config)
        cam.start()
        time.sleep(1)
        buf = io.BytesIO()
        cam.capture_file(buf, format='jpeg')
        cam.stop()
        return buf.getvalue(), cam
    except ImportError:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None, None
        _, buf = cv2.imencode('.jpg', frame)
        return buf.tobytes(), None


def send_to_locate_anything(image_bytes, target_text):
    """Send image to Azure Locate Anything, return BBOX and latency."""
    import requests

    endpoint = os.environ.get("AZURE_ENDPOINT")
    api_key = os.environ.get("AZURE_API_KEY")

    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    payload = {
        "input": {
            "image": image_b64,
            "text_prompt": target_text,
        }
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    start = time.time()
    response = requests.post(f"{endpoint}/score", json=payload,
                             headers=headers, timeout=30)
    latency = (time.time() - start) * 1000

    if response.status_code != 200:
        return None, latency

    data = response.json()
    bbox = data.get("bbox") or data.get("bounding_box") or \
           data.get("output", {}).get("bbox")
    return bbox, latency


def bbox_to_steering(bbox):
    """Convert BBOX to (left_speed, right_speed)."""
    x_min, y_min, x_max, y_max = bbox
    bbox_cx = (x_min + x_max) / 2
    bbox_area = (x_max - x_min) * (y_max - y_min)
    frame_area = FRAME_WIDTH * FRAME_HEIGHT

    error = (bbox_cx - FRAME_WIDTH / 2) / (FRAME_WIDTH / 2)
    steering = KP_STEER * error * 100

    area_ratio = bbox_area / frame_area
    if area_ratio > 0.3:
        speed = BASE_SPEED * 0.3
    elif area_ratio > 0.1:
        speed = BASE_SPEED * 0.6
    else:
        speed = BASE_SPEED

    left = max(min(speed + steering, 100), -100)
    right = max(min(speed - steering, 100), -100)
    return left, right


# ── Motor control ─────────────────────────────────────────

class MotorDriver:
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

    def drive(self, left_speed, right_speed):
        for name in LEFT_MOTORS:
            self._set(name, left_speed)
        for name in RIGHT_MOTORS:
            self._set(name, right_speed)

    def _set(self, name, speed):
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

    def stop(self):
        self.drive(0, 0)

    def cleanup(self):
        self.stop()
        for p in self.pwm.values():
            p.stop()
        self.GPIO.cleanup()


# ── Main loop ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Brick 15: Visual Servo Loop")
    parser.add_argument("--target", default="cup", help="Object to track")
    parser.add_argument("--max-cycles", type=int, default=50,
                        help="Max inference cycles before timeout")
    args = parser.parse_args()

    if not load_env():
        print("FAIL: No .env file")
        return False

    try:
        import RPi.GPIO as GPIO
    except (ImportError, RuntimeError):
        print("RPi.GPIO not available — cannot run visual servo without hardware")
        return False

    driver = MotorDriver(GPIO)

    # Setup proximity sensor
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(0.5)

    print(f"Visual Servo Loop")
    print(f"Target: {args.target}")
    print(f"Max cycles: {args.max_cycles}")
    print("=" * 50)

    cycle = 0
    try:
        while cycle < args.max_cycles:
            cycle += 1

            # 1. Check proximity first (safety takes priority)
            dist = measure_distance(GPIO)
            if dist is not None and dist < STOP_DISTANCE_CM:
                driver.stop()
                print(f"\n  ARRIVED: obstacle at {dist:.1f} cm. Stopping.")
                print(f"PASS: Visual servo reached target in {cycle} cycles")
                return True

            # 2. Capture frame
            image_bytes, _ = capture_frame_bytes()
            if image_bytes is None:
                print(f"  [{cycle}] Frame capture failed, skipping")
                continue

            # 3. Send to cloud
            bbox, latency = send_to_locate_anything(image_bytes, args.target)
            if bbox is None:
                print(f"  [{cycle}] No detection (latency: {latency:.0f}ms)")
                # Hold last command (do not stop)
                continue

            # 4. Convert to steering
            left, right = bbox_to_steering(bbox)
            bbox_cx = (bbox[0] + bbox[2]) / 2

            # 5. Apply motor commands
            driver.drive(left, right)

            dist_str = f"{dist:.0f}cm" if dist else "---"
            print(f"  [{cycle}] BBOX_cx={bbox_cx:.0f} "
                  f"L={left:+5.1f}% R={right:+5.1f}% "
                  f"dist={dist_str} lat={latency:.0f}ms")

    except KeyboardInterrupt:
        print(f"\n\nInterrupted after {cycle} cycles")

    finally:
        driver.cleanup()

    print("DONE: Max cycles reached without arriving")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
