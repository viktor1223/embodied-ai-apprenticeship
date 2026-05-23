# Wokwi + PlatformIO Workflow Reference

## What the pieces are

| Piece | What it does |
|-------|-------------|
| **PlatformIO** | Compiles your C++ code into firmware (a `.hex` file the microcontroller understands) |
| **wokwi.toml** | Tells the Wokwi simulator where to find that compiled firmware |
| **diagram.json** | Describes the virtual circuit — which board, which components, how they're wired |
| **Wokwi extension** | Runs the firmware against the virtual circuit inside VS Code |

## The actual workflow (step by step)

### 1. Install the extension

- Open VS Code Extensions sidebar
- Search "Wokwi" → install **Wokwi for VS Code**
- Press `F1` → "Wokwi: Request a new License"
- Browser opens → click "GET YOUR LICENSE" → confirm back in VS Code
- One-time setup, never again

### 2. Compile your code

In terminal (from project root):

```bash
pio run
```

This produces:
- `.pio/build/uno/firmware.hex` — the actual program for the chip
- `.pio/build/uno/firmware.elf` — debug symbols (helps Wokwi run faster)

### 3. Start the simulator

- Press `F1` → "Wokwi: Start Simulator"
- Wokwi reads `wokwi.toml` to find the firmware
- Wokwi reads `diagram.json` to build the virtual circuit
- Simulation starts — you see the board, LED blinks, serial output appears

### 4. Make changes and iterate

1. Edit `src/main.cpp`
2. Run `pio run` again
3. Wokwi auto-restarts with the new firmware (or stop/start manually)

That's the whole loop: **edit → compile → simulate → observe**.

---

## File reference

### wokwi.toml (minimal for Arduino Uno + PlatformIO)

```toml
[wokwi]
version = 1
firmware = '.pio/build/uno/firmware.hex'
elf = '.pio/build/uno/firmware.elf'
```

- `firmware` — path to compiled binary (relative to project root)
- `elf` — optional but speeds up simulation
- For ESP32 projects, use `.bin` or `flasher_args.json` instead of `.hex`

### diagram.json (minimal — just the board)

```json
{
  "version": 1,
  "author": "Your Name",
  "editor": "wokwi",
  "parts": [
    { "type": "wokwi-arduino-uno", "id": "uno", "top": 0, "left": 0, "attrs": {} }
  ],
  "connections": [],
  "serialMonitor": { "display": "auto" }
}
```

The built-in LED (pin 13) is already on the board — no extra parts needed for blink.

### Adding components (for later labs)

Parts go in the `"parts"` array:

```json
{ "type": "wokwi-led", "id": "led1", "top": 100, "left": 200, "attrs": { "color": "red" } }
```

Connections go in the `"connections"` array:

```json
["led1:A", "uno:13", "green", []]
```

Format: `["partId:pinName", "partId:pinName", "wire-color", []]`

### Common part types

| Type | Component |
|------|-----------|
| `wokwi-arduino-uno` | Arduino Uno R3 |
| `wokwi-led` | LED (attrs: color) |
| `wokwi-resistor` | Resistor (attrs: resistance) |
| `wokwi-potentiometer` | Potentiometer |
| `wokwi-servo` | Servo motor |
| `wokwi-lcd1602` | 16x2 LCD display |
| `wokwi-pushbutton` | Pushbutton |
| `wokwi-buzzer` | Piezo buzzer |

Full list: https://docs.wokwi.com/parts/wokwi-arduino-uno

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Firmware not found" | Run `pio run` first — the `.hex` file doesn't exist until you compile |
| Simulator shows nothing | Check `diagram.json` has a microcontroller part (e.g., `wokwi-arduino-uno`) |
| Serial output not showing | Add `"serialMonitor": { "display": "auto" }` to diagram.json |
| Wrong board type | Match the `type` in diagram.json to your `platformio.ini` board |
| LED brightness looks binary (on/off) | This is a visual limitation of the sim — check Serial Monitor values instead. The PWM is working; Wokwi just doesn't render subtle brightness differences. Verify on real hardware. |

### General Rule: Trust the Serial Monitor, Not the Visuals

Wokwi's component rendering (especially LEDs) doesn't faithfully show analog behavior. If you need to verify smooth PWM output or analog changes, **read the serial log** — that's your ground truth in simulation. Save visual confirmation for physical hardware.

---

## Key docs

- Getting started: https://docs.wokwi.com/vscode/getting-started
- Project config: https://docs.wokwi.com/vscode/project-config
- Diagram format: https://docs.wokwi.com/diagram-format
- Example projects (PlatformIO): https://github.com/wokwi/arduino-simon-game
