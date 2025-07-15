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

## M300 - Play Tone

From: https://marlinfw.org/docs/gcode/M300.html

### Description

Add a tone to the tone queue.

------

__**NOTE**__ Requires SPEAKER to play tones (not just beeps).

In Marlin 1.0.2, playing tones block the command queue. Marlin 1.1.0 uses a tone
queue and background tone player to keep the command buffer from being blocked
by playing tones.

------

### Usage

``` 
M300 [P<ms>] [S<Hz>]
```

| Parameters | Description                                      |
| ---------- | -----------                                      |
| [P\<ms\>]  | Duration (in ms)                                 |
| [S\<Hz\>]  | Frequency (in Hz)                                |

### Example

Play a short tune:

```
M300 S440 P200
M300 S660 P250
M300 S880 P300
```

Breakdown:

- `M300 S440 P200` -> S400 -> 440 Hz for 200 ms
- `M300 S660 P250` -> S660 -> 660 Hz for 250 ms
- `M300 S880 P300` -> S880 -> 880 Hz for 300 ms

## M226 - Wait for Pin State

From: https://marlinfw.org/docs/gcode/M226.html

### Related Codes

- [M42 - Set Pin State](#m42-set-pin-state)

### Description

Wait for a pin to have a certain value or state.

### Usage

```
M226 P<pin> [S<state>] 
```

| Parameters   | Description                                      |
| ----------   | -----------                                      |
| [P\<pin\>]   | Pin Number                                       |
| [S\<State\>] | State 0 or 1. Default to (-1) for inverted       |

## M42 - Set Pin State

From: https://marlinfw.org/docs/gcode/M042.html

### Related Codes

- [M226 - Wait for Pin State](#m226---wait-for-pin-state)

### Description

For custom hardware not officially supported in Marlin, you can often just
connect up an unused pin and use M42 to control it.

### Usage

```
M42 [I<bool>] [P<pin>] S<state> [T<0|1|2|3>]
```

| Parameters     | Description                                                    |
| ----------     | -----------                                                    |
| [I\<bool\>]    | Ignore protection on pins that Marlin is using                 |
| [P\<pin\>]     | Pin Number. `LED_PIN` is used by default                       |
| [S\<State\>]   | State 0 or 1. PWM pins may be set from 0 to 255 for duty cycle |
| [T\<0|1|2|3\>] | Set the pin mode.                                              |

Pin Mode Options:

- T0: Input
- T1: Output
- T2: Input Pull Up
- T3: Input Pull Down

### Examples

Turn `LED_PIN` on:

```
M42 S1
```

Turn on pin 33:

```
M42 P33 S1
```

Set PWM (pin 44) to output with 50% duty cycle:

```
M43 P44 S128
```

## Set Passcode

From: https://marlinfw.org/docs/gcode/M512.html

### Related Codes

- 

https://marlinfw.org/docs/gcode/M512.html

### Description

Check the passcode given with P and if it is correct clear the passcode. If a
new passcode is given with S then set a new passcode.

------

__**NOTE**__: Requires PASSWORD_FEATURE.

Use PASSWORD_LENGTH to configure the length, up to 9 digits.

------

### Usage 
