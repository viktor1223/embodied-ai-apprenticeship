#include "wokwi-api.h"
#include <stdio.h>
#include <stdlib.h>

// DC Motor simulation chip
// Reads analog voltage on TERM1 and TERM2, computes differential,
// and prints direction + approximate speed to the Wokwi debug console.
//
// In a real circuit: TERM1 and TERM2 connect to L298N OUT1/OUT2 (or OUT3/OUT4).
// Voltage differential determines direction and magnitude determines speed.

typedef struct {
  pin_t pin_term1;
  pin_t pin_term2;
  uint32_t ratedV_attr;
  uint32_t timer_id;
  int last_direction;  // -1, 0, 1
  int last_speed_pct;
} chip_state_t;

static void motor_timer_callback(void *user_data);

void chip_init(void) {
  chip_state_t *chip = malloc(sizeof(chip_state_t));

  chip->pin_term1 = pin_init("TERM1", ANALOG);
  chip->pin_term2 = pin_init("TERM2", ANALOG);
  chip->ratedV_attr = attr_init_float("ratedV", 12.0);
  chip->last_direction = 0;
  chip->last_speed_pct = 0;

  // Poll motor state every 100ms (simulated time)
  const timer_config_t timer_cfg = {
    .callback = motor_timer_callback,
    .user_data = chip,
  };
  chip->timer_id = timer_init(&timer_cfg);
  timer_start(chip->timer_id, 100000, true);  // 100ms, repeating

  printf("[DC Motor] Initialized. Rated voltage: %.0fV\n",
         attr_read_float(chip->ratedV_attr));
}

static void motor_timer_callback(void *user_data) {
  chip_state_t *chip = (chip_state_t *)user_data;

  // Read voltages in millivolts
  float v1 = pin_adc_read(chip->pin_term1) / 1000.0;
  float v2 = pin_adc_read(chip->pin_term2) / 1000.0;
  float diff = v1 - v2;
  float ratedV = attr_read_float(chip->ratedV_attr);

  int direction = 0;
  if (diff > 0.5) direction = 1;       // forward
  else if (diff < -0.5) direction = -1; // reverse

  float abs_diff = diff < 0 ? -diff : diff;
  int speed_pct = (int)((abs_diff / ratedV) * 100);
  if (speed_pct > 100) speed_pct = 100;

  // Only print when state changes to avoid flooding console
  if (direction != chip->last_direction || 
      abs(speed_pct - chip->last_speed_pct) > 5) {
    if (direction == 0) {
      printf("[DC Motor] STOPPED\n");
    } else {
      printf("[DC Motor] %s @ %d%% speed (%.1fV across terminals)\n",
             direction > 0 ? "FORWARD" : "REVERSE",
             speed_pct, abs_diff);
    }
    chip->last_direction = direction;
    chip->last_speed_pct = speed_pct;
  }
}
