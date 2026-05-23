# Research Journal: The AI Accelerator Paradox

**Date:** 2026-05-23
**Context:** Setting up 101 labs, working through first Arduino circuits

---

## The Tension

I can use an LLM to generate code and wire circuits instantly. The beginner projects are simple enough that I don't *need* to build them manually. But I'm worried this skips the foundation-building that makes harder things possible later.

## What I Actually Learned Today (Without "Building")

The potentiometer exercise exposed a broken mental model:

> I assumed components connect directly to each other (pot → LED).
> The real model: **everything routes through the microcontroller.** Inputs go in, outputs go out, the Arduino is the brain in between.

This is a genuine insight. I didn't need to solder anything to get it — I needed to *wire it wrong* in Wokwi and then ask "why doesn't this work?"

## Emerging Mental Model: Input → Processing → Output

```text
[Sensors / Input Devices]
        ↓
   (analog/digital pins)
        ↓
  [Microcontroller — the decision-maker]
        ↓
   (PWM / digital pins)
        ↓
[Actuators / Output Devices]
```

**Open question:** There are components *between* the Arduino and the I/O devices (resistors, capacitors, motor drivers). These seem to be passive or amplifying — they don't make decisions, they condition signals. I need to understand when and why these exist.

## Reframing: What Does "Building Intuition" Actually Require?

It's not about typing code or wiring by hand. It's about:

1. **Predicting** what will happen before running it
2. **Being wrong** and understanding why
3. **Updating the mental model** based on the failure

All three happened today without writing a single line of code myself:
- I predicted pot → LED directly
- I was wrong (nothing worked)
- I updated: everything routes through the MCU

## How to Use AI Without Losing the Foundation

The risk isn't that AI writes code for me. The risk is that I **never make predictions and never fail.**

Rules for myself:
- Before asking AI to build something: **draw what I think the circuit looks like**
- Before running a simulation: **predict what will happen**
- When it doesn't work: **diagnose before asking for the fix**
- AI handles syntax/boilerplate; I handle architecture/signal-flow reasoning

## Where This Gets Interesting

The simple projects (blink, LED+pot) aren't where I need deep struggle. They're vocabulary-building. The AI accelerator becomes dangerous if I skip to complex systems without this vocabulary. But it becomes powerful if I use it to compress the vocabulary phase and spend more time on the hard stuff:

- Feedback loops (102)
- State estimation under noise (201)
- Learned policies (301)

**The foundation isn't code. The foundation is the mental model of signal flow.**

---

## Action Items

- [ ] For each remaining 101 lab: sketch the circuit *before* looking at the answer
- [ ] Predict what each pin does before reading the code
- [ ] Document every wrong prediction — those are the actual learning moments
- [ ] Don't feel guilty about AI-generated code; feel guilty about AI-generated *understanding*
