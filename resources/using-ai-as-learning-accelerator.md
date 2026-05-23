# How to Use AI as a Learning Accelerator (Not a Shortcut)

> The goal is to build intuition faster — not to skip building it.

---

## The Method: Predict → Attempt → Diagnose → Correct

Every lab follows this loop. AI plays the role of a patient instructor, not an answer key.

### Step 1: Wire it up (predict)

Before asking anything:
- Sketch or build what you *think* the circuit looks like in Wokwi
- Write down what you expect to happen when it runs
- This is your prediction — it can be wrong, that's the point

### Step 2: Check with AI (like showing a teacher your diagram)

Show your wiring to the AI and ask: "Is this right?"
- If wrong: ask *why*, not just *what* the fix is
- Identify the broken mental model (e.g., "I thought the pot connects directly to the LED")
- Update your understanding before moving on

### Step 3: Write/generate the code

Now that the circuit is correct:
- Predict what the code needs to do (in plain English)
- Let AI generate the implementation — syntax isn't the learning here
- Read it and make sure you can explain every line

### Step 4: Debug manually first

When something doesn't work:
- **Observe** the symptoms (LED doesn't light, serial shows 0, etc.)
- **Hypothesize** what's wrong before asking AI
- **Test** your hypothesis (change one thing, re-run)
- Only after you've tried: ask AI to confirm or redirect

### Step 5: Document the bug

Every wrong prediction is a learning moment. Write down:
- What you expected
- What actually happened
- What mental model was wrong
- The corrected understanding

---

## When AI Helps vs When It Hurts

| AI helps | AI hurts |
|----------|----------|
| Explaining *why* a circuit doesn't work | Giving you the fixed circuit without explanation |
| Generating boilerplate code after you understand the logic | Writing code you can't explain |
| Answering Socratic questions about theory | Answering questions you haven't tried to answer yourself |
| Compressing vocabulary/syntax learning | Skipping the predict → fail → correct loop |

---

## The Rule

> **Never let AI fix something you haven't tried to diagnose.**

The fix is easy. The diagnosis is where intuition lives.

---

## Practical Workflow for Each Lab

```text
1. Read the lab objective
2. Sketch the circuit (pen/paper or Wokwi) WITHOUT looking at the solution
3. Show AI your attempt → get feedback on mental model gaps
4. Correct the circuit, predict behavior
5. Run simulation → observe
6. If wrong: diagnose manually, then verify with AI
7. Document: what you predicted, what happened, what you learned
8. Move to code: describe what it should do, let AI generate, read and verify
9. Run → debug loop (same predict/diagnose pattern)
10. Write up the theory note if a deep concept surfaced
```

---

## Why This Works

- **Simple projects** (blink, LED+pot) build vocabulary — AI compresses this phase
- **Hard projects** (feedback control, state estimation) require the mental models built during simple ones
- The foundation isn't code. **The foundation is signal-flow reasoning.**
- AI handles syntax; you handle architecture

---

## Related

- [Research Journal: AI Accelerator Paradox](../research_journal/2026-05-23-ai-accelerator-paradox.md)
- [ADC, Quantization, and Signal Mapping](adc-quantization-and-mapping.md) — example of Socratic method producing theory notes
