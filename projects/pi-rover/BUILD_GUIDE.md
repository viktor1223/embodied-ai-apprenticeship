---
title: Pi Rover Build Guide
description: Step-by-step hardware assembly, wiring, and integration testing from first frame to full pipeline
ms.date: 2026-05-30
ms.topic: tutorial
author: Viktor Ciroski
---

# Pi Rover Build Guide

This guide walks you through assembling and testing the rover one layer at a time.
Every section ends with a concrete pass/fail test. Do not move forward until the
current brick passes. Each test script lives in `tests/` and runs standalone.

## Prerequisites

Before you begin, confirm you have:

- Raspberry Pi (with Raspberry Pi OS installed, SSH enabled)
- Arducam IMX708 Camera Module 3 with 15-to-22pin FFC adapter cable
- USB microphone
- 2x L298N H-bridge modules
- 4x DC motors (from XiaoR Geek chassis kit or equivalent)
- HC-SR04 ultrasonic sensor
- 1kOhm and 2kOhm resistors (voltage divider for HC-SR04 Echo)
- USB power bank (5V 3A, for Pi logic)
- 4xAA battery holder with batteries (6V, for motors)
- Jumper wires, chassis, and mounting hardware
- An Azure subscription with access to Nvidia Locate Anything

Install Python dependencies on the Pi:

```bash
sudo apt update
sudo apt install -y python3-opencv python3-pip libportaudio2
pip3 install openwakeword azure-cognitiveservices-speech requests numpy
```

## Architecture Overview

The system has four layers, tested bottom-up:

```text
LAYER 4: INTEGRATION
  Voice command triggers full visual servo pipeline

LAYER 3: ACTUATION
  DC motors via L298N, proximity sensor safety stop

LAYER 2: CLOUD
  Azure Locate Anything inference, Speech-to-Text

LAYER 1: PERCEPTION
  Camera capture, microphone capture, wake word detection
```

Refer to `wiring/pinout-and-wiring.md` for all GPIO assignments and
`wiring/safety-and-power.md` for power distribution before connecting anything.

---

## Layer 1: Perception

### Brick 1: Camera Capture (Single Frame)

Connect the Arducam IMX708 to the Pi's CSI port using the 15-to-22pin FFC adapter.
The ribbon cable's blue side faces the Ethernet/USB ports on the Pi.

After connecting:

```bash
# Verify the camera is detected
libcamera-hello --list-cameras
```

You should see the IMX708 listed. If you see "no cameras available," reseat the
ribbon cable and check the adapter orientation.

Run the test:

```bash
cd ~/pi-rover/tests
python3 brick01_camera_capture.py
```

Pass condition: a file `test_frame.jpg` appears and you can open it.
The terminal prints resolution and file size.

### Brick 2: Camera Live Feed

Same hardware as Brick 1. This streams live video to a window.

```bash
python3 brick02_camera_live.py
```

Pass condition: a window opens showing live video from the camera. Press `q` to quit.
If you are running headless over SSH, use X11 forwarding (`ssh -X pi@<ip>`) or
skip to Brick 6 where you send frames to Azure instead of displaying them locally.

### Brick 3: Microphone Capture

Plug the USB microphone into one of the Pi's USB ports (USB2 is free if the mic is
on USB1 per the diagram).

```bash
# Verify the mic is detected
arecord -l
```

You should see a USB Audio device listed. Then:

```bash
python3 brick03_mic_capture.py
```

Pass condition: speaks into the mic for 3 seconds, a file `test_audio.wav` appears,
and you can play it back. The terminal prints sample rate and duration.

### Brick 4: Wake Word Detection

Same hardware as Brick 3. This listens continuously for the wake phrase.

```bash
python3 brick04_wake_word.py
```

Pass condition: say "Hey Rover" and the terminal prints `WAKE WORD DETECTED`.
Say "stop" and the terminal prints `STOP COMMAND`. Press Ctrl+C to exit.

