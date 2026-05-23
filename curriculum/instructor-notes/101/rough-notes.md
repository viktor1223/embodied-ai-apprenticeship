# 101 Rough Notes

## Step 1: Setting Up Wokwi in VS Code

- First thing we do before any hardware — get the simulator running
- Wokwi = hardware simulator inside VS Code (Arduino, ESP32, visual wiring, LEDs, motors, sensors)
- Why start here: fast iteration, no wiring mistakes, no burned parts, instant feedback
- Test logic before committing to real hardware
- Setup steps:
  1. Install Wokwi for VS Code extension
  2. Get free license (prompt on first use)
  3. `wokwi.toml` in project root → tells simulator which firmware to load
  4. `diagram.json` → defines virtual circuit (board, components, wires)
  5. Command palette: `Wokwi: Start Simulator`
- How it fits together:
  - PlatformIO compiles code → firmware (`.bin` / `.elf`)
  - `wokwi.toml` points simulator at firmware
  - `diagram.json` describes virtual breadboard
  - Simulator runs compiled code against virtual circuit in real time
  - Serial Monitor shows up in VS Code terminal
- Demo: build blink → run in Wokwi → see LED blink → change delay → rebuild → faster blink
- Workflow loop: edit code → compile → simulate → observe

---

## Key Reference: Arduino Pin Types

This table surfaced during Lab 2 and is foundational for all wiring:

| Pin type | Direction | What it does |
|----------|-----------|-------------|
| A0–A5 (analog) | **Input** — reads from the world | Converts voltage → number (ADC) |
| PWM pins (3,5,6,9,10,11) | **Output** — writes to the world | Sends pulsed signal to control things |
| Digital pins (2–13) | **Input or Output** | Read HIGH/LOW or write HIGH/LOW |
| 5V / 3.3V | Power out | Constant voltage supply |
| GND | Ground | Common return path |

**Common misconceptions that surfaced:**
- VCC on a component = power input, not signal output
- PWM pins cannot read analog values — they only write
- Multiple components can share 5V and GND (like a power strip)
- Standard servos = 0–180° position; DC motors = continuous rotation

