# Course 201: State Estimation & Robot Awareness

> How does a robot know where it is?

**Deliverable:** Rover V3 — State-Aware Rover
**Prerequisite:** Course 102

---

## Core Objective

Learn odometry, sensor fusion, localization, filtering, and robot state representation.

This is one of the most important courses in the curriculum. A robot that cannot estimate its own state cannot plan, navigate, or learn effectively.

---

## Theory Topics

### Estimation Fundamentals

- Noise in physical measurements
- Drift and accumulated error
- Uncertainty representation
- Probabilistic state estimation
- Gaussian distributions in robotics

### Sensor Fusion

- IMU + encoder fusion
- Complementary filters
- Kalman filter (intuition and implementation)
- Extended Kalman Filter (EKF) basics
- When to trust which sensor

### Localization

- Wheel odometry (forward kinematics)
- Dead reckoning and its limitations
- Coordinate frames and transformations
- Pose representation (x, y, θ)
- Mapping robot motion over time

---

## Resources

### Books

| Book | Use For |
|------|---------|
| *Probabilistic Robotics* (Thrun, Burgard, Fox) | Definitive reference for estimation and localization |
| *Modern Robotics* (Lynch & Park) | Kinematics, coordinate frames, motion planning |

### Courses

| Course | Focus |
|--------|-------|
| [MIT Underactuated Robotics](https://underactuated.mit.edu/) | Dynamics, control, and estimation |
| [Modern Robotics (Northwestern)](https://modernrobotics.northwestern.edu/) | Kinematics, dynamics, and motion planning |

---

## Labs

### Lab 1: Wheel Odometry Estimation

**Objective:** Estimate rover position using encoder ticks and differential drive kinematics.

**You will learn:**
- Forward kinematics for differential drive
- Accumulating position from wheel rotations
- Drift over time without correction

---

### Lab 2: IMU Orientation Tracking

**Objective:** Track the rover's heading using gyroscope integration and accelerometer tilt.

**You will learn:**
- Gyroscope drift
- Accelerometer noise
- Complementary filtering for orientation

---

### Lab 3: Sensor Fusion Rover

**Objective:** Combine encoder odometry and IMU data using a Kalman filter (or complementary filter) for improved state estimation.

**You will learn:**
- Fusing multiple noisy sensors
- Prediction + correction cycle
- Improved accuracy over either sensor alone

---

### Lab 4: Map Robot Trajectory Over Time

**Objective:** Log and visualize the rover's estimated trajectory in 2D as it moves through the environment.

**You will learn:**
- Telemetry logging and data collection
- Visualization of estimated vs actual paths
- Quantifying estimation error

---

## Deliverable: Rover V3

### Capabilities

- Real-time orientation estimation
- Dead reckoning with odometry
- Trajectory awareness (where have I been?)
- Telemetry logging and post-analysis

### Engineering Deliverables

- [ ] Kalman filter implementation (or complementary filter)
- [ ] Sensor fusion block diagram
- [ ] Trajectory plot comparing estimated vs ground truth
- [ ] Analysis of drift over distance/time
- [ ] GitHub repository updates

### Demo Video

**Title:** "How Robots Estimate Reality"

Must explain:
- Why sensors drift over time
- How uncertainty accumulates
- What estimation errors look like in practice
- How fusion improves raw sensor data

---

## Core Lesson

> Reactive robots fail because perception is incomplete.

Even with good state estimation, a robot relying only on proximity sensors has a narrow view of the world. It cannot recognize objects, understand scenes, or make informed decisions about complex environments.

**This motivates Course 202: Vision Perception.**
