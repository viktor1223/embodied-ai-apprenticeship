# Robotics From First Principles

An independent embodied robotics curriculum and engineering journal documenting the journey from physical control systems to modern embodied AI.

This repository follows a structured, project-based learning path designed to rebuild robotics intuition from the physical layer upward.

Rather than building disconnected tutorials or hobby projects, the curriculum revolves around **one evolving robotics platform**. The rover develops new capabilities over time while each phase solves a limitation of the previous approach.

---

## Learning Philosophy

### Build First

Theory matters. But robotics intuition comes from wiring mistakes, unstable controllers, noisy sensors, debugging power issues, and physical failure modes.

The goal is not passive consumption. The goal is engineering fluency.

### Every Course Solves A Failure

The curriculum follows the historical progression of robotics systems.

```text
Open-loop motion fails       → need feedback
Feedback fails               → need state estimation
Estimation fails             → need richer perception
Hand-engineered perception fails → need learned policies
Learned policies fail        → need memory + prediction
Prediction leads toward world models
```

Each version of the rover introduces new theory, new sensors, new architecture, and new autonomy capabilities.

---

## Curriculum Roadmap

| Course | Focus | Rover Version |
|--------|-------|---------------|
| 101 | Physical Embodiment & Actuation | V1 — Open-Loop Rover |
| 102 | Feedback & Reactive Robotics | V2 — Reactive Rover |
| 201 | State Estimation & Localization | V3 — State-Aware Rover |
| 202 | Vision & Perception Robotics | V4 — Vision Rover |
| 301 | Learned Policies & Robot Learning | V5 — Learned Policy Rover |
| 401 | World Models & Predictive Robotics | V6 — World Model Rover |

Full course outlines live in `curriculum/`.

---

## AI-Assisted Learning Setup

This repo is designed to be worked through *with* an AI assistant (GitHub Copilot, ChatGPT, etc.) acting as a Socratic tutor — not an answer key.

### How it works

Custom instruction files in `.github/instructions/` shape AI behavior in this repo:

| File | What it does |
|------|-------------|
| `socratic-learning.instructions.md` | Makes the AI ask what you predict/diagnose before giving answers |
| `copilot-instructions.md` | General repo rules (teaching voice, documentation standards) |

### The learning protocol

```text
1. Wire/build what you THINK is correct (predict)
2. Show AI your attempt — it checks your mental model, not just pin numbers
3. Diagnose failures yourself before asking for the fix
4. AI generates code (syntax isn't the learning) — you verify you understand it
5. Document broken mental models → those are the real lessons
```

### Key resources

- [Using AI as a Learning Accelerator](resources/using-ai-as-learning-accelerator.md) — full workflow guide
- [Research Journal: AI Accelerator Paradox](research_journal/2026-05-23-ai-accelerator-paradox.md) — why this approach works

### Setting this up yourself

1. Use VS Code with GitHub Copilot (or any editor with AI chat)
2. The `.github/instructions/` files are automatically picked up by Copilot
3. The AI will ask you to predict before confirming, challenge your mental models, and flag learning moments
4. If you want to skip the Socratic mode and just get an answer, say so — the instructions account for that

---

## Wokwi Simulation: What It Is and What It Isn't

We use [Wokwi for VS Code](https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode) to simulate circuits before building them physically. But know its limits:

**Wokwi is good for:**
- Validating wiring logic (correct pins, correct signal paths)
- Debugging mental models with AI (paste your diagram, get feedback)
- Verifying code logic via Serial Monitor output
- Fast iteration without burning components

**Wokwi is NOT good for:**
- Visual confirmation that things work (LED brightness, servo movement often don't render faithfully)
- Power behavior (no capacitor simulation, no brownout, no current limits)
- Replacing real hardware testing

**The rule:** Wokwi proves your *logic* is right. Physical hardware proves your *system* works. You need both. If the serial output shows correct values but the component doesn't animate — that's a sim limitation, not a bug in your circuit. Build it for real to see it move.

### Custom Wokwi Chips

Wokwi does not include every component (no L298N H-bridge, no DC motor). We build custom chips to fill the gaps. These live in `shared/wokwi-chips/` as the source of truth and get copied into each project's `chips/` folder.

| Chip | Location | What it simulates |
|------|----------|-------------------|
| L298N | `shared/wokwi-chips/l298n/` | Dual H-bridge motor driver — enable gating, direction logic, voltage output |
| DC Motor | `shared/wokwi-chips/dc-motor/` | Reads terminal voltage differential, prints direction and speed % to console |

**How to use them in a project:**

1. Copy the `.chip.json` and `.chip.c` files into your project's `chips/` directory
2. Reference them in `diagram.json` with type `"chip-l298n"` or `"chip-dc-motor"`
3. Wire pins as normal in the `"connections"` array
4. Run `pio run` then start the Wokwi simulator — chip output appears in the debug console

**Adding new chips:** Create a new folder under `shared/wokwi-chips/<chip-name>/` with a `.chip.json` (pin definitions, controls) and a `.chip.c` (logic using the [Wokwi Chips API](https://docs.wokwi.com/chips-api/getting-started)).

---

## Repository Structure

```text
embodied-ai-apprenticeship/
├── curriculum/          # Course outlines and theory progression
├── projects/            # Firmware, wiring, and build artifacts per rover version
├── research_journal/    # Failures, debugging, design changes, lessons learned
├── resources/           # Books, papers, courses, references
├── evaluation/          # Self-assessment and milestone tracking
└── shared/              # Reusable libraries and utilities
```

---

## Research Journal

This repository also functions as an engineering journal.

The goal is to document failures, debugging process, design changes, lessons learned, and evolving robotics intuition. Not polished tutorials. A public record of rebuilding robotics understanding from motors and control loops toward embodied intelligence.

---

## Long-Term Objective

An embodied robotics platform capable of perception, memory, planning, prediction, learning, world modeling, and autonomous decision making — bridging classical robotics, modern AI, and embodied cognition.

---

## Prerequisites

- Arduino-compatible microcontroller (ESP32 or similar)
- PlatformIO or Arduino IDE
- Basic electronics (breadboard, multimeter, power supply)
- C/C++ fundamentals

---

## Current Status

**Phase:** Course 101 — Physical Embodiment & Actuation

> Build a differential drive rover capable of reliable open-loop motion using Arduino-controlled motor actuation.
