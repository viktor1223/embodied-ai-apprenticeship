"""Brick 3: Microphone Capture — record 3 seconds of audio and save to file.

Pass condition: test_audio.wav exists and is playable. Terminal prints sample rate
and duration.
Hardware: USB microphone plugged into Pi USB port.
"""

import sys
import os
import wave
import struct
import time


DURATION = 3       # seconds
SAMPLE_RATE = 16000
CHANNELS = 1
OUTPUT_FILE = "test_audio.wav"


def main():
    try:
        import pyaudio
    except ImportError:
        print("pyaudio not installed. Install with:")
        print("  sudo apt install libportaudio2")
        print("  pip3 install pyaudio")
        return False

    return record_audio()


def record_audio():
    import pyaudio

    pa = pyaudio.PyAudio()

    # Find the USB mic
    mic_index = None
    print("Available audio devices:")
    for i in range(pa.get_device_count()):
        info = pa.get_device_info_by_index(i)
        if info["maxInputChannels"] > 0:
            print(f"  [{i}] {info['name']} (inputs: {info['maxInputChannels']})")
            if mic_index is None:
                mic_index = i

    if mic_index is None:
        print("FAIL: No input device found")
        pa.terminate()
        return False

    print(f"\nUsing device [{mic_index}]")
    print(f"Recording {DURATION}s at {SAMPLE_RATE} Hz...")

    stream = pa.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        input_device_index=mic_index,
        frames_per_buffer=1024,
    )

    frames = []
    for _ in range(0, int(SAMPLE_RATE / 1024 * DURATION)):
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    pa.terminate()

    # Write WAV file
    wf = wave.open(OUTPUT_FILE, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(2)  # 16-bit = 2 bytes
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    file_size = os.path.getsize(OUTPUT_FILE)
    actual_duration = len(frames) * 1024 / SAMPLE_RATE

    print(f"\nPASS: Audio saved to {OUTPUT_FILE}")
    print(f"  Sample rate: {SAMPLE_RATE} Hz")
    print(f"  Duration:    {actual_duration:.1f}s")
    print(f"  File size:   {file_size / 1024:.1f} KB")
    print(f"\nPlayback: aplay {OUTPUT_FILE}")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
