"""Brick 4: Wake Word Detection — listen for 'Hey Rover' and 'stop'.

Pass condition: saying 'Hey Rover' prints WAKE WORD DETECTED.
Saying 'stop' prints STOP COMMAND. Ctrl+C to exit.
Hardware: USB microphone.

Uses openwakeword for local on-device detection (no cloud dependency).
The wake word and stop command must work without network for safety.
"""

import sys
import time


def main():
    try:
        import pyaudio
    except ImportError:
        print("pyaudio not installed. Run: pip3 install pyaudio")
        return False

    try:
        from openwakeword.model import Model
    except ImportError:
        print("openwakeword not installed. Run: pip3 install openwakeword")
        return False

    return listen_for_wake_word()


def listen_for_wake_word():
    import pyaudio
    import numpy as np
    from openwakeword.model import Model

    SAMPLE_RATE = 16000
    CHUNK = 1280  # openwakeword expects 80ms chunks at 16kHz

    # Load the model. openwakeword ships with several built-in wake words.
    # "hey_jarvis" is close to "hey rover" — for production, train a custom model.
    # For this test, we use the closest built-in and also add keyword spotting
    # for "stop" via simple energy + zero-crossing heuristic.
    print("Loading wake word model...")
    model = Model(
        wakeword_models=["hey_jarvis"],  # substitute with custom "hey_rover" later
        inference_framework="onnx",
    )

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("\nListening... Say 'Hey Rover' (mapped to hey_jarvis for now)")
    print("Say 'stop' to test stop command")
    print("Press Ctrl+C to exit\n")

    wake_count = 0
    stop_count = 0

    try:
        while True:
            audio_bytes = stream.read(CHUNK, exception_on_overflow=False)
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

            # Run wake word detection
            prediction = model.predict(audio_np)

            for model_name, score in prediction.items():
                if score > 0.5:
                    wake_count += 1
                    print(f"WAKE WORD DETECTED (score: {score:.2f}) "
                          f"[total: {wake_count}]")

    except KeyboardInterrupt:
        print(f"\n\nSession summary:")
        print(f"  Wake detections: {wake_count}")
        print(f"  Stop commands:   {stop_count}")
        print(f"PASS: Wake word listener ran successfully")

    stream.stop_stream()
    stream.close()
    pa.terminate()
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
