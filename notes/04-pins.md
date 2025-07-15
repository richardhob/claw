# Pins

We need to override a few defaults from the Creality bits:

1. Change the Extruder Temperature Sensor pin into a Joystick Input 
2. Change the Bed Temperature Sensor pin into a Joystick Input 
3. Change the Extruder Fan pin into a custom button pin
4. Find ANOTHER pin to use as the DROP pin (MOSI? MISO? SCK?)

Comments from `Marlin/src/pins/sanguino/pins_MELZI_CREALITY.h`:

``` cpp
/**
  PIN:   0   Port: B0        E0_DIR_PIN       protected
  PIN:   1   Port: B1        E0_STEP_PIN      protected
  PIN:   2   Port: B2        Z_DIR_PIN        protected
  PIN:   3   Port: B3        Z_STEP_PIN       protected
  PIN:   4   Port: B4        AVR_SS_PIN       protected
  .                          FAN0_PIN         protected
  .                       SD_SS_PIN           protected
  PIN:   5   Port: B5        AVR_MOSI_PIN     Output = 1
  .                       SD_MOSI_PIN         Output = 1
  PIN:   6   Port: B6        AVR_MISO_PIN     Input  = 0    TIMER3A   PWM:     0    WGM: 1    COM3A: 0    CS: 3    TCCR3A: 1    TCCR3B: 3    TIMSK3: 0
  .                       SD_MISO_PIN         Input  = 0
  PIN:   7   Port: B7        AVR_SCK_PIN      Output = 0    TIMER3B   PWM:     0    WGM: 1    COM3B: 0    CS: 3    TCCR3A: 1    TCCR3B: 3    TIMSK3: 0
  .                       SD_SCK_PIN          Output = 0
  PIN:   8   Port: D0        RXD              Input  = 1
  PIN:   9   Port: D1        TXD              Input  = 0
  PIN:  10   Port: D2        BTN_EN2          Input  = 1
  PIN:  11   Port: D3        BTN_EN1          Input  = 1
  PIN:  12   Port: D4        HEATER_BED_PIN   protected
  PIN:  13   Port: D5        HEATER_0_PIN     protected
  PIN:  14   Port: D6        E0_ENABLE_PIN    protected
  .                          X_ENABLE_PIN     protected
  .                          Y_ENABLE_PIN     protected
  PIN:  15   Port: D7        X_STEP_PIN       protected
  PIN:  16   Port: C0        BTN_ENC          Input  = 1
  .                          SCL              Input  = 1
  PIN:  17   Port: C1        LCD_PINS_EN      Output = 0
  .                          SDA              Output = 0
  PIN:  18   Port: C2        X_MIN_PIN        protected
  .                          X_STOP_PIN       protected
  PIN:  19   Port: C3        Y_MIN_PIN        protected
  .                          Y_STOP_PIN       protected
  PIN:  20   Port: C4        Z_MIN_PIN        protected
  .                          Z_STOP_PIN       protected
  PIN:  21   Port: C5        X_DIR_PIN        protected
  PIN:  22   Port: C6        Y_STEP_PIN       protected
  PIN:  23   Port: C7        Y_DIR_PIN        protected
  PIN:  24   Port: A7        TEMP_0_PIN       protected
  PIN:  25   Port: A6        TEMP_BED_PIN     protected
  PIN:  26   Port: A5        Z_ENABLE_PIN     protected
  PIN:  27   Port: A4        BEEPER_PIN       Output = 0
  PIN:  28   Port: A3        LCD_PINS_RS      Output = 0
  PIN:  29   Port: A2        <unused/unknown> Input  = 0
  PIN:  30   Port: A1        LCD_PINS_D4      Output = 1
  PIN:  31   Port: A0        SDSS             Output = 1
*/
```

From `pins_SANGUINOLOLU_11.h`:

``` cpp
//
// Temperature Sensors
//
#define TEMP_0_PIN                             7  // Analog Input (pin 33 extruder)
#define TEMP_BED_PIN                           6  // Analog Input (pin 34 bed)

//
// Heaters / Fans
//
#define HEATER_0_PIN                          13  // (extruder)
```

From `pins_SANGUINOLOLU_12.h`:

``` cpp
#define HEATER_BED_PIN                        12  // (bed)

#if !defined(FAN0_PIN) && ENABLED(LCD_I2C_PANELOLU2)
  #define FAN0_PIN                             4  // Uses Transistor1 (PWM) on Panelolu2's Sanguino Adapter Board to drive the fan
#endif
```

From `pins_MELZI_CREALITY.h`: (NONE)

From `pins_MELZI.h`:

``` cpp
#ifndef FAN0_PIN
  #define FAN0_PIN                             4
#endif
```

## Definitions

With this information in mind, we can use the following pins:

- Joystick X: 7 (Extruder Temp Sensor Pin)
- Joystick Y: 6 (Bed Temp Sensor Pin)
- Custom Button 1: 4 (Extruder Fan Pin)
- Custom Button 2: 30? 28? 17?
- Servo Pin 1: 12 (Bed Heater Pin)
- Servo Pin 2: 13 (Extruder Heater Pin)

Note that the LCD Buttons are:

- `#define BTN_ENC                    EXP1_02_PIN // 16`
- `#define BTN_EN1                    EXP1_03_PIN // 11`
- `#define BTN_EN2                    EXP1_05_PIN // 10`
- `#define BEEPER_PIN                 EXP1_01_PIN // 27`

It looks like Arduino does the Analog pins first in numbering (pins 0-8 are
typically Analog inputs)... which means that the package pin doesn't correspond
with the pin number. Which is Fine. Totally fine - it would be nice if there was
a better look up table? That's probably why the provided the one in the header
file, but it would be nice to include the arduino pin number in addittion to the
package pin number.

