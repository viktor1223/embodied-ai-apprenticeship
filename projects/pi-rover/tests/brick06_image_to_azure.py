"""Brick 6: Image to Azure — capture a frame and send to Locate Anything.

Pass condition: prints BBOX coordinates, confidence, and round-trip latency.
Hardware: Pi + camera (or webcam fallback).
Requires: Bricks 1 and 5 passing. .env file configured.

Usage: python3 brick06_image_to_azure.py --target "cup"
"""

import sys
import os
import time
import argparse
import base64


def load_env():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if not os.path.exists(env_path):
        print("FAIL: No .env file. Run brick05 first.")
        return False
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    return True


def capture_frame():
    """Capture a single frame and return it as JPEG bytes."""
    try:
        from picamera2 import Picamera2
        cam = Picamera2()
        config = cam.create_still_configuration(main={"size": (640, 480)})
        cam.configure(config)
        cam.start()
        time.sleep(2)
        import io
        data = io.BytesIO()
        cam.capture_file(data, format='jpeg')
        cam.stop()
        return data.getvalue()
    except ImportError:
        pass

    import cv2
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    _, buf = cv2.imencode('.jpg', frame)
    return buf.tobytes()


def send_to_locate_anything(image_bytes, target_text):
    """Send image + text prompt to Nvidia Locate Anything via Azure endpoint."""
    import requests

    endpoint = os.environ.get("AZURE_ENDPOINT")
    api_key = os.environ.get("AZURE_API_KEY")

    if not endpoint or not api_key:
        print("FAIL: AZURE_ENDPOINT and AZURE_API_KEY not set")
        return None

    # Encode image as base64 for the API payload
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')

    # Nvidia Locate Anything API format
    # Adjust this payload structure to match your specific deployment
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

    url = f"{endpoint}/score"
    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    latency_ms = (time.time() - start_time) * 1000

    if response.status_code != 200:
        print(f"FAIL: API returned {response.status_code}")
        print(f"  Body: {response.text[:500]}")
        return None

    result = response.json()
    return result, latency_ms


def main():
    parser = argparse.ArgumentParser(description="Brick 6: Image to Azure")
    parser.add_argument("--target", default="cup",
                        help="Object to locate (e.g., 'cup', 'red ball')")
    args = parser.parse_args()

    if not load_env():
        return False

    print(f"Target: {args.target}")
    print("Capturing frame...")

    image_bytes = capture_frame()
    if image_bytes is None:
        print("FAIL: Could not capture frame")
        return False

    print(f"  Frame size: {len(image_bytes) / 1024:.1f} KB")
    print(f"Sending to Locate Anything...")

    result = send_to_locate_anything(image_bytes, args.target)
    if result is None:
        return False

    data, latency_ms = result

    # Parse the bounding box from the response
    # Adjust these keys to match your actual API response format
    bbox = data.get("bbox") or data.get("bounding_box") or data.get("output", {}).get("bbox")
    confidence = data.get("confidence") or data.get("score") or data.get("output", {}).get("score")

    print(f"\nPASS: Locate Anything returned a result")
    print(f"  Target:     {args.target}")
    print(f"  BBOX:       {bbox}")
    print(f"  Confidence: {confidence}")
    print(f"  Latency:    {latency_ms:.0f}ms")
    print(f"  Raw:        {data}")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
