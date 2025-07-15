# Marlin FW GCODE Reference

## G0 - Linear Move

From: https://marlinfw.org/docs/gcode/G000-G001.html

### Related Codes

- [G90 - Absolute Positioning](#g90-absolute-positioning)
- [G91 - Relative Positioning](#g91-relative-positioning)
- G2 - Arc or Circle Move
- G3 - Arc or Circle Move
- G5 - Bezier Cubic Spline Move
- M82 - E Absolute
- M83 - E Relative

### Description

The `G0` and `G1` commands add a linear move to the queue to be performed after
all previous moves are completed. These commands yield control back to the
command parser as soon as the move is queued, but they may delay the command
parser while awaiting a slot in the queue.

A linear move traces a straight line from one point to another, ensuring that
the specified axes will arrive simultaneously at the given coordinates (by
linear interpolation). The speed may change over time following an acceleration
curve, according to the acceleration and jerk settings of the given axes.

A command like `G1 F1000` sets the feedrate for all subsequent moves.

By convention, most G-code generators use `G0` for non-extrusion movements
(those without the E axis) and `G1` for moves that include extrusion. This is
meant to allow a kinematic system to, optionally, do a more rapid uninterpolated
movement requiring much less calculation.

For Cartesians and Deltas the `G0` (rapid linear movement) command is (and must
be) a direct alias for `G1` (rapid movement). On SCARA machines `G0` does a fast
non-linear move. Marlin 2.0 introduces an option to maintain a separate default
feedrate for `G0`. Note: Slicers tend to override firmware feedrates!

------

__**NOTE**__ Coordinates are given in millimeters by default. Units may be set
to inches by `G20`.

In Relative Mode (`G91`) all coordinates are interpreted as relative, adding
onto the previous position.

In Extruder Relative Mode (`M83`) the E coordinate is interpreted as relative,
adding onto the previous E position.

A single linear move may generate several smaller moves to the planner due to
kinematics and bed leveling compensation. Printing performance can be tuned by
adjusting segments-per-second.

Developers: Keep using `G0` for non-print moves. It makes G-code more adaptable
to lasers, engravers, etc.

------

### Usage

```
G0 [A<pos>] [B<pos>] [C<pos>] [E<pos>] [F<rate>] [S<power>] [U<pos>] [V<pos>] [W<pos>] [X<pos>] [Y<pos>] [Z<pos>]
G1 [A<pos>] [B<pos>] [C<pos>] [E<pos>] [F<rate>] [S<power>] [U<pos>] [V<pos>] [W<pos>] [X<pos>] [Y<pos>] [Z<pos>] 
```

| Parameters      | Description                                                            |
| ----------      | -----------                                                            |
| [A\<pos\>]      | An absolute or relative coordinate on the A axis (in current units)    |
| [B\<pos\>]      | An absolute or relative coordinate on the B axis (in current units)    |
| [C\<pos\>]      | An absolute or relative coordinate on the C axis (in current units)    |
| [E\<pos\>]      | An absolute or relative coordinate on the E axis (in current units)    |
| [U\<pos\>]      | An absolute or relative coordinate on the U axis (in current units)    |
| [V\<pos\>]      | An absolute or relative coordinate on the V axis (in current units)    |
| [W\<pos\>]      | An absolute or relative coordinate on the W axis (in current units)    |
| [X\<pos\>]      | An absolute or relative coordinate on the X axis (in current units)    |
| [Y\<pos\>]      | An absolute or relative coordinate on the Y axis (in current units)    |
| [Z\<pos\>]      | An absolute or relative coordinate on the Z axis (in current units)    |
| [F\<rate\>]     | Set the requested movement rate for this move and any following moves  |
| [S\<power\>]    | Set the laser power for the move                                       |

### Examples

Move to 12mm on the X axis:

```
G0 X11
```

Set the feedrate to 1500 mm/min:

```
G0 F1500
```

Move to 90.6mm on the X axis and 12.8mm on the Y axis:

```
G0 X90.6 Y12.8
```

## G90 - Absolute Positioning

From: https://marlinfw.org/docs/gcode/G090.html

### Description

In absolute mode all coordinates given in G-code are interpreted as positions in
the logical coordinate space. This includes the extruder position unless
overridden by `M83 - E Relative`.

__**NOTE**__ Absolute positioning is the default.

### Example

Enable Absolute Mode:

```
G90
```

## G91 - Relative Positioning

### Description

Set relative position mode. In this mode all coordinates are interpreted as
relative to the last position. This includes the extruder position unless
overridden by `M82 - E Absolute`.

### Example

Enable Relative Mode:

```
G91
```

## G4 - Dwell

From: https://marlinfw.org/docs/gcode/G004.html

### Related Codes

- [M400 - Finish Moves](#m400-finish-moves)

### Description

Dwell pauses the command queue and waits for a period of time.

------

__**NOTE**__: If both S and P are included, S takes precedence.

M0/M1 provides an interruptible “dwell” (Marlin 1.1.0 and up).

G4 with no arguments is effectively the same as M400.

------

### Usage

``` 
G4 [P<time(ms)>] [S<time(sec)>]
```

| Parameters       | Description                   |
| ----------       | -----------                   |
| [P\<time(ms)\>]  | Amount of time to dwell (ms)  | 
| [S\<time(sec)\>] | Amount of time to dwell (sec) |

### Example

Dwell for 500 milliseconds:

```
G4 P500
```

## G28 - Auto Home

From: https://marlinfw.org/docs/gcode/G028.html

### Description

When you first start up your machine it has no idea where the toolhead is
positioned, so Marlin needs to use a procedure called "homing" to establish a
known position. To do this it moves each axis towards one end of its track until
it triggers a switch, commonly called an "endstop." Marlin knows where the
endstops are, so once all the endstops have been triggered the position is
known.

The `G28` command is used to home one or more axes. The default behavior with no
parameters is to home all axes.

In order to improve positional accuracy, the homing procedure can re-bump at a
slower speed according to the `[XYZ]_HOME_BUMP_MM` and `HOMING_BUMP_DIVISOR`
settings.

The position is easy to lose when the steppers are turned off, so homing may be
required or advised after the machine has been sitting idle for a period of
time. See the Configuration files for all homing options.

------

__**NOTE**__ Homing is required before `G29 - Bed Leveling`, `M48 - Probe
Repeatability test`, and some other procedures.

If homing is needed the LCD will blink the X Y Z indicators.

By default G28 disables bed leveling. Follow with `M420 - Bed Leveling State` 
to turn leveling on.

- With `ENABLE_LEVELING_AFTER_G28` leveling will always be enabled after `G28`.
- With `RESTORE_LEVELING_AFTER_G28` leveling is restored to whatever state it
  was in before `G28`.

------

### Usage

```
G28 [A] [B] [C] [L] [O] [R] [U] [V] [W] [X] [Y] [Z]
```

| Parameters      | Description                                                            |
| ----------      | -----------                                                            |
| [A]             | Flag to home the A Axis.                                               |
| [B]             | Flag to home the B Axis.                                               |
| [C]             | Flag to home the C Axis.                                               |
| [U]             | Flag to home the U Axis.                                               |
| [V]             | Flag to home the V Axis.                                               |
| [W]             | Flag to home the W Axis.                                               |
| [X]             | Flag to home the X Axis.                                               |
| [Y]             | Flag to home the Y Axis.                                               |
| [Z]             | Flag to home the Z Axis.                                               |
| [L]             | Flag to restore bed leveling state after homing. (default true)        |
| [O]             | Flag to skip homing if the position is already trusted                 |
| [R\<mm\>]       | Distance to raise the nozzle before homing (in mm)                     |

### Example

The most-used form of this command is to home all axes:

``` 
G28
```

Home the X and Z axes:

```
G28 X Z
```

Home all the "untrusted" axes:

``` 
G28 O
```

## M400 - Finish Moves

From: https://marlinfw.org/docs/gcode/M400.html

### Related Codes

- [G4 - Dwell](#g4-dwell)

### Description

This command causes G-code processing to pause and wait in a loop until all
moves in the planner are completed.

### Example

Wait for moves to finish and play a tone:

```
M400
M300 S440 P100
```

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

## M510 - Lock Machine

From: https://marlinfw.org/docs/gcode/M510.html

### Related Codes

- [511 - Unlock Machine](#511-unlock-machine)
- [512 - Set Passcode](#512-set-passcode)

### Description

Lock the machine. When the machine is locked a passcode is required to unlock
it. Use `M511 P<Password>` with your passcode to unlock the machine.

### Example

Lock the machine now:

``` 
M510
```

## M511 - Unlock Machine

From: https://marlinfw.org/docs/gcode/M511.html

### Related Codes

- [510 - Lock Machine](#m510-lock-machine)
- [512 - Set Passcode](#512-set-passcode)

### Description

Check the given passcode and unlock the machine if it is correct. Otherwise,
delay for a period of time before allowing another attempt.

### Usage

```
M511 P<passcode>
```

| Parameters      | Description                                               |
| ----------      | -----------                                               |
| [P\<Password\>] | Passcode to try                                           |

### Example

Unlock a machine with passcode "12345":

```
M511 P12345
```

## M512 - Set Passcode

From: https://marlinfw.org/docs/gcode/M512.html

### Related Codes

- [510 - Lock Machine](#m510-lock-machine)
- [511 - Unlock Machine](#511-unlock-machine)

### Description

Check the passcode given with P and if it is correct clear the passcode. If a
new passcode is given with S then set a new passcode.

------

__**NOTE**__: Requires PASSWORD_FEATURE.

Use PASSWORD_LENGTH to configure the length, up to 9 digits.

------

### Usage 

```
M512 P<password> [S<password>]
```

| Parameters      | Description                                                            |
| ----------      | -----------                                                            |
| [P\<Password\>] | Current passcode. This must be correct to clear or change the passcode |
| [S\<Password\>] | If `S` is included the new passcode will be set to this value          |

### Example

Change passcode from "1234" to "9090":

```
M512 P1234 S9090
```

