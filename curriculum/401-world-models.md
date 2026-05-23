# Course 401: World Models & Predictive Robotics

> Can robots imagine the future?

**Deliverable:** Rover V6 — Embodied World Model Rover
**Prerequisite:** Course 301

---

## Core Objective

Develop predictive embodied systems with latent world representations, future-state reasoning, and planning over imagined futures.

The rover moves from reactive intelligence to predictive intelligence — it can reason about what will happen before it acts.

---

## Hardware Setup

World models are neural networks — they do not run on an Arduino. The compute architecture:

```
[Desktop GPU]  →  trains world model  →  deploys to  →  [Pi 5 or Jetson Orin Nano]  →  commands  →  [Arduino]  →  [Motors]
```

**Option A: Raspberry Pi 5** — works for smaller models (compressed VAEs, lightweight sequence models). Use ONNX Runtime or TensorFlow Lite for optimized inference. Start here.

**Option B: Jetson Orin Nano** — needed if your world model requires GPU inference at control frequency (>10 Hz with larger architectures). Upgrade only if Pi 5 can't keep up.

The Arduino still handles real-time motor control and sensor reading. That layer doesn't change.

---

## Theory Topics

### World Models

- Latent state representations (compressed world understanding)
- Future prediction from current state + action
- Dreaming: planning through imagined rollouts
- Model-based reinforcement learning
- Variational autoencoders for world compression

### Embodied Cognition

- Memory in robotic systems (episodic, semantic)
- Semantic grounding (connecting symbols to physical experience)
- Long-horizon behavior and temporal abstraction
- Goal-conditioned behavior

### Planning

- Predictive action selection (choose actions by imagining outcomes)
- Latent trajectory rollout (simulate futures in compressed space)
- Model Predictive Control (MPC) with learned models
- Hierarchical planning (abstract goals → concrete actions)

---

## Resources

### Key Papers

| Paper | Contribution |
|-------|-------------|
| [RT-1](https://robotics-transformer1.github.io/) | Large-scale robotic learning with transformers |
| [RT-2](https://robotics-transformer2.github.io/) | Vision-language models as robot policies |
| [PaLM-E](https://palm-e.github.io/) | Embodied multimodal language model |
| [Dreamer (v1/v2/v3)](https://danijar.com/dreamer/) | World models for decision-making |
| [GAIA-1](https://wayve.ai/thinking/scaling-gaia-1/) | Generative world model for autonomous driving |

### Additional Reading

- Ha & Schmidhuber "World Models" (2018) — foundational paper
- Decision Transformer — sequence modeling for RL
- UniSim — universal simulation via generative models

---

## Labs

### Lab 1: Predict Future Rover Trajectories

**Objective:** Train a model to predict where the rover will be N steps in the future given current state and planned actions.

**You will learn:**
- Sequence prediction for robotics
- Temporal modeling (RNN, Transformer, or SSM)
- Evaluating prediction accuracy over time horizons

---

### Lab 2: Latent Environment Representation

**Objective:** Train an autoencoder (or VAE) to compress camera observations into a latent space, then predict transitions in latent space.

**You will learn:**
- Representation learning for robotics
- Latent dynamics models
- Information compression and reconstruction

---

### Lab 3: Predictive Navigation Planning

**Objective:** Use the learned world model to plan actions by "imagining" multiple possible futures and selecting the best trajectory.

**You will learn:**
- Model Predictive Control with learned dynamics
- Rollout-based planning in latent space
- Comparing planned vs reactive behavior

---

### Lab 4: Memory-Enabled Navigation

**Objective:** Add episodic memory to the rover — it remembers previously visited locations and uses this memory to improve future navigation decisions.

**You will learn:**
- Memory architectures for embodied agents
- Retrieval-augmented decision making
- Long-horizon task completion with memory

---

## Deliverable: Rover V6

### Capabilities

- Predictive planning (imagining futures before acting)
- Latent world model (compressed environment understanding)
- Episodic memory (remembering past experiences)
- Semantic reasoning about the environment
- Future-state estimation

### Engineering Deliverables

- [ ] World model architecture and training pipeline
- [ ] Prediction accuracy evaluation (short vs long horizon)
- [ ] Planning comparison: reactive vs predictive behavior
- [ ] Memory system design and retrieval evaluation
- [ ] Visualization of latent space and predicted futures
- [ ] GitHub repository updates

### Demo Video

**Title:** "Can a Robot Imagine the Future?"

Must explain:
- What prediction means for a robot
- How latent space representations work (intuition)
- How planning over imagined futures improves behavior
- The role of memory in embodied systems

---

## Core Lesson

> World models enable robots to think before they act.

With prediction, memory, and planning, the rover transitions from a reactive machine to something approaching cognitive behavior. It can reason about consequences, remember experiences, and choose actions based on imagined outcomes.

**This motivates the Capstone: building a complete embodied autonomous agent.**
