"""Brick 7: Audio to Azure — record speech and send to Azure Speech-to-Text.

Pass condition: speak a sentence, terminal prints the transcribed text.
Hardware: USB microphone.
Requires: Bricks 3 and 5 passing. .env file with AZURE_SPEECH_KEY and
AZURE_SPEECH_REGION.
"""

import sys
import os


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


def main():
    if not load_env():
        return False

    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        print("Azure Speech SDK not installed. Run:")
        print("  pip3 install azure-cognitiveservices-speech")
        return False

    speech_key = os.environ.get("AZURE_SPEECH_KEY")
    speech_region = os.environ.get("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        print("FAIL: AZURE_SPEECH_KEY and AZURE_SPEECH_REGION must be set in .env")
        return False

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=speech_region,
    )
    speech_config.speech_recognition_language = "en-US"

    # Use the default microphone
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config,
    )

    print("Speak now (listening for one utterance)...")

    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"\nPASS: Speech recognized")
        print(f"  Text: \"{result.text}\"")
        return True
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print(f"FAIL: No speech recognized")
        print(f"  Detail: {result.no_match_details}")
        return False
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print(f"FAIL: Recognition canceled")
        print(f"  Reason: {cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"  Error:  {cancellation.error_details}")
        return False

    return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
