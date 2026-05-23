# Embodied AI Robotics Curriculum

## From Physical Control to Autonomous World Models

---

## Philosophy

This curriculum transforms an AI/perception engineer into an embodied AI systems engineer capable of building autonomous robotic agents and implementing modern robotics research on physical systems.

Everything revolves around **one evolving platform** — not disconnected tutorials. Each phase solves a limitation of the previous phase, increases autonomy, introduces a new abstraction layer, and builds toward embodied cognition.

---

## The Evolving Rover

The rover is the central research platform. It grows across the entire curriculum:

| Version | Capability | Course |
|---------|-----------|--------|
| V1 | Open-loop movement | 101 |
| V2 | Feedback control | 102 |
| V3 | State estimation | 201 |
| V4 | Vision perception | 202 |
| V5 | Autonomous navigation | 301 |
| V6 | Learned policies | 301 |
| V7 | World models | 401 |
| V8 | Embodied cognition | Capstone |

---

## Course Sequence

| Course | Title | Key Question |
|--------|-------|--------------|
| [101](101-physical-embodiment.md) | Physical Embodiment & Actuation | How does a robot move intentionally? |
| [102](102-feedback-control.md) | Feedback Control & Reactive Robotics | How does a robot correct itself? |
| [201](201-state-estimation.md) | State Estimation & Robot Awareness | How does a robot know where it is? |
| [202](202-vision-perception.md) | Vision & Perception-Driven Robotics | How does a robot perceive the world? |
| [301](301-learned-policies.md) | Learned Policies & Robot Learning | Can robots learn behavior instead of hardcoded rules? |
| [401](401-world-models.md) | World Models & Predictive Robotics | Can robots imagine the future? |
| [Capstone](capstone.md) | Embodied Autonomous Agent Platform | Full integration |

---

## Hardware Progression

The rover's compute evolves as the curriculum demands more processing power. The Arduino/ESP32 stays as the low-level motor controller throughout — it never goes away. What changes is what sits on top of it.

| Course | Compute Brain | Why |
|--------|--------------|-----|
| 101–102 | Arduino / ESP32 only | Direct motor control, sensors, PWM — no heavy compute needed |
| 201 | Arduino + Raspberry Pi (optional) | Pi useful for logging, visualization, and running filters — but Arduino alone can handle it |
| 202 | Arduino + Raspberry Pi 5 | Camera processing requires Linux, OpenCV, and real-time inference |
| 301 | Arduino + Raspberry Pi 5 | Policy inference runs on Pi; training happens on your laptop/desktop GPU |
| 401 | Arduino + Raspberry Pi 5 (or Jetson Orin Nano) | World model inference is heavier — Pi 5 can handle small models, Jetson for larger ones |

**Architecture pattern from 202 onward:**
```
[Raspberry Pi / Jetson]  ←→  [Arduino/ESP32]  ←→  [Motors + Sensors]
    (perception,               (real-time              (physical
     planning,                  motor control,          world)
     inference)                 sensor reading)
```

The Pi/Jetson handles vision, inference, and planning. It sends high-level commands (speed, direction) over serial/I2C to the Arduino, which handles the real-time motor control loop. Training always happens off-board on a workstation with a GPU.

---

## Progression Logic

Each course exists because the previous approach failed:

```
Open-loop fails    → because reality is inconsistent       → motivates feedback
Feedback fails     → because state estimation is poor      → motivates filtering
Reactive fails     → because perception is incomplete      → motivates vision
Hand-engineered    → fails in complex environments         → motivates learning
Learned policies   → fail without memory and prediction    → motivates world models
```

---

## Deliverables Per Course

Every course requires:

- Working rover iteration with new capabilities
- Wiring diagram / subsystem architecture
- Signal flow or system diagram
- Debug notes and engineering reflections
- GitHub commits with documentation
- Demo video explaining the work and its limitations

---

## How to Use This Curriculum

1. Work through courses sequentially — each builds on the last
2. Complete all labs before attempting the deliverable
3. Watch/read the listed resources before starting labs
4. Document everything in the `research_journal/` folder
5. Record demo videos that explain both successes and failures
6. Push all code and diagrams to the `projects/` folder
