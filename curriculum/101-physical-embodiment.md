# Course 101: Physical Embodiment & Actuation

> How does a robot move intentionally?

**Deliverable:** Rover V1 — Open-Loop Rover

---

## Core Objective

Develop intuition for motors, servos, power systems, signal flow, embedded systems, and electrical architecture.

By the end of this course, physical systems stop feeling magical.

---

## Theory Topics

### Electronics Foundations

- Voltage, current, resistance
- PWM (Pulse Width Modulation)
- Analog vs digital signals
- Grounding and power distribution
- Breadboard prototyping
- Pull-up / pull-down resistors

### Embedded Systems

- GPIO (General Purpose I/O)
- ADC (Analog-to-Digital Conversion)
- Interrupts and timing
- PWM generation
- Serial debugging (UART)

### Actuation

- Servo motors (position control)
- DC motors (continuous rotation)
- H-bridges (bidirectional motor control)
- Differential drive (tank steering)

---

## Resources

### YouTube

| Channel | Focus |
|---------|-------|
| [Afrotechmods](https://www.youtube.com/@afrotechmods) | Electronics fundamentals with clear visuals |
| [Paul McWhorter Arduino Course](https://www.youtube.com/playlist?list=PLGs0VKk2DiYxD8tlakcyaz1T3Am6CzcfH) | Step-by-step Arduino from zero |
| [Jeremy Fielding](https://www.youtube.com/@JeremyFieldingSr) | Motors, mechanisms, and practical builds |

### Books

| Book | Use For |
|------|---------|
| *Practical Electronics for Inventors* | Reference for circuits, components, and design |
| *Make: Electronics* | Hands-on experiments and intuition building |

### Digital Wiring Diagrams

| Tool | Use For |
|------|---------|
| [Fritzing](https://fritzing.org/) | Breadboard-style diagrams, beginner-friendly |
| [KiCad](https://www.kicad.org/) | Professional schematics and PCB design (free/open-source) |
| [Wokwi](https://wokwi.com/) | Online Arduino/ESP32 simulator with visual wiring |

---

## Labs

### Lab 1: LED Brightness with Potentiometer

**Objective:** Read an analog input (potentiometer) and map it to PWM output (LED brightness).

**You will learn:**
- Analog input reading (ADC)
- PWM output generation
- Signal mapping between ranges

**Reference links:**
- [Arduino: Analog In, Out Serial (this exact lab)](https://docs.arduino.cc/built-in-examples/analog/AnalogInOutSerial/)
- [analogRead()](https://docs.arduino.cc/language-reference/en/functions/analog-io/analogRead/)
- [analogWrite() / PWM](https://docs.arduino.cc/language-reference/en/functions/analog-io/analogWrite/)
- [map() function](https://www.arduino.cc/reference/en/language/functions/math/map/)

**Project:** `projects/101/lab1-led-pot/`

**Theory deep-dive:** [ADC, Quantization, and Signal Mapping](../resources/adc-quantization-and-mapping.md)

---

### Lab 2: Servo Angle Control

**Objective:** Control a servo motor's angle using a potentiometer or serial input.

**You will learn:**
- PWM actuation for position control
- Signal timing requirements
- Control interfaces and signal standards

**Reference links:**
- [Servo Motor Basics with Arduino (Knob + Sweep)](https://docs.arduino.cc/learn/electronics/servo-motors/)
- [Servo Library reference](https://docs.arduino.cc/libraries/servo/)
- [Knob example (pot → servo)](https://www.arduino.cc/en/Tutorial/Knob)
- [Sweep example (auto 0–180°)](https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep)

**Project:** `projects/101/lab2-servo-control/`

---

### Lab 3: Motor Driver + DC Motor

**Objective:** Wire and control a DC motor through an H-bridge motor driver (e.g., L298N or TB6612).

**You will learn:**
- H-bridge operation and wiring
- Bidirectional motor control
- Power constraints and separate power rails

**Reference links:**
- [Arduino: DC Motor Control with L298N](https://docs.arduino.cc/learn/electronics/stepper-motors/)
- [L298N H-Bridge Motor Driver Datasheet](https://www.st.com/resource/en/datasheet/l298.pdf)
- [TB6612FNG Hookup Guide (SparkFun)](https://learn.sparkfun.com/tutorials/tb6612fng-hookup-guide)
- [H-Bridge Theory of Operation](https://www.modularcircuits.com/blog/articles/h-bridge-secrets/h-bridges-the-basics/)

---

### Lab 4: Build Your Own "Servo"

**Objective:** Create a closed-loop position control system using a DC motor + encoder (or potentiometer as feedback).

**You will learn:**
- Feedback concepts (reading position, computing error)
- Closed-loop thinking
- Motor + encoder integration

**Reference links:**
- [Arduino PID Library](https://playground.arduino.cc/Code/PIDLibrary/)
- [Rotary Encoder Basics (Last Minute Engineers)](https://lastminuteengineers.com/rotary-encoder-arduino-tutorial/)
- [PID Control — A Brief Introduction](https://www.arrow.com/en/research-and-events/articles/pid-controller-basics-and-tutorial-pid-implementation-in-arduino)
- [Building a Servo from a DC Motor (YouTube — James Bruton)](https://www.youtube.com/watch?v=dTGITLnYAY0)

---

## Deliverable: Rover V1

### Capabilities

- Timed forward/backward movement
- Turning (differential drive)
- Scripted path execution (e.g., drive a square)

### Engineering Deliverables

- [ ] Wiring diagram (hand-drawn or digital)
- [ ] Subsystem architecture diagram
- [ ] Signal flow diagram (input → processing → output)
- [ ] Debug notes documenting issues encountered
- [ ] GitHub repository with code and documentation

### Demo Video

**Title:** "Building My First Open-Loop Robot"

Must explain:
- How power flows through the system
- How PWM controls motor speed
- How motor control signals work
- Why open-loop systems have limitations

---

## Core Lesson

> Open-loop systems fail because reality is inconsistent.

You will see this firsthand: command the rover to drive a perfect square, then run it multiple times. Each attempt will produce a different shape. The rover drifts, turns too far or too little, and ends up in a different position every time. Without sensing the result of its own actions, it cannot correct for friction differences, battery voltage drop, or uneven surfaces.

**This motivates Course 102: Feedback Control.**
