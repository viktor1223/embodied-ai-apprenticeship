# Course 202: Vision & Perception-Driven Robotics

> How does a robot perceive the world?

**Deliverable:** Rover V4 — Vision-Guided Rover
**Prerequisite:** Course 201

---

## Core Objective

Bridge computer vision, real-time robotics, and embodied perception. The rover gains eyes and learns to act on what it sees.

---

## Theory Topics

### Computer Vision for Robotics

- Lane detection (edge-based and learned)
- Image segmentation (semantic and instance)
- Object detection (YOLO, SSD)
- Visual tracking (correlation, Kalman-based)
- Camera calibration and distortion

### Real-Time Constraints

- Inference latency and frame rate
- Edge deployment (running models on embedded hardware)
- Perception-action timing (how fast must decisions be?)
- Resolution vs speed tradeoffs

### Vision-Based Control

- Visual servoing (controlling motion from image features)
- Perception-driven steering
- Reactive vs predictive visual control
- Handling occlusion and ambiguity

---

## Hardware Setup

This is where the rover gets a second brain. The Arduino/ESP32 remains as the motor controller, but a **Raspberry Pi 5** is added on top for camera processing and inference.

```
[Pi 5 + Camera]  →  serial/I2C  →  [Arduino]  →  [Motors]
  (vision,                           (PWM,
   inference,                         real-time
   steering decisions)                control)
```

Training (if any) happens on your laptop/desktop. The Pi runs inference only.

---

## Resources

### Hardware

| Platform | Use For |
|----------|---------|
| Raspberry Pi + Camera | Initial vision experiments, lighter models |
| Jetson Orin Nano | Real-time inference, heavier models, production deployment |

### Courses

| Course | Focus |
|--------|-------|
| [NVIDIA Jetson AI Certification](https://developer.nvidia.com/embedded/learn/jetson-ai-certification-programs) | Edge AI, real-time inference, Jetson deployment |

### Frameworks

- OpenCV (classical vision)
- PyTorch / TensorRT (learned models)
- ROS2 image transport (if using ROS)

---

## Labs

### Lab 1: Camera Lane Following

**Objective:** Use a downward-facing or forward camera to detect lane lines and steer the rover to follow them.

**You will learn:**
- Image preprocessing for robotics
- Line detection (Hough transform or learned)
- Translating visual features into steering commands

---

### Lab 2: Object Tracking Turret

**Objective:** Mount a camera on a servo and track a moving object (e.g., colored ball) by centering it in frame.

**You will learn:**
- Visual tracking algorithms
- PID control from visual error
- Real-time processing constraints

---

### Lab 3: Visual Obstacle Avoidance

**Objective:** Use a camera to detect obstacles and navigate around them (replacing or augmenting ultrasonic sensors).

**You will learn:**
- Depth estimation from monocular vision (or stereo)
- Object segmentation for navigation
- Comparing vision-based vs proximity-based avoidance

---

### Lab 4: Semantic Object-Aware Navigation

**Objective:** Detect and classify objects in the environment, then make navigation decisions based on what is seen (e.g., avoid people, approach targets).

**You will learn:**
- Semantic understanding for decision-making
- Object detection integration with control
- Context-dependent behavior

---

## Deliverable: Rover V4

### Capabilities

- Camera-based lane following
- Object detection and tracking
- Visual navigation in structured environments
- Semantic awareness of surroundings

### Engineering Deliverables

- [ ] Vision pipeline architecture diagram
- [ ] Latency measurements (camera → decision → actuation)
- [ ] Model selection rationale (accuracy vs speed)
- [ ] Failure case documentation (lighting, occlusion, etc.)
- [ ] GitHub repository updates

### Demo Video

**Title:** "Teaching a Robot to Drive Using Vision"

Must explain:
- Perception latency and its effect on control
- How steering is estimated from visual input
- Failure cases and edge conditions
- Comparison with non-vision approaches

---

## Core Lesson

> Hand-engineered perception systems fail in complex environments.

Classical vision pipelines are brittle. They break with lighting changes, novel objects, and unstructured environments. Manually designing features and rules does not scale.

**This motivates Course 301: Learned Policies.**