---

## Layer 2: Cloud

### Brick 5: Azure Endpoint Setup

No hardware needed. This brick provisions the Azure resources. You need:

1. An Azure subscription
2. Azure CLI installed (`az login`)
3. A deployed Nvidia Locate Anything endpoint

If you do not have the endpoint yet, follow these steps:

```bash
# Login to Azure
az login

# Create a resource group (if you do not have one)
az group create --name pi-rover-rg --location eastus

# Deploy the model endpoint (details depend on your Azure AI setup)
# See Azure documentation for Nvidia Locate Anything deployment
```

Run the verification script:

```bash
python3 brick05_azure_setup.py
```

Pass condition: the script connects to your Azure endpoint and prints
`ENDPOINT REACHABLE` with the model name and API version.

Before running, create a `.env` file in the `tests/` directory:

```text
AZURE_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com
AZURE_API_KEY=your-api-key
AZURE_SPEECH_KEY=your-speech-key
AZURE_SPEECH_REGION=eastus
```

Never commit this file. It is already in `.gitignore`.

### Brick 6: Image to Azure (Locate Anything)

Requires: Brick 1 passing (camera works) and Brick 5 passing (endpoint reachable).

```bash
python3 brick06_image_to_azure.py --target "cup"
```

Pass condition: the script captures a frame, sends it to Locate Anything with the
text prompt "cup," and prints the returned bounding box coordinates.
Place an actual cup in front of the camera for a real test.

Expected output format:

```text
Target: cup
BBOX: [x_min, y_min, x_max, y_max]
Confidence: 0.87
Latency: 342ms
```

### Brick 7: Audio to Azure (Speech-to-Text)

Requires: Brick 3 passing (mic works) and Brick 5 passing (endpoint reachable).

```bash
python3 brick07_audio_to_azure.py
```

Pass condition: speak a sentence into the mic, and the terminal prints the
transcribed text from Azure Speech-to-Text.

### Brick 8: Command Parsing

No hardware needed. This tests the text-to-command parser.

```bash
python3 brick08_command_parse.py
```

Pass condition: runs a set of test phrases and prints parsed results:

```text
"drive to the cup"       -> Command(action=DRIVE, target=cup)
"go to the red ball"     -> Command(action=DRIVE, target=red ball)
"stop"                   -> Command(action=STOP, target=None)
"hey rover find the cat" -> Command(action=DRIVE, target=cat)
```

---

## Layer 3: Actuation

### Safety First

Before connecting any motors:

1. Read `wiring/safety-and-power.md` completely
2. Use the 4xAA battery pack for motor power, USB power bank for Pi logic
3. Connect grounds between Pi and L298N BEFORE connecting motor power
4. Keep the battery pack disconnected until you are ready to test
5. Never connect motor power (6V) to Pi GPIO pins

### Brick 9: Single Motor Spin

Connect ONE motor to L298N_L Channel A only. Follow the pin assignments in
`wiring/pinout-and-wiring.md`:

- GPIO5 -> IN1
- GPIO6 -> IN2
- GPIO12 -> ENA (PWM speed)

Connect motor to OUT1/OUT2. Connect 4xAA battery to L298N 12V/GND.
Connect Pi GND to L298N GND.

```bash
python3 brick09_single_motor.py
```

Pass condition: the motor spins forward for 2 seconds, stops for 1 second,
spins backward for 2 seconds, then stops. The terminal prints direction and speed.

### Brick 10: All Four Motors

Wire all four motors per the full pinout. Both L298N modules connected.

```bash
python3 brick10_all_motors.py
```

Pass condition: each motor spins individually in sequence (FL, RL, FR, RR) with
its name printed. You verify each physical motor matches its label.

### Brick 11: Steering Patterns

Same hardware as Brick 10.

```bash
python3 brick11_steering.py
```

