"""Brick 1: Camera Capture — grab a single frame and save to file.

Pass condition: test_frame.jpg exists, terminal prints resolution and file size.
Hardware: Pi + Arducam IMX708 via CSI ribbon cable.
"""

import sys
import os

def main():
    try:
        from picamera2 import Picamera2
    except ImportError:
        print("picamera2 not available — falling back to OpenCV webcam capture")
        return capture_opencv()

    return capture_picamera()


def capture_picamera():
    """Capture using the Pi CSI camera via picamera2."""
    from picamera2 import Picamera2

    cam = Picamera2()
    config = cam.create_still_configuration(main={"size": (1920, 1080)})
    cam.configure(config)
    cam.start()

    import time
    time.sleep(2)  # let the auto-exposure settle

    output_path = "test_frame.jpg"
    cam.capture_file(output_path)
    cam.stop()

    file_size = os.path.getsize(output_path)
    print(f"PASS: Frame saved to {output_path}")
    print(f"  Resolution: 1920x1080")
    print(f"  File size:  {file_size / 1024:.1f} KB")
    return True


def capture_opencv():
    """Fallback capture using OpenCV (works with USB webcam on Mac/PC)."""
    import cv2

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("FAIL: No camera found")
        return False

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        print("FAIL: Could not capture frame")
        return False

    output_path = "test_frame.jpg"
    cv2.imwrite(output_path, frame)

    h, w = frame.shape[:2]
    file_size = os.path.getsize(output_path)
    print(f"PASS: Frame saved to {output_path}")
    print(f"  Resolution: {w}x{h}")
    print(f"  File size:  {file_size / 1024:.1f} KB")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
