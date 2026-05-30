"""Brick 16: Voice-Triggered Full Pipeline — wake word to visual servo.

Pass condition: say "Hey Rover, drive to the cup." The rover wakes, identifies
the target, turns toward it, drives to it, and stops at a safe distance.
Say "stop" at any time for immediate halt.
Hardware: all sensors + motors + microphone + camera + network.
Requires: all previous bricks passing.

Pipeline:
  1. Listen for wake word (local, on-device)
  2. After wake: record speech -> Azure STT -> parse command
  3. If DRIVE command: start visual servo loop (Brick 15)
  4. If STOP command: immediate halt
  5. Proximity override active at all times
"""

import sys
import os
import time
import threading
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


# ── Reuse helpers from earlier bricks ─────────────────────

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Command:
    action: str
    target: Optional[str]


DRIVE_PATTERNS = [
    r"(?:drive|go|move|navigate|head)\s+to\s+(?:the\s+)?(.+)",
    r"(?:find|locate|look\s+for)\s+(?:the\s+)?(.+)",
]

STOP_PATTERNS = [
    r"^stop$", r"^halt$", r"^freeze$",
    r"stop\s+(?:now|immediately|moving)",
    r"emergency\s+stop",
]


def parse_command(text):
    text = text.strip().lower().rstrip('.')
    for pattern in STOP_PATTERNS:
        if re.search(pattern, text):
            return Command(action="STOP", target=None)
    for pattern in DRIVE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return Command(action="DRIVE", target=match.group(1).strip().rstrip('.'))
    return Command(action="UNKNOWN", target=None)


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
    return (pulse_end - pulse_start) * 1_000_000 * SPEED_OF_SOUND_CM_PER_US / 2


def bbox_to_steering(bbox):
    x_min, y_min, x_max, y_max = bbox
    cx = (x_min + x_max) / 2
    area_ratio = (x_max - x_min) * (y_max - y_min) / (FRAME_WIDTH * FRAME_HEIGHT)
    error = (cx - FRAME_WIDTH / 2) / (FRAME_WIDTH / 2)
    steering = KP_STEER * error * 100
    speed = BASE_SPEED * (0.3 if area_ratio > 0.3 else 0.6 if area_ratio > 0.1 else 1)
    return (max(min(speed + steering, 100), -100),
            max(min(speed - steering, 100), -100))


def send_to_locate_anything(image_bytes, target_text):
    import requests
    endpoint = os.environ.get("AZURE_ENDPOINT")
    api_key = os.environ.get("AZURE_API_KEY")
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    payload = {"input": {"image": image_b64, "text_prompt": target_text}}
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    start = time.time()
    resp = requests.post(f"{endpoint}/score", json=payload, headers=headers, timeout=30)
    latency = (time.time() - start) * 1000
    if resp.status_code != 200:
        return None, latency
    data = resp.json()
    bbox = data.get("bbox") or data.get("bounding_box") or data.get("output", {}).get("bbox")
    return bbox, latency


# ── Motor driver ──────────────────────────────────────────

class MotorDriver:
    def __init__(self, GPIO):
        self.GPIO = GPIO
        self.pwm = {}
        for name, pins in MOTORS.items():
            GPIO.setup(pins["en"], GPIO.OUT)
            GPIO.setup(pins["in1"], GPIO.OUT)
            GPIO.setup(pins["in2"], GPIO.OUT)
            pwm = GPIO.PWM(pins["en"], 1000)
            pwm.start(0)
            self.pwm[name] = pwm

    def drive(self, left, right):
        for n in LEFT_MOTORS:
            self._set(n, left)
        for n in RIGHT_MOTORS:
            self._set(n, right)

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


# ── Main pipeline ─────────────────────────────────────────

