# Course 301: Learned Policies & Robot Learning

> Can robots learn behavior instead of hardcoded rules?

**Deliverable:** Rover V5 — Learned Navigation Rover
**Prerequisite:** Course 202

---

## Core Objective

Transition from explicit robotics logic to learned robot behavior. Instead of hand-coding every rule, the rover learns from demonstrations and experience.

---

## Hardware Setup

Same architecture as Course 202: Raspberry Pi 5 handles policy inference, Arduino handles motors. Training happens entirely off-board on your laptop/desktop GPU.

```
[Desktop GPU]  →  trains policy  →  deploys to  →  [Pi 5]  →  commands  →  [Arduino]  →  [Motors]
```

If inference is too slow on the Pi 5 for your model size, this is where a Jetson Orin Nano becomes worth considering — but start with the Pi and only upgrade if you hit a wall.

---

## Theory Topics

### Imitation Learning

- Behavior cloning (supervised learning from demonstrations)
- Dataset collection for robotics (teleoperation, human demos)
- Trajectory learning and action prediction
- Distribution shift and compounding errors (DAgger)

### Robot Learning

- Policy representation (neural networks as controllers)
- Action spaces (continuous vs discrete)
- Diffusion policy (denoising actions from noise)
- Vision-Language-Action models (VLA)
- Reward-free learning approaches

### Simulation

- Physics simulation for robotics (why and when)
- Domain randomization
- Sim-to-real transfer challenges
- Reality gap and how to close it

---

## Resources

### Simulation Platforms

| Platform | Use For |
|----------|---------|
| [Isaac Sim](https://developer.nvidia.com/isaac/sim) | High-fidelity robotics simulation, GPU-accelerated |
| [MuJoCo](https://mujoco.readthedocs.io/) | Fast physics simulation, research standard |

### Key Papers

| Paper | Contribution |
|-------|-------------|
| [Diffusion Policy](https://diffusion-policy.cs.columbia.edu/) | Denoising diffusion for robot action generation |
| [OpenVLA](https://openvla.github.io/) | Open-source Vision-Language-Action model |
| [ACT (Action Chunking with Transformers)](https://tonyzhaozh.github.io/aloha/) | Transformer-based imitation learning |

### Additional Reading

- Behavior cloning tutorial papers
- DAgger (Dataset Aggregation) original paper
- RT-1 (Robotics Transformer) for context on scaling

---

## Labs

### Lab 1: Behavior Cloning Steering Policy

**Objective:** Collect human driving demonstrations (teleoperated rover), then train a neural network to predict steering commands from camera images.

**You will learn:**
- Data collection for imitation learning
- Training a policy network (image → action)
- Evaluating learned vs hand-coded behavior
- Distribution shift in practice

---

### Lab 2: Learned Navigation Behavior

**Objective:** Train a policy to navigate a simple environment (hallway, track) end-to-end from vision input.

**You will learn:**
- End-to-end learning pipelines
- Handling multiple behaviors (straight, turn, stop)
- When learned policies outperform engineered ones

---

### Lab 3: Sim-to-Real Transfer

**Objective:** Train a navigation policy in simulation, then deploy it on the physical rover.

**You will learn:**
- Setting up a simulation environment
- Domain randomization techniques
- The reality gap and transfer challenges
- Fine-tuning in the real world

---

## Deliverable: Rover V5

### Capabilities

- Learned steering from demonstration data
- Imitation learning-based navigation
- Policy-driven behavior (no hand-coded rules)
- Basic sim-to-real transfer

### Engineering Deliverables

- [ ] Dataset collection pipeline and tooling
- [ ] Training infrastructure (scripts, configs, logging)
- [ ] Policy evaluation metrics (success rate, deviation)
- [ ] Comparison: learned vs hand-coded performance
- [ ] Failure analysis (when does the policy break?)
- [ ] GitHub repository updates

### Demo Video

**Title:** "When Hardcoded Robotics Stops Working"

Must explain:
- Edge cases that break hand-coded systems
- Brittleness of rule-based approaches
- How learning-based control adapts
- Remaining limitations of learned policies

---

## Core Lesson

> Learned policies fail without memory and prediction.

A behavior-cloned policy reacts to the current observation. It has no memory of where it's been, no prediction of what comes next, and no ability to plan over long horizons. It is reactive, not cognitive.

**This motivates Course 401: World Models.**
