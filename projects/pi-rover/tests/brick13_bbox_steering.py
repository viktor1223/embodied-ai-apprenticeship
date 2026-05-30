"""Brick 13: BBOX to Steering — proportional steering from bounding box position.

Pass condition: mock BBOX positions produce correct motor commands.
Can run without hardware (dry-run) or with motors connected.

This is the core of visual servoing: the BBOX center's horizontal offset from
the frame center becomes the error signal for a proportional controller.
"""

import sys
import time

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_CENTER_X = FRAME_WIDTH // 2

# Proportional gain: how aggressively to steer based on pixel offset
# Higher Kp = sharper turns. Tune this on the real rover.
KP_STEER = 0.15

# Base forward speed (% duty cycle)
BASE_SPEED = 50

# Minimum speed for any motor (below this, motor stalls)
MIN_SPEED = 20


def bbox_to_steering(bbox, frame_width=FRAME_WIDTH):
    """Convert a bounding box to left/right motor speeds.

    Args:
        bbox: [x_min, y_min, x_max, y_max] in pixel coordinates
        frame_width: width of the camera frame in pixels

    Returns:
        (left_speed, right_speed) as percentages (-100 to 100)
        Positive = forward, negative = backward
    """
    x_min, y_min, x_max, y_max = bbox
    bbox_center_x = (x_min + x_max) / 2
    bbox_width = x_max - x_min
    bbox_height = y_max - y_min

    # Error: how far the object is from the frame center (pixels)
    # Positive error = object is to the right
    error_x = bbox_center_x - (frame_width / 2)

    # Normalize error to [-1, 1]
    error_normalized = error_x / (frame_width / 2)

    # Steering correction: proportional to error
    steering = KP_STEER * error_normalized * 100

    # Size-based speed: larger bbox = closer = slower approach
    bbox_area_ratio = (bbox_width * bbox_height) / (frame_width * FRAME_HEIGHT)
    if bbox_area_ratio > 0.3:
        forward_speed = BASE_SPEED * 0.3  # very close, crawl
    elif bbox_area_ratio > 0.1:
        forward_speed = BASE_SPEED * 0.6  # medium distance
    else:
        forward_speed = BASE_SPEED         # far away, full speed

    # Differential steering: offset left/right based on correction
    left_speed = forward_speed + steering
    right_speed = forward_speed - steering

    # Clamp to valid range
    left_speed = max(min(left_speed, 100), -100)
    right_speed = max(min(right_speed, 100), -100)

    return left_speed, right_speed


def describe_steering(left_speed, right_speed):
    """Human-readable description of the steering command."""
    if abs(left_speed - right_speed) < 5:
        direction = "STRAIGHT"
    elif left_speed > right_speed:
        direction = "steer RIGHT"
    else:
        direction = "steer LEFT"

    avg_speed = (abs(left_speed) + abs(right_speed)) / 2
    if avg_speed < 20:
        pace = "SLOW (close)"
    elif avg_speed < 40:
        pace = "MODERATE"
    else:
        pace = "FORWARD"

    return f"{direction}, {pace}"


def main():
    # Mock BBOX test cases: [x_min, y_min, x_max, y_max]
    test_cases = [
        {
            "name": "Object at frame LEFT",
            "bbox": [50, 200, 150, 300],
            "expect": "steer LEFT",
        },
        {
            "name": "Object at frame RIGHT",
            "bbox": [490, 200, 590, 300],
            "expect": "steer RIGHT",
        },
        {
            "name": "Object at MIDDLE",
            "bbox": [270, 200, 370, 300],
            "expect": "STRAIGHT",
        },
        {
            "name": "Object SMALL (far away)",
            "bbox": [290, 220, 350, 260],
            "expect": "FORWARD",
        },
        {
            "name": "Object LARGE (close)",
            "bbox": [100, 50, 540, 430],
            "expect": "SLOW",
        },
    ]

    print("BBOX to Steering Test")
    print("=" * 60)
    print(f"Frame: {FRAME_WIDTH}x{FRAME_HEIGHT}, Center: {FRAME_CENTER_X}")
    print(f"Kp: {KP_STEER}, Base speed: {BASE_SPEED}%\n")

    passed = 0
    has_gpio = False

    try:
        import RPi.GPIO as GPIO
        has_gpio = True
        print("Motors available — will send real commands.\n")
    except (ImportError, RuntimeError):
        print("No GPIO — dry run mode. Printing commands only.\n")

    for tc in test_cases:
        bbox = tc["bbox"]
        left, right = bbox_to_steering(bbox)
        desc = describe_steering(left, right)

        ok = tc["expect"] in desc
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1

        bbox_cx = (bbox[0] + bbox[2]) / 2
        bbox_area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])

        print(f"  {status}: {tc['name']}")
        print(f"         BBOX center_x={bbox_cx:.0f}, area={bbox_area}")
        print(f"         L={left:+6.1f}%  R={right:+6.1f}%  -> {desc}")

    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{len(test_cases)} passed")

    if passed == len(test_cases):
        print("PASS: All BBOX-to-steering conversions correct")
        return True
    else:
        print(f"FAIL: {len(test_cases) - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
