---
title: Pi Rover Safety and Power Design
description: Power distribution, safety constraints, and pre-flight checklist for the Pi 3 rover
ms.date: 2026-05-30
---

## Power Architecture

The rover uses two separate power supplies to isolate logic from motors. Servo stall current and startup surges can cause voltage drops that reset the Pi or corrupt the SD card.

```text
┌─────────────────┐     ┌─────────────────┐
│  Logic Supply    │     │  Motor Supply    │
│  (USB power bank │     │  (4×AA battery   │
│   5V 3A)         │     │   holder, 6V)    │
│                  │     │                  │
│  Pi 3 micro-USB  │     │  L298N_L 12V in  │
│  HC-SR04 VCC     │     │  L298N_R 12V in  │
│                  │     │                  │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         └──── Common GND ────────┘
```

### Why Separate Supplies

| Risk | What happens | Prevention |
|------|-------------|------------|
| Motor stall draws 4A+ | Voltage drops below 4.75V | Motor battery isolated from Pi |
| Motor startup surge | Pi brownout, SD card corruption | Separate rail absorbs surge |
| Backfeed through GPIO | Damaged Pi 3.3V regulator | Voltage divider on HC-SR04 Echo |
| Shared ground loop | Erratic sensor readings | Single common ground point |

### Power Budget Estimate

| Component | Voltage | Typical draw | Peak draw |
|-----------|---------|-------------|-----------|
| Raspberry Pi 3 | 5V | 700mA | 2.5A (with camera + USB) |
| HC-SR04 | 5V | 15mA | 15mA |
| USB microphone | 5V | 100mA | 200mA |
| **Logic total** | | **~815mA** | **~2.7A** |
| 2× L298N quiescent | 6V | 30mA each (60mA) | 60mA |
| 4× DC motors | 6V | 200mA each (800mA) | 1A each (4A) |
| **Motor total** | | **~860mA** | **~4A** |

### Supply Recommendations

| Rail | Minimum spec | Recommended |
|------|-------------|-------------|
| Logic | 5V 3A USB power bank | 5V 3A with stable output under load |
| Motor | 6V 4A | 4×AA NiMH (4.8V) or 4×AA alkaline (6V) in holder |

## Safety Rules

### Electrical Safety

1. **Never connect HC-SR04 Echo directly to GPIO.** Always use the voltage divider (1kΩ + 2kΩ). A 5V signal on a 3.3V GPIO will damage the Pi's SoC permanently.

2. **Never power motors from the Pi's 5V pins.** The Pi's onboard regulator cannot supply more than ~300mA on the 5V header. Four motors will exceed this instantly. Motors go through the L298N, powered by a separate battery.

3. **Connect grounds together.** The Pi GND, L298N GND (both), HC-SR04 GND, and motor battery negative must share a common ground. Without this, signals have no reference and nothing works.

4. **Double-check polarity before powering on.** Reversed power on the L298N or HC-SR04 will destroy them.

5. **Do not feed 5V into L298N's 5V pin.** The L298N has an onboard 5V regulator that outputs on this pin. If you connect the Pi's 5V here, you create a conflict between two regulators.

### Software Safety

1. **Proximity override is non-negotiable.** The HC-SR04 safety stop must run as a local, high-priority check. If distance < threshold, all motor commands are zeroed regardless of navigator state.

2. **Watchdog timeout on motor commands.** If the navigator node dies or stops publishing, motors should stop within 500ms. Never leave motors running without a heartbeat.

3. **Startup state is stopped.** On boot, all servos must initialize to zero speed. The rover should never move without an explicit command.

4. **Wake word "stop" is local-only.** The stop command must never depend on network connectivity. It follows the same principle as the proximity override: safety-critical inputs are always local.

### Operational Safety

1. **Prop the rover up for first tests.** Lift the wheels off the ground while testing motor directions and speed. Verify left/right spin directions match expectations before ground tests.

2. **Test HC-SR04 standalone first.** Before integrating with motor control, verify the sensor reads correct distances and the voltage divider output is under 3.4V with a multimeter.

3. **Test voice commands without motors.** Verify wake word detection and command parsing produce correct ROS2 messages before enabling motor output.

## Pre-Flight Checklist

Run through this before every powered test:

* [ ] Logic and motor power supplies are separate
* [ ] Common ground wire connected between supplies
* [ ] HC-SR04 Echo pin goes through voltage divider, NOT direct to GPIO
* [ ] Verify divider output with multimeter: should read ~3.3V when Echo is HIGH
* [ ] L298N_L responds to GPIO: IN1 HIGH makes motor FL spin
* [ ] L298N_R responds to GPIO: IN1 HIGH makes motor FR spin
* [ ] Camera detected: `vcgencmd get_camera` or `libcamera-hello`
* [ ] USB mic detected: `arecord -l`
* [ ] Wheels elevated off ground for initial motor test
* [ ] Proximity override node is running before navigator starts
* [ ] All motors initialize to zero speed on startup (ENA/ENB PWM = 0)