Pass condition: the rover executes a sequence:
forward (2s) -> stop (1s) -> backward (2s) -> stop (1s) ->
turn left (2s) -> stop (1s) -> turn right (2s) -> stop.
You verify the chassis moves in the expected directions.

### Brick 12: Proximity Reading

Wire the HC-SR04 per pinout (GPIO17 = TRIG, GPIO27 = ECHO through voltage divider).

```bash
python3 brick12_proximity.py
```

Pass condition: the terminal prints distance readings in cm, updating every 200ms.
Move your hand toward the sensor and verify the readings decrease. Readings should
be stable (within +/- 1cm) at a fixed distance.

---

## Layer 4: Integration

### Brick 13: BBOX to Steering (Mock)

No camera or cloud needed. This feeds mock BBOX values to the steering controller
and verifies the proportional response.

```bash
python3 brick13_bbox_steering.py
```

Pass condition: prints the expected motor commands for mock BBOX positions:

```text
BBOX center at frame LEFT  -> steer LEFT  (right motors faster)
BBOX center at frame RIGHT -> steer RIGHT (left motors faster)
BBOX center at MIDDLE      -> drive STRAIGHT
BBOX is SMALL (far away)   -> drive FORWARD at moderate speed
BBOX is LARGE (close)      -> drive FORWARD at slow speed
```

If motors are connected, you will see the rover respond physically. Otherwise
the test runs in dry-run mode and just prints the motor commands.

### Brick 14: Proximity Emergency Stop

Requires: Brick 11 passing (motors work) and Brick 12 passing (sensor works).

```bash
python3 brick14_proximity_stop.py
```

Pass condition: the rover drives forward slowly. Place your hand in front of the
HC-SR04 sensor. When distance drops below 20cm, the rover stops immediately.
The terminal prints `EMERGENCY STOP: obstacle at Xcm`. Remove your hand, and
the rover resumes after 2 seconds.

### Brick 15: Visual Servo Loop

Requires: Bricks 1, 6, 11, 12 all passing.

```bash
python3 brick15_visual_servo.py --target "cup"
```

Pass condition: the rover turns toward the cup (camera -> Azure -> BBOX -> steer)
in a continuous loop. It approaches the cup and stops when the proximity sensor
reads below the threshold. The terminal prints each cycle with latency,
BBOX position, and motor commands.

This is the first time the full perception-to-actuation loop runs.

### Brick 16: Voice-Triggered Full Pipeline

Requires: all previous bricks passing.

```bash
python3 brick16_voice_pipeline.py
```

Pass condition: say "Hey Rover, drive to the cup." The rover wakes, identifies the
target object, turns toward it, drives to it, and stops at a safe distance.
Say "stop" at any point and the rover halts immediately.

---

## Troubleshooting

### Camera not detected

Reseat the FFC ribbon cable. Blue side faces the Ethernet/USB ports. Run
`libcamera-hello --list-cameras` to verify. If using Pi 5, check that you have the
correct 22-pin cable (no adapter needed on Pi 5).

### Motor spins wrong direction

Swap the two wires on the motor terminals (OUT1/OUT2 or OUT3/OUT4). The software
direction will then match physical direction. Alternatively, swap IN1/IN2 in the
pin config.

### HC-SR04 reads 0 or garbage values

Check the voltage divider. Measure with a multimeter: the junction between the 1kOhm
and 2kOhm resistors should read about 3.3V when Echo is HIGH (not 5V). If you see
5V, the divider is wired incorrectly or bypassed.

### Azure returns errors

Verify your `.env` file has the correct endpoint URL and key. Run Brick 5 first.
Check that your Azure subscription has quota for the Locate Anything model.

### High latency from Azure

Expected round-trip for Locate Anything is 200-500ms. If you see >1s, check your
network connection. Consider using a wired Ethernet connection instead of Wi-Fi.
The visual servo loop in Brick 15 is designed to hold the last steering command
while waiting for the next inference result.
