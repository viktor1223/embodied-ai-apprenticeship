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

---

## Lab 2: Servo Control — Full Lesson Breakdown

### Demo Video

`projects/101/lab2-servo-control/lab2-servo-pot-demo.mp4` (local only, gitignored)

Shows: physical Arduino Uno + 850kΩ pot + SG90 servo, pot controlling servo angle in real time.

### The Iterative Wiring Process (3 Attempts in Sim, 1 Fix on Hardware)

This is the core teaching moment — NOT the code. The code was trivial. The wiring is where all the learning happened.

**Attempt 1 — wrong mental model of everything:**
- Pot VCC → pin 13 (treated power pin like a signal output)
- Servo pinout backwards (GND and PWM swapped)
- No signal wire from pot to Arduino at all

**Attempt 2 — fixed servo, still confused about pot:**
- Servo wiring corrected
- Pot SIG → pin 11 (PWM output, not analog input)
- Pot VCC → 3.3V (works but 5V gives full ADC range)

**Attempt 3 — correct:**
- Pot SIG → A0 (analog INPUT pin)
- Pot VCC → 5V
- All servo connections correct

**Physical build — one more fix:**
- Followed diagram but missed the signal wire entirely (only connected power + ground)
- Symptom: servo made one sound at startup, then nothing
- Diagnosis: servo works (proved by startup), pot has no signal path to Arduino
- Fix: add wire from pot middle pin to A0

### Key Insight for YouTube Script

The lesson isn't "how to wire a servo." It's:
> "The foundation isn't code. The foundation is the mental model of signal flow."

Every wiring mistake traced back to confusing:
- Input vs output (which direction does data flow?)
- Signal vs power (what carries information vs what supplies energy?)
- Pin function (what can this pin actually do?)

### Hardware-Specific Lessons

- **850kΩ pot works** but needs software averaging (10 reads, 2ms apart) — Arduino ADC recommends ≤10kΩ source impedance
- **SG90 powered from Arduino 5V** works for no-load demos but will brownout under real torque
- **Servo startup twitch** is normal — `attach()` sends it to position 0
- Physical pot middle pin = wiper = signal (always)

### What Wokwi Gave Us vs What Hardware Gave Us

| Wokwi | Physical hardware |
|-------|-------------------|
| Fast iteration on wiring logic | Proved the system actually works |
| Caught pin-type confusion (3 attempts) | Caught missing wire (signal not connected) |
| Serial monitor = ground truth | Servo visually moves (satisfying) |
| No risk of burning components | Real current/power behavior |
| Servo didn't animate (sim limitation) | Servo responds immediately |

---

## Lab 3: DC Motor Control — Power Budget Deep Dive

### The Core Lesson (Discovered the Hard Way)

Motor buzzed but didn't spin. Code was correct. Wiring was correct. Problem: **power budget**.

This is the first lab where signal correctness isn't enough — you must also get the *energy* right.

### How to Find the Numbers: Datasheet Reading

Every power budget calculation requires three datasheets. Here's where to find each one:

**1. Arduino Uno R3 — Power Supply Limits**

