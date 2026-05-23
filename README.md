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
