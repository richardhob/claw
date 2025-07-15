# Planning 2025-07-11

Let's finish our investigation of the firmware and make a plan for the claw
game.

## UI

The User interface seems to be managed by `Marlin/src/lcd/marlinui.cpp`

## Features we could exploit

- Joy stick (Do we have the pins?)
- Disable SD Card
- Enable Serial
- Disable Heaters?
- Disable 

## Goal of this project

Make a Claw game, which can be coin operated (eventually). Features are as
follows:

- Button to say start 
- Count down timer on start
- Button to say "go" (can be same as start button)
- Joystick to control position

I think this can work by:

1. Removing Thermistor connections (I think they're analog / ADC In connections)
2. Connecting up a joy stick 

Pretty simple?

## Joystick

Using an analog joystick, we can control the printer:

``` cpp
//#define JOYSTICK
#if ENABLED(JOYSTICK)
  #define JOY_X_PIN    5  // RAMPS: Suggested pin A5  on AUX2
  #define JOY_Y_PIN   10  // RAMPS: Suggested pin A10 on AUX2
  #define JOY_Z_PIN   12  // RAMPS: Suggested pin A12 on AUX2
  #define JOY_EN_PIN  44  // RAMPS: Suggested pin D44 on AUX2
  //#define INVERT_JOY_X  // Enable if X direction is reversed
  //#define INVERT_JOY_Y  // Enable if Y direction is reversed
  //#define INVERT_JOY_Z  // Enable if Z direction is reversed
  // Use M119 with JOYSTICK_DEBUG to find reasonable values after connecting:
  #define JOY_X_LIMITS { 5600, 8190-100, 8190+100, 10800 } // min, deadzone start, deadzone end, max
  #define JOY_Y_LIMITS { 5600, 8250-100, 8250+100, 11000 }
  #define JOY_Z_LIMITS { 4800, 8080-100, 8080+100, 11550 }
#endif
```

The thermister inputs are ADC inputs, so that should "just work." I think the
joy stick requires a 5V input:

![Joy Stick Module](images/Joystick-Module-Pinout.png)

