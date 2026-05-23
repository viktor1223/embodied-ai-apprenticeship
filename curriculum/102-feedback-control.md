# Course 102: Feedback Control & Reactive Robotics

> How does a robot correct itself?

**Deliverable:** Rover V2 — Reactive Autonomous Rover
**Prerequisite:** Course 101

---

## Core Objective

Learn feedback loops, PID intuition, sensor-driven correction, stability, and reactive autonomy.

The rover gains the ability to respond to its environment rather than blindly executing commands.

---

## Theory Topics

### Control Systems

- Error signals (desired vs actual)
- Feedback loops (open-loop vs closed-loop)
- Proportional control (P)
- PID control (Proportional, Integral, Derivative)
- Oscillation, overshoot, and stability
- Tuning methods

### Sensors

- Rotary encoders (wheel speed/position)
- Ultrasonic distance sensors
- IMUs (Inertial Measurement Units — accelerometer + gyroscope)
- Sensor noise and filtering basics

### Reactive Autonomy

- Obstacle avoidance behaviors
- Steering correction from sensor input
- Sensor → Decision → Action loops
- Behavior-based robotics concepts

---

## Resources

### YouTube

| Channel | Focus |
|---------|-------|
| [Brian Douglas](https://www.youtube.com/@BrianBDouglas) | Control systems theory with intuitive explanations |
| [DroneBot Workshop](https://www.youtube.com/@Dronebotworkshop) | Practical sensor and control projects |

### Books

| Book | Use For |
|------|---------|
| *Feedback Systems* (Åström & Murray) | Rigorous but accessible control theory |

---

## Labs

### Lab 1: Obstacle Avoidance Rover

**Objective:** Use ultrasonic sensors to detect obstacles and steer around them.

**You will learn:**
- Reactive behavior implementation
- Sensor latency and its effects on control
- Threshold-based decision making

---

### Lab 2: Distance-Keeping Robot

**Objective:** Maintain a fixed distance from a wall or object using feedback control.

**You will learn:**
- Adaptive cruise control concepts
- Proportional (and PID) feedback control
- Steady-state error and correction

---

### Lab 3: Self-Balancing Robot

**Objective:** Build a two-wheeled balancing robot using an IMU and PID control.

**You will learn:**
- Inherent instability and active stabilization
- Control loop tuning (gains, response time)
- IMU data interpretation (complementary filter)

---

## Deliverable: Rover V2

### Capabilities

- Autonomous obstacle avoidance
- Distance regulation (maintain setpoint)
- Reactive steering correction
- Stable behavior in dynamic environments

### Engineering Deliverables

- [ ] Control loop block diagram
- [ ] PID tuning notes (what worked, what oscillated)
- [ ] Sensor integration documentation
- [ ] Comparison: open-loop vs closed-loop behavior
- [ ] GitHub repository updates

### Demo Video

**Title:** "Why Open-Loop Robots Fail"

Must demonstrate:
- Open-loop drift and inconsistency
- Instability without feedback
- Corrective behavior with feedback enabled
- Side-by-side comparison of V1 vs V2

---

## Core Lesson

> Feedback fails when the robot cannot estimate its own state accurately.

PID can correct errors, but only if the robot knows where it is and what it's doing. Noisy sensors, drift, and incomplete measurements limit what reactive control can achieve.

**This motivates Course 201: State Estimation.**
