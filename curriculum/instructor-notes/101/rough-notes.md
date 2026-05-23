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