* Source: [docs.arduino.cc/hardware/uno-rev3](https://docs.arduino.cc/hardware/uno-rev3/) → "Tech Specs" tab
* Datasheet PDF: [A000066-datasheet.pdf](https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf)

Key specs to extract:

| Parameter | Value | Where to find |
|-----------|-------|---------------|
| I/O Voltage | 5V | Tech Specs table |
| DC Current per I/O Pin | 20 mA | Tech Specs table |
| 5V pin max output (USB powered) | ~500 mA | ATmega328P datasheet §28 + USB spec |
| 5V pin max output (barrel jack) | ~900 mA | After regulator losses |
| Input voltage (nominal) | 7–12V | Tech Specs table |

The 5V pin is NOT a motor power supply. It passes through from USB (500 mA total for the entire board + peripherals) or the onboard regulator.

**2. L298N Motor Driver — Voltage Drop**

* Source: [components101.com/modules/l293n-motor-driver-module](https://components101.com/modules/l293n-motor-driver-module)
* ST Datasheet: [st.com/resource/en/datasheet/l298.pdf](https://www.st.com/resource/en/datasheet/l298.pdf)
* Look for: "Saturation Voltage" table (Table 4 in the ST datasheet)

Key specs:

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Motor Supply Voltage (VS) | 5–46V | External battery connects here |
| V_CEsat (high side) | ~1.2V @ 1A | Voltage eaten by top transistor |
| V_CEsat (low side) | ~1.2V @ 1A | Voltage eaten by bottom transistor |
| **Total path drop** | **~2–3V** | High + low + wiring + sense resistor |
| Logic supply (VSS) | 5V | From Arduino 5V pin (only ~20 mA) |
| Max continuous current | 2A per channel | Thermal limit with heatsink |

The L298N uses **bipolar (BJT) transistors** — these have a fixed voltage drop (V_CEsat) regardless of current. This is the key insight: you always lose 2–3V through the bridge.

**3. DC Motor (FA-130 type, typical hobby motor)**

* Source: [Mabuchi FA-130 datasheet](https://www.mabuchi-motor.com/product/detail/27) or seller specs
* What to look for: Rated voltage, no-load current, stall current

Typical FA-130 specs:

| Parameter | Value |
|-----------|-------|
| Rated voltage | 3–6V |
| No-load current | ~150–200 mA |
| Stall current | ~800 mA |
| No-load speed | ~9000 RPM @ 3V |

### The Formula

```text
V_motor = (V_S − V_drop) × (PWM / 255)
```

Where:

* `V_S` = voltage at the L298N "12V" terminal (your battery)
* `V_drop` = total H-bridge voltage drop (~2–3V for L298N)
* `PWM` = analogWrite value (0–255)
* `V_motor` = effective voltage the motor actually sees

### Worked Example: Why USB Power Failed

Our setup: Arduino USB → 5V pin → L298N VS terminal. PWM at 75% (analogWrite 191).

```text
V_S       = 5.0V  (from Arduino 5V pin, which is USB bus voltage)
V_drop    = 2.5V  (typical L298N path: high-side + low-side + sense resistor)
Available = 5.0 − 2.5 = 2.5V
PWM duty  = 191/255 = 0.75

V_motor   = 2.5V × 0.75 = 1.875V
```

**Result:** 1.875V applied to a motor rated for 3–6V. The motor has enough voltage to energize the coils (you hear buzzing) but not enough torque to overcome static friction and start spinning.

### Worked Example: With a 4×AA Battery Pack (6V)

Same code, but battery connected to the L298N "12V" terminal:

```text
V_S       = 6.0V  (4 × 1.5V alkaline AAs)
V_drop    = 2.5V
Available = 6.0 − 2.5 = 3.5V
PWM duty  = 191/255 = 0.75

V_motor   = 3.5V × 0.75 = 2.625V
```

Better — marginal. Motor will spin unloaded but may stall with any resistance.

### Worked Example: With a 9V Supply

```text
V_S       = 9.0V  (barrel jack adapter or 6×AA pack)
V_drop    = 2.5V
Available = 9.0 − 2.5 = 6.5V
PWM duty  = 191/255 = 0.75

V_motor   = 6.5V × 0.75 = 4.875V
```

Solid. Motor runs well within its 3–6V range at 75% speed.

### Why Not Just Use 12V?

You can. The L298N handles up to 46V. But:

```text
V_S       = 12.0V
V_drop    = 2.5V
Available = 12.0 − 2.5 = 9.5V at full PWM
```

At 100% PWM, that's 9.5V on a motor rated for 6V max → overheating, shortened lifespan, possible burnout. You'd need to limit PWM to ~160/255 (63%) to keep the motor safe.

### The MOSFET Alternative: TB6612FNG / DRV8833

Modern motor drivers use MOSFETs instead of BJTs:

| Driver | Type | Voltage drop | Implication |
|--------|------|-------------|-------------|
| L298N | Bipolar (BJT) | ~2–3V | Need VS ≫ V_motor_rated |
| TB6612FNG | MOSFET | ~0.1–0.5V | Can run motors on 5V directly |
| DRV8833 | MOSFET | ~0.2–0.3V | Even more efficient |

With a TB6612 on USB 5V:

```text
V_S       = 5.0V
V_drop    = 0.3V  (MOSFET R_DS(on) × current, much lower)
Available = 5.0 − 0.3 = 4.7V

V_motor   = 4.7V × 0.75 = 3.525V  ← motor spins fine!
```

**Rover planning lesson:** If you want USB-powered prototyping, use a MOSFET driver. If you have an external battery (you will for a rover), L298N works fine with 7–12V supply.

### Minimum Supply Voltage Rule of Thumb

```text
V_S(min) = V_motor_rated + V_drop_driver + margin

For L298N + FA-130:  3V + 3V + 1V = 7V minimum supply
For TB6612 + FA-130:  3V + 0.5V + 0.5V = 4V minimum supply
```

### Current Budget (Secondary Concern)

| Source | Max current | Can it drive a motor? |
|--------|-------------|----------------------|
| Arduino I/O pin (e.g., pin 9) | 20 mA | NO — control signal only |
| Arduino 5V pin (USB) | ~500 mA total | Barely — one small motor at no-load |
| L298N VS input | 2A per channel | Yes — that's what it's for |
| 4×AA battery pack | ~2A sustained | Yes — well matched to L298N |

The I/O pins (ENA, IN1, etc.) only carry **control signals** (~5–15 mA). The motor power comes from VS, through the L298N's transistors, out to the motor. This is why you need a separate power supply.

### Summary: The Signal/Power Split

```text
Signal path:  Arduino pin 9 → ENA (tells L298N how fast)
              Arduino pin 8 → IN1 (tells L298N which direction)
              Arduino pin 7 → IN2

Power path:   Battery(+) → L298N 12V/VS terminal
              L298N OUT1 → Motor terminal 1
              L298N OUT2 → Motor terminal 2
              Battery(−) → L298N GND → Arduino GND (shared ground!)
```

The Arduino never supplies motor current. It only supplies *instructions*.

