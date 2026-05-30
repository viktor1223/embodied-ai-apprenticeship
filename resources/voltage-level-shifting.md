---
title: Voltage Level Shifting
description: Theory and techniques for safely connecting devices that operate at different logic voltages
ms.date: 2026-05-30
keywords:
  - voltage divider
  - level shifting
  - 3.3V
  - 5V
  - GPIO safety
---

## The Problem

Different devices operate at different logic voltages. Common levels:

| Voltage | Devices |
|---------|---------|
| 5V | Arduino Uno, HC-SR04, many legacy sensors |
| 3.3V | Raspberry Pi, ESP32, most modern MCUs |
| 1.8V | Some ARM processors, FPGA I/O banks |

When a 5V output connects to a 3.3V input, the receiving chip sees a voltage above its maximum rating. This can damage or destroy the input pin, sometimes immediately, sometimes as gradual degradation.

The reverse (3.3V output to 5V input) usually works because most 5V devices treat anything above ~2V as logic HIGH. But check the datasheet for the specific device's minimum HIGH voltage ($V_{IH}$).

## Resistor Voltage Divider

The simplest level shifter for **unidirectional, slow signals** (under ~1MHz).

```text
V_high ─── R1 ───┬──► V_out (to 3.3V input)
                  │
                 R2
                  │
                 GND
```

$$V_{out} = V_{in} \times \frac{R2}{R1 + R2}$$

### Choosing Resistor Values

For 5V → 3.3V: you need $\frac{R2}{R1 + R2} = \frac{3.3}{5} = 0.66$

Common choices:

| R1 | R2 | Actual $V_{out}$ | Notes |
|----|----|--------------------|-------|
| 1kΩ | 2kΩ | 3.33V | Standard, easy to find |
| 1kΩ | 2.2kΩ | 3.44V | Slightly high, but within 3.3V tolerance |
| 10kΩ | 20kΩ | 3.33V | Lower current draw, but slower response |

### Limitations

* **Unidirectional only**: signal flows one way (high → low)
* **Speed limited**: the resistors and parasitic capacitance form an RC filter. Fine for the HC-SR04 (~40kHz ultrasonic, but the echo pulse is slow), too slow for SPI or fast I2C
* **Not for power**: this dissipates energy as heat. It's for signal lines, not power rails

## When to Use What

| Scenario | Method |
|----------|--------|
| Slow signal, one direction (HC-SR04 Echo) | Resistor voltage divider |
| Bidirectional signal (I2C between 3.3V and 5V devices) | MOSFET level shifter module (e.g., BSS138-based) |
| Fast signal (SPI, UART > 1MHz) | Dedicated level shifter IC (e.g., TXB0108) |
| Power rail conversion | Voltage regulator (LDO or switching), never resistor dividers |

## Connection to Course 101

The potentiometer in Lab 1 is a variable voltage divider. Turning the knob changes the ratio between the upper and lower resistance, producing a variable voltage at the wiper. A fixed resistor voltage divider is the same circuit with the ratio locked in place.

## Connection to Course 102

In feedback control, sensor signals flow into the controller. If your sensor operates at a different voltage than your MCU, level shifting is part of the signal conditioning chain: raw sensor output → level shift → ADC or digital input → control algorithm → actuator output.
