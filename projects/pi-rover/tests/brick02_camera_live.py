"""Brick 2: Camera Live Feed — stream video to a display window.

Pass condition: a window opens showing live video. Press 'q' to quit.
Hardware: Pi + Arducam IMX708 via CSI ribbon cable.
For headless SSH, use: ssh -X pi@<ip>
"""

import sys


def main():
    try:
        from picamera2 import Picamera2
        return stream_picamera()
    except ImportError:
        print("picamera2 not available — falling back to OpenCV webcam")
        return stream_opencv()


def stream_picamera():
    """Stream via picamera2 + OpenCV display."""
    from picamera2 import Picamera2
    import cv2
    import time

    cam = Picamera2()
    config = cam.create_preview_configuration(main={"size": (640, 480)})
    cam.configure(config)
    cam.start()
    time.sleep(1)

    print("Live feed active. Press 'q' in the window to quit.")
    frame_count = 0
    start = time.time()

    while True:
        frame = cam.capture_array()
        # picamera2 returns RGB; OpenCV expects BGR
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_count += 1
        elapsed = time.time() - start
        fps = frame_count / elapsed if elapsed > 0 else 0

        cv2.putText(frame_bgr, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Brick 2: Camera Live Feed", frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.stop()
    cv2.destroyAllWindows()
    print(f"PASS: Streamed {frame_count} frames at {fps:.1f} FPS")
    return True


def stream_opencv():
    """Stream via OpenCV webcam (Mac/PC fallback)."""
    import cv2
    import time

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("FAIL: No camera found")
        return False

    print("Live feed active. Press 'q' in the window to quit.")
    frame_count = 0
    start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("FAIL: Lost camera feed")
            break

        frame_count += 1
        elapsed = time.time() - start
        fps = frame_count / elapsed if elapsed > 0 else 0

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Brick 2: Camera Live Feed", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"PASS: Streamed {frame_count} frames at {fps:.1f} FPS")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
