# Research Journal: Lab 2 — Servo Wiring Struggles

**Date:** 2026-05-23
**Context:** Lab 2, servo angle control with potentiometer

---

## The Task

Wire a potentiometer and servo to an Arduino so that turning the pot controls the servo angle.

## Attempt 1 — Same Mistakes as Lab 1

Repeated the Lab 1 error pattern:
- Connected pot VCC to pin 13 (thinking it was the signal path)
- Connected servo power to a digital pin (pin 7)
- Connected Arduino GND to servo PWM (misread the servo pinout)

**Root cause:** Still thinking of pins by position/number rather than by *function*.

## Attempt 2 — Partial Fix

Fixed the servo pinout (PWM, V+, GND in correct positions). But:
- Connected pot SIG to pin 11 (a PWM output pin)
- Connected pot VCC to 3.3V

**What was wrong:** Confused PWM output pins with analog input pins. Pin 11 *sends* signals; it can't *read* voltages. The pot needs to be read by an ADC pin (A0–A5).

## Attempt 3 — Got It

Final wiring:
- pot SIG → A0 (analog input reads the pot)
- pot VCC → 5V (constant power)
- servo PWM → pin 7 (signal output)
- Everything else: power and ground where they belong

**Three attempts.** Each one exposed a different misconception.

---

## Key Mental Model Update: Pin Types Have Roles

| Pin type | Direction | What it does |
|----------|-----------|-------------|
| A0–A5 (analog) | **Input** — reads from the world | Converts voltage → number (ADC) |
| PWM pins (3,5,6,9,10,11) | **Output** — writes to the world | Sends pulsed signal to control things |
| Digital pins (2–13) | **Input or Output** | Read HIGH/LOW or write HIGH/LOW |
| 5V / 3.3V | Power out | Constant voltage supply |
| GND | Ground | Common return path |

This table didn't exist in my head before today. I was treating all pins as interchangeable.

---

## Other Insights

- **Multiple components can share 5V/GND** — it's like a power strip
- **Standard servos only do 0–180°** — for wheels you need DC motors (Lab 3)
- **Servo library can use any digital pin** (not just PWM pins) because it generates its own timing via software interrupts
- **Wokwi may not animate servo visually** even when serial output confirms correct values — same visual limitation as LED brightness

---

## Wrong Predictions That Drove Learning

1. "VCC is where the signal comes out" → No, VCC is power IN, SIG is signal OUT
2. "PWM pins can read analog values" → No, PWM = output only; A0–A5 = input only
3. "Servos can do 360°" → No, standard servos are 0–180° (position control)

Each wrong prediction updated the mental model. The code itself was trivial — three lines in a loop. The wiring is where the real understanding lives.
