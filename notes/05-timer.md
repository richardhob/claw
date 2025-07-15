# Generic Timer

We can potentially use the PWM for the FAN for the timer, by settings the
`FAST_PWM_FAN` frequency:

## Fast PWM Fan Frequency Scaling

PWM Fan Scaling

Define the min/max speeds for PWM fans (as set with `M106`).

With these options the `M106` 0-255 value range is scaled to a subset to ensure
that the fan has enough power to spin, or to run lower current fans with higher
current. (e.g., 5V/12V fans with 12V/24V) Value 0 always turns off the fan.

Define one or both of these to override the default 0-255 range.

- `FAN_MIN_PWM` -> Example provided is 50
- `FAN_MAX_PWM` -> Example provided is 128

We can override the PWM frequency by defining:

- `FAST_PWM_FAN` -> Enable this feature
- `FAST_PWM_FAN_FREQUENCY` -> Set the desired Frequency

This is typically written in the `Configuration_adv.h` file.

The PWM "ON" time starts on T0 according to the Arduino Tutorial on PWMs:

    https://docs.arduino.cc/tutorials/generic/secrets-of-arduino-pwm/

Considering that we are restricted on the Frequency available....

## Fan FAST PWM

Combinations of PWM Modes, prescale values and TOP resolutions are used internally
to produce a frequency as close as possible to the desired frequency.

### FAST_PWM_FAN_FREQUENCY

Set this to your desired frequency.

For AVR, if left undefined this defaults to:

$$ F = F_CPU/(2*255*1) $$

Typically:

- $F = 31.4kHz$ on 16MHz micro-controllers 
- $F = 39.2kHz$ on 20MHz micro-controllers.

For non AVR, if left undefined this defaults to F = 1Khz.

This F value is only to protect the hardware from an absence of configuration
and not to complete it when users are not aware that the frequency must be
specifically set to support the target board.

------

__**NOTE**__  Setting very low frequencies (< 10 Hz) may result in unexpected
timer behavior. Setting very high frequencies can damage your hardware.

------

### USE_OCR2A_AS_TOP [undefined by default]

Boards that use TIMER2 for PWM have limitations resulting in only a few possible frequencies on TIMER2:

- 16MHz MCUs: [62.5kHz, 31.4kHz (default), 7.8kHz, 3.92kHz, 1.95kHz, 977Hz, 488Hz, 244Hz, 60Hz, 122Hz, 30Hz]
- 20MHz MCUs: [78.1kHz, 39.2kHz (default), 9.77kHz, 4.9kHz, 2.44kHz, 1.22kHz, 610Hz, 305Hz, 153Hz, 76Hz, 38Hz]

A greater range can be achieved by enabling `USE_OCR2A_AS_TOP`. But note that
this option blocks the use of PWM on pin OC2A. Only use this option if you don't
need PWM on 0C2A. (Check your schematic.) `USE_OCR2A_AS_TOP` sacrifices duty
cycle control resolution to achieve this broader range of frequencies.
