---
title: Pi Rover — Vision-Guided Differential-Steer Rover
description: Raspberry Pi 3 rover with voice-commanded navigation, 4 DC motors via dual L298N H-bridges, camera streaming to Azure for Nvidia Locate Anything inference, and ultrasonic proximity safety stop
ms.date: 2026-05-30
---

## Overview

A voice-commanded 4-wheel differential-steer rover built on a Raspberry Pi 3. The user issues a wake word ("Hey [name]") followed by a command like "Drive to the [object]." The rover extracts the target object name, streams camera frames with that query to Azure running Nvidia Locate Anything, receives bounding-box positions back, and computes motor commands to drive toward the target. An HC-SR04 ultrasonic sensor acts as a safety override, triggering a hard stop when obstacles are too close.

## Signal Flow

```text
Microphone ──► wake word (local) ──► speech-to-text ──► extract object name
                                                              │
                                                              ▼
Camera (input) ──► Pi ──► Azure (Locate Anything + object query) ──► bbox
                    │                                                   │
                    ▼                                                   ▼
                    Pi ──────────► compute heading/speed ──► 4 DC motors (via 2× L298N)
                    ▲
                    │
HC-SR04 (input) ──► safety override (hard stop when too close)
```

## Hardware

| Component               | Qty | Role                                   |
|-------------------------|-----|----------------------------------------|
| Raspberry Pi 3          | 1   | Main controller                        |
| DC geared motor         | 4   | Wheel drive (from chassis kit)         |
| L298N motor driver      | 2   | H-bridge, 2 channels each (4 motors)  |
| Pi Camera / USB webcam  | 1   | Vision input                           |
| HC-SR04 ultrasonic      | 1   | Proximity / obstacle avoidance         |
| USB microphone          | 1   | Voice command input                    |
| 1kΩ + 2kΩ resistors    | 1 each | Voltage divider for HC-SR04 Echo    |
| USB power bank (5V 3A)  | 1   | Pi logic supply                        |
| 4×AA battery holder     | 1   | Motor supply (6V)                      |
| AA batteries            | 4   | For motor battery holder               |

## Software Stack

| Layer          | Technology                          |
|----------------|-------------------------------------|
| Robot framework | ROS2 (Humble or Iron)              |
| Language       | Python                              |
| Motor control  | `RPi.GPIO` PWM (direct GPIO to dual L298N)   |
| Camera         | `picamera2` or OpenCV               |
| Cloud inference | Azure compute + Nvidia Locate Anything |
| Wake word      | Local on-device (e.g. `openwakeword`, `porcupine`) |
| Speech-to-text | TBD (local vs cloud)                |
| Proximity      | `gpiozero` / `RPi.GPIO`            |

## Steering Model

Differential (skid) steering with 4 DC motors via 2× L298N H-bridges:

* **Forward**: all 4 motors same speed, same direction (IN1=HIGH, IN2=LOW per motor)
* **Turn left**: right motors faster than left (or left reversed)
* **Turn right**: left motors faster than left (or right reversed)
* **Spin in place**: left side forward, right side reverse (or vice versa)
* **Speed control**: PWM on ENA/ENB pins (0–100% duty cycle)
* **GPIO usage**: 12 pins total (3 per motor × 4 motors)

## Project Structure

```text
pi-rover/
├── config/            # ROS2 launch files, parameters
├── src/
│   ├── motor_control/ # L298N driver + differential steering node
│   ├── vision/        # Camera capture + Azure inference client
│   ├── voice/         # Wake word detection + speech-to-text + command parsing
│   ├── proximity/     # HC-SR04 ultrasonic sensor node (safety override)
│   └── navigator/     # High-level target tracking + obstacle avoidance
├── wiring/            # Pinout diagrams, wiring notes
└── README.md
```

## Open Questions

* Camera resolution / frame rate vs network bandwidth to Azure
* Latency budget: camera → Azure inference → motor command round-trip
* ROS2 on Pi 3 resource constraints (consider offloading heavy nodes)
* Wake word engine choice: `openwakeword` (open source) vs `porcupine` (Picovoice, commercial)
* Speech-to-text: local (Whisper.cpp on Pi 3?) vs cloud (Azure Speech) — latency vs reliability tradeoff
* Wake word / rover name selection
* Command grammar: how complex? Just "drive to {object}" or also "stop", "come back", "turn around"?
