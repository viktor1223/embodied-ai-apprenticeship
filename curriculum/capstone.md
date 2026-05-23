# Capstone: Embodied Autonomous Agent Platform

> Full integration of perception, memory, planning, prediction, action, and learning.

**Duration:** Open-ended (research project)
**Deliverable:** Rover V7/V8 — Research-Grade Embodied AI Platform
**Prerequisite:** All previous courses

---

## Objective

Develop a research-grade embodied robotics platform capable of:

- Perception (vision, proprioception, environmental sensing)
- Memory (episodic and semantic)
- Planning (hierarchical, predictive)
- Prediction (world model-based future reasoning)
- Action (learned policies, adaptive control)
- Learning (continuous improvement from experience)

---

## Required Systems

### Core Architecture

| System | Description |
|--------|-------------|
| Real-time perception | Camera + sensor fusion running at control frequency |
| Telemetry logging | Full state recording for replay and analysis |
| Modular architecture | Swappable components (perception, planning, control) |
| Embodied memory | Store and retrieve past experiences for decision-making |
| Predictive planning | World model-based trajectory evaluation |
| Action policies | Learned behaviors with fallback safety controllers |

---

## Research Requirement

The capstone has a research component. You must:

1. **Reproduce** one modern embodied AI paper on your platform
2. **Extend or modify** it experimentally (new environment, architecture change, ablation study, or novel application)

### Suggested Papers for Reproduction

- RT-1 / RT-2 (scaled robotic learning)
- Diffusion Policy (denoising for action generation)
- PaLM-E (embodied language models)
- Dreamer v3 (world model RL)
- OpenVLA (open vision-language-action)
- Any relevant paper from CoRL, RSS, ICRA, or NeurIPS robotics track

---

## Public Deliverables

### Required Artifacts

- [ ] **GitHub repository** — complete codebase with documentation
- [ ] **Architecture documentation** — system design, interfaces, data flow
- [ ] **Engineering notebook** — decisions, tradeoffs, iterations
- [ ] **System diagrams** — hardware, software, and data architecture
- [ ] **Evaluation metrics** — quantitative performance measurements
- [ ] **Failure analysis** — what broke, why, and how it was resolved
- [ ] **Demo videos** — showing system capabilities and limitations

---

## Final Demo Video

**Title:** "Building an Embodied AI Robot from Scratch"

This video documents the entire journey. It must cover:

- The full progression from Course 101 through the Capstone
- Key failures and what they taught
- Redesigns and architectural pivots
- The evolution of autonomy across rover versions
- The transition from control → perception → learning → cognition

---

## Evaluation Criteria

The capstone is successful if the platform demonstrates:

| Criterion | Evidence |
|-----------|----------|
| Perception works in real-time | FPS metrics, latency measurements |
| Memory improves performance | With/without memory comparison |
| Planning outperforms reactive | Side-by-side behavior comparison |
| System is modular | Swapping one component doesn't break others |
| Research paper is reproduced | Quantitative results comparison |
| Extension adds novelty | Clear description of what's new |

---

## Guiding Principle

> Each course exists because the previous approach failed.

The capstone integrates everything. It proves that the full stack — from motor control to world models — is not a collection of independent techniques, but a coherent progression toward embodied intelligence.