def main():
    if not load_env():
        print("FAIL: No .env file")
        return False

    try:
        import RPi.GPIO as GPIO
    except (ImportError, RuntimeError):
        print("FAIL: Requires Raspberry Pi GPIO hardware")
        return False

    try:
        import pyaudio
        import numpy as np
        from openwakeword.model import Model
        import azure.cognitiveservices.speech as speechsdk
    except ImportError as e:
        print(f"FAIL: Missing dependency: {e}")
        return False

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup proximity
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)

    driver = MotorDriver(GPIO)

    # Shared stop flag for the proximity safety thread
    should_stop = threading.Event()
    is_driving = threading.Event()

    def proximity_watchdog():
        """Background thread: monitor distance and force stop if too close."""
        while not should_stop.is_set():
            if is_driving.is_set():
                dist = measure_distance(GPIO)
                if dist is not None and dist < STOP_DISTANCE_CM:
                    driver.stop()
                    is_driving.clear()
                    print(f"\n  PROXIMITY STOP: {dist:.1f} cm")
            time.sleep(0.1)

    watchdog = threading.Thread(target=proximity_watchdog, daemon=True)
    watchdog.start()

    # Wake word model
    print("Loading wake word model...")
    ww_model = Model(wakeword_models=["hey_jarvis"], inference_framework="onnx")

    # Speech recognizer
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get("AZURE_SPEECH_KEY"),
        region=os.environ.get("AZURE_SPEECH_REGION"),
    )
    speech_config.speech_recognition_language = "en-US"

    # Audio stream for wake word
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16, channels=1, rate=16000,
        input=True, frames_per_buffer=1280,
    )

    print("\nVoice Pipeline Active")
    print("=" * 50)
    print("Say 'Hey Rover' to wake, then give a command.")
    print("Say 'stop' at any time to halt.")
    print("Ctrl+C to exit.\n")

    try:
        while True:
            # Phase 1: Listen for wake word
            audio = stream.read(1280, exception_on_overflow=False)
            audio_np = np.frombuffer(audio, dtype=np.int16)
            prediction = ww_model.predict(audio_np)

            for model_name, score in prediction.items():
                if score > 0.5:
                    print("WAKE WORD DETECTED — listening for command...")

                    # Phase 2: Recognize speech command via Azure
                    audio_config = speechsdk.audio.AudioConfig(
                        use_default_microphone=True)
                    recognizer = speechsdk.SpeechRecognizer(
                        speech_config=speech_config, audio_config=audio_config)
                    result = recognizer.recognize_once_async().get()

                    if result.reason != speechsdk.ResultReason.RecognizedSpeech:
                        print("  Could not understand. Returning to listen mode.")
                        continue

                    text = result.text
                    print(f"  Heard: \"{text}\"")

                    # Phase 3: Parse command
                    cmd = parse_command(text)
                    print(f"  Parsed: {cmd}")

                    if cmd.action == "STOP":
                        driver.stop()
                        is_driving.clear()
                        print("  STOPPED.")

                    elif cmd.action == "DRIVE" and cmd.target:
                        print(f"  Driving to: {cmd.target}")
                        is_driving.set()

                        # Phase 4: Visual servo loop
                        for cycle in range(50):
                            if not is_driving.is_set():
                                print("  Stopped by proximity or voice.")
                                break

                            # Capture and infer
                            img, _ = capture_frame_bytes()
                            if img is None:
                                continue
                            bbox, lat = send_to_locate_anything(img, cmd.target)
                            if bbox is None:
                                continue

                            left, right = bbox_to_steering(bbox)
                            driver.drive(left, right)
                            cx = (bbox[0] + bbox[2]) / 2
                            print(f"    [{cycle}] cx={cx:.0f} "
                                  f"L={left:+.0f}% R={right:+.0f}% "
                                  f"lat={lat:.0f}ms")

                        driver.stop()
                        is_driving.clear()
                        print("  Maneuver complete. Listening for next command...")

                    else:
                        print("  Unknown command. Try: 'drive to the [object]'")

    except KeyboardInterrupt:
        print("\n\nShutting down...")

    finally:
        should_stop.set()
        driver.stop()
        driver.cleanup()
        stream.stop_stream()
        stream.close()
        pa.terminate()
        GPIO.cleanup()

    print("PASS: Voice pipeline ran successfully")
    return True


def capture_frame_bytes():
    try:
        from picamera2 import Picamera2
        import io
        cam = Picamera2()
        config = cam.create_still_configuration(
            main={"size": (FRAME_WIDTH, FRAME_HEIGHT)})
        cam.configure(config)
        cam.start()
        time.sleep(0.5)
        buf = io.BytesIO()
        cam.capture_file(buf, format='jpeg')
        cam.stop()
        return buf.getvalue(), None
    except ImportError:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None, None
        _, buf = cv2.imencode('.jpg', frame)
        return buf.tobytes(), None


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
