# ADC, Quantization, and Signal Mapping

> Socratic Q&A session while reading the Arduino [AnalogInOutSerial](https://docs.arduino.cc/built-in-examples/analog/AnalogInOutSerial/) example.
> Demonstrates using AI as a study partner to interrogate documentation rather than passively reading it.

---

## Method: Socratic Learning with AI

Instead of reading documentation linearly, ask questions about every assumption:

1. **Notice something you don't understand** (why 0–1023?)
2. **State your current hypothesis** (I expected 0–255 because 8-bit)
3. **Ask AI to challenge or confirm it** (is that right? why not?)
4. **Follow up until the root concept is exposed** (ADC resolution, quantization)

This turns passive reading into active reasoning.

---

## Core Questions and Insights

### 1. Why does `analogRead()` return 0–1023 (not 0–255)?

**Initial intuition:** Expected 0–255 because I was thinking in 8-bit terms.

**Insight:**

- Arduino uses a **10-bit ADC**, not 8-bit
- A 10-bit system gives: $2^{10} = 1024$ values, so range is 0 to 1023

The range is determined by **ADC resolution**, not arbitrary design.

---

### 2. What is actually happening during `analogRead()`?

**Refined understanding:**

- Real-world input = continuous voltage (e.g., 0–5V)
- The ADC divides this range into discrete steps and assigns each step an integer value

```text
analog voltage → quantized level → integer (0–1023)
```

The ADC is performing **quantization**, not just "reading a value."

---

### 3. Does this pattern generalize beyond Arduino?

**Yes — this is universal to ADCs.**

General rule: range = $0$ to $2^N - 1$

| Resolution | Range |
|-----------|-------|
| 8-bit | 0–255 |
| 10-bit | 0–1023 |
| 12-bit | 0–4095 |
| 16-bit | 0–65535 |

This is **not Arduino-specific** — it's fundamental to digital signal representation.

---

### 4. Why 10 bits instead of 8 or 16?

**Engineering tradeoffs:**

- More bits → higher precision
- But also: more noise sensitivity, higher cost/complexity, slower conversion

10-bit is a **practical engineering compromise** for general microcontroller use.

---

### 5. What does `map()` do — is it converting back to real values?

**Initial hypothesis:** Maybe `map()` converts digital values back into physical values.

**Correction:**

- `map()` does NOT convert to voltage or physical units
- It simply rescales one numeric range to another

```cpp
map(val, 0, 1023, 0, 255);
// "express position within one range in terms of another range"
```

`map()` is **linear interpolation**, not physical conversion.

---

### 6. How do you actually convert to real voltage?

```cpp
float voltage = reading * (Vref / 1023.0);
```

- This incorporates **system physics (Vref)**
- Unlike `map()`, this produces a real-world scalar

---

## Final Mental Model

```text
Physical World
   ↓
(voltage signal)
   ↓
ADC (quantization into 2^N levels)
   ↓
integer value (e.g., 0–1023)
   ↓
[Option A] map() → different discrete range (e.g., PWM 0–255)
[Option B] formula → physical value (e.g., volts)
```

---

## Key Conceptual Shift

> The number from `analogRead()` is not a voltage —
> it is a **scaled integer representation of a ratio relative to Vref**.

---

## Connection to Lab 1

In the AnalogInOutSerial example:

1. `analogRead(A0)` → reads pot position (0–1023)
2. `map(sensorValue, 0, 1023, 0, 255)` → scales to PWM range
3. `analogWrite(9, outputValue)` → drives LED brightness

Understanding this pipeline explains *why those specific ranges are used* and how data flows through the system.

---

## Related Courses

- **101 — Physical Embodiment:** Lab 1 (LED brightness with potentiometer)
- **102 — Feedback Control:** ADC readings as sensor feedback
- **201 — State Estimation:** Quantization noise and measurement uncertainty
