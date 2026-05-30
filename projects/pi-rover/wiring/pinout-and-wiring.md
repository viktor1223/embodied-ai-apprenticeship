---
title: Pi Rover Wiring and Pinout Reference
description: Complete wiring diagram, pin assignments, and connection details for the Pi 3 rover
ms.date: 2026-05-30
---

## Pi 3 GPIO Header Reference

```text
                    3V3  (1)  (2)  5V
          I2C SDA  GPIO2 (3)  (4)  5V
          I2C SCL  GPIO3 (5)  (6)  GND
                   GPIO4 (7)  (8)  GPIO14
                     GND (9)  (10) GPIO15
                  GPIO17 (11) (12) GPIO18
                  GPIO27 (13) (14) GND
                  GPIO22 (15) (16) GPIO23
                    3V3  (17) (18) GPIO24
                  GPIO10 (19) (20) GND
                   GPIO9 (21) (22) GPIO25
                  GPIO11 (23) (24) GPIO8
                     GND (25) (26) GPIO7
                   GPIO0 (27) (28) GPIO1
                   GPIO5 (29) (30) GND
                   GPIO6 (31) (32) GPIO12
                  GPIO13 (33) (34) GND
                  GPIO19 (35) (36) GPIO16
                  GPIO26 (37) (38) GPIO20
                     GND (39) (40) GPIO21
```

## Pin Assignments

| Component | Function | Pi Pin | GPIO | Notes |
|-----------|----------|--------|------|-------|
| L298N_L | ENA (FL speed) | 32 | GPIO12 | PWM for front-left motor |
| L298N_L | IN1 (FL dir) | 29 | GPIO5 | Front-left direction A |
| L298N_L | IN2 (FL dir) | 31 | GPIO6 | Front-left direction B |
| L298N_L | ENB (RL speed) | 33 | GPIO13 | PWM for rear-left motor |
| L298N_L | IN3 (RL dir) | 35 | GPIO19 | Rear-left direction A |
| L298N_L | IN4 (RL dir) | 37 | GPIO26 | Rear-left direction B |
| L298N_R | ENA (FR speed) | 36 | GPIO16 | PWM for front-right motor |
| L298N_R | IN1 (FR dir) | 38 | GPIO20 | Front-right direction A |
| L298N_R | IN2 (FR dir) | 40 | GPIO21 | Front-right direction B |
| L298N_R | ENB (RR speed) | 22 | GPIO25 | PWM for rear-right motor |
| L298N_R | IN3 (RR dir) | 24 | GPIO8 | Rear-right direction A |
| L298N_R | IN4 (RR dir) | 26 | GPIO7 | Rear-right direction B |
| HC-SR04 | Trig | 11 | GPIO17 | 3.3V output, safe for sensor |
| HC-SR04 | Echo | 13 | GPIO27 | Via voltage divider (see below) |
| HC-SR04 | VCC | 4 | 5V | Sensor requires 5V supply |
| HC-SR04 | GND | 14 | GND | Common ground |
| Camera | CSI ribbon | CSI port | N/A | Dedicated camera connector, no GPIO |
| USB mic | USB | USB port | N/A | Any USB port, no GPIO |

**Total GPIO pins used: 14** (12 for motors, 2 for HC-SR04)

## Wiring Diagram

```text
                              ┌──────────────────────┐
  ┌─────────┐                 │    Raspberry Pi 3     │                 ┌─────────┐
  │ L298N_L │  6 GPIO wires   │                       │  6 GPIO wires   │ L298N_R │
  │ (left)  │◄────────────────│  GPIO5,6,12 (Ch A)    │────────────────►│ (right) │
  │         │                 │  GPIO19,26,13 (Ch B)  │                 │         │
  │         │                 │                       │                 │         │
  │ OUT1,2 ─┤── Motor FL      │  GPIO20,21,16 (Ch A)  │                 ├─ OUT1,2 │── Motor FR
  │ OUT3,4 ─┤── Motor RL      │  GPIO8,7,25 (Ch B)    │                 ├─ OUT3,4 │── Motor RR
  │         │                 │                       │                 │         │
  │ 12V ◄───┤── Motor         │                       │       Motor ───►├── 12V   │
  │ GND ◄───┤── Battery       │                       │       Battery──►├── GND   │
  └─────────┘                 │                       │                 └─────────┘
                              │                       │
  ┌─────────┐                 │                       │
  │ HC-SR04 │                 │                       │
  │         │                 │                       │
  │ VCC ◄───┤── 5V (Pin 4)   │                       │
  │ GND ◄───┤── GND (Pin 14) │                       │
  │ Trig◄───┤── GPIO17       │                       │
  │ Echo───►├── R1 (1kΩ) ──┬──► GPIO27 (Pin 13)      │
  │         │              R2 (2kΩ)                   │
  │         │              │                          │
  └─────────┘             GND                         │
                              │                       │
                              │  CSI ◄── Pi Camera    │
                              │  USB ◄── Microphone   │
                              └──────────────────────┘
```

## HC-SR04 Voltage Divider Detail

The Echo pin outputs 5V, but Pi GPIO is 3.3V tolerant only. A resistor voltage divider steps the voltage down.

```text
HC-SR04 Echo (5V) ───── R1 (1kΩ) ───┬──► GPIO27 (reads ~3.3V)
                                     │
                                   R2 (2kΩ)
                                     │
                                    GND
```

$$V_{out} = V_{in} \times \frac{R2}{R1 + R2} = 5V \times \frac{2000}{3000} \approx 3.3V$$

**Trig pin** does not need a divider: the Pi sends a 3.3V pulse out, and the HC-SR04 accepts anything above 2V as HIGH.

## L298N Motor Driver Connections

Each L298N has 2 H-bridge channels (A and B). Each channel drives one DC motor with 3 control signals from the Pi:

| Signal | Function | How it works |
|--------|----------|-------------|
| EN (ENA/ENB) | Speed | PWM duty cycle 0–100% controls motor speed |
| IN1/IN3 | Direction A | HIGH = current flows one way |
| IN2/IN4 | Direction B | HIGH = current flows other way |

### Direction Truth Table

| IN1 | IN2 | Motor action |
|-----|-----|-------------|
| HIGH | LOW | Forward |
| LOW | HIGH | Reverse |
| LOW | LOW | Coast (free spin) |
| HIGH | HIGH | Brake (locked) |

### Motor-to-Driver Mapping

| L298N | Channel | Motor | EN pin | IN pins |
|-------|---------|-------|--------|---------|
| L298N_L | A | Front-Left | GPIO12 | GPIO5, GPIO6 |
| L298N_L | B | Rear-Left | GPIO13 | GPIO19, GPIO26 |
| L298N_R | A | Front-Right | GPIO16 | GPIO20, GPIO21 |
| L298N_R | B | Rear-Right | GPIO25 | GPIO8, GPIO7 |

### Power Connections

Each L298N needs:

| Terminal | Connect to | Notes |
|----------|-----------|-------|
| 12V (motor supply) | Motor battery pack + | 6V–7.4V (name is misleading, accepts 5–35V) |
| GND | Motor battery – AND Pi GND | Common ground required |
| 5V | Leave unconnected | L298N's onboard regulator outputs 5V; do NOT feed Pi 5V into this |
| OUT1, OUT2 | Motor A terminals | Polarity determines "forward" direction |
| OUT3, OUT4 | Motor B terminals | Polarity determines "forward" direction |
