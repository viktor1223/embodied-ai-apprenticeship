#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>

// L298N Dual H-Bridge Motor Driver
// Channels A (ENA, IN1, IN2 -> OUT1, OUT2) and B (ENB, IN3, IN4 -> OUT3, OUT4)
//
// Truth table per channel (e.g. Channel A):
//   ENA=LOW  -> OUT1, OUT2 float (motor disconnected)
//   ENA=HIGH, IN1=HIGH, IN2=LOW  -> OUT1=Vs, OUT2=0  (forward)
//   ENA=HIGH, IN1=LOW,  IN2=HIGH -> OUT1=0,  OUT2=Vs (reverse)
//   ENA=HIGH, IN1=IN2            -> OUT1=OUT2 (brake)
//
// PWM on ENA/ENB controls speed (outputs only active when enable is HIGH).

typedef struct {
  pin_t pin_ENA;
  pin_t pin_ENB;
  pin_t pin_IN1;
  pin_t pin_IN2;
  pin_t pin_IN3;
  pin_t pin_IN4;
  pin_t pin_OUT1;
  pin_t pin_OUT2;
  pin_t pin_OUT3;
  pin_t pin_OUT4;
  uint32_t Vs_attr;
} chip_state_t;

static void update_outputs(chip_state_t *chip);
static void chip_pin_change(void *user_data, pin_t pin, uint32_t value);

void chip_init(void) {
  chip_state_t *chip = malloc(sizeof(chip_state_t));

  chip->pin_ENA = pin_init("ENA", INPUT);
  chip->pin_ENB = pin_init("ENB", INPUT);
  chip->pin_IN1 = pin_init("IN1", INPUT);
  chip->pin_IN2 = pin_init("IN2", INPUT);
  chip->pin_IN3 = pin_init("IN3", INPUT);
  chip->pin_IN4 = pin_init("IN4", INPUT);
  chip->pin_OUT1 = pin_init("OUT1", ANALOG);
  chip->pin_OUT2 = pin_init("OUT2", ANALOG);
  chip->pin_OUT3 = pin_init("OUT3", ANALOG);
  chip->pin_OUT4 = pin_init("OUT4", ANALOG);

  chip->Vs_attr = attr_init_float("Vs", 12.0);

  const pin_watch_config_t watch_config = {
    .edge = BOTH,
    .pin_change = chip_pin_change,
    .user_data = chip,
  };

  pin_watch(chip->pin_ENA, &watch_config);
  pin_watch(chip->pin_ENB, &watch_config);
  pin_watch(chip->pin_IN1, &watch_config);
  pin_watch(chip->pin_IN2, &watch_config);
  pin_watch(chip->pin_IN3, &watch_config);
  pin_watch(chip->pin_IN4, &watch_config);

  printf("[L298N] Initialized. Vs=%.1fV\n", attr_read_float(chip->Vs_attr));
}

static void chip_pin_change(void *user_data, pin_t pin, uint32_t value) {
  chip_state_t *chip = (chip_state_t *)user_data;
  update_outputs(chip);
}

static void update_outputs(chip_state_t *chip) {
  int ENA = pin_read(chip->pin_ENA);
  int ENB = pin_read(chip->pin_ENB);
  int IN1 = pin_read(chip->pin_IN1);
  int IN2 = pin_read(chip->pin_IN2);
  int IN3 = pin_read(chip->pin_IN3);
  int IN4 = pin_read(chip->pin_IN4);
  float Vs = attr_read_float(chip->Vs_attr);
  int Vs_mv = (int)(Vs * 1000);

  // Channel A: gated by ENA
  if (ENA) {
    pin_dac_write(chip->pin_OUT1, IN1 ? Vs_mv : 0);
    pin_dac_write(chip->pin_OUT2, IN2 ? Vs_mv : 0);
  } else {
    pin_dac_write(chip->pin_OUT1, 0);
    pin_dac_write(chip->pin_OUT2, 0);
  }

  // Channel B: gated by ENB
  if (ENB) {
    pin_dac_write(chip->pin_OUT3, IN3 ? Vs_mv : 0);
    pin_dac_write(chip->pin_OUT4, IN4 ? Vs_mv : 0);
  } else {
    pin_dac_write(chip->pin_OUT3, 0);
    pin_dac_write(chip->pin_OUT4, 0);
  }
}
