# Planning 2025-07-11

Let's finish our investigation of the firmware and make a plan for the claw
game.

## Goal of this project

Make a Claw game, which can be coin operated (eventually). Features are as
follows:

- Button to say start 
- Count down timer on start? (May require a custom hardware / software solution)
- Button to say "grab" (can be same as start button)
- Joystick to control position

I think this can work by:

1. Removing Thermistor connections (I think they're analog / ADC In connections)
2. Connecting up a joy stick to the removed thermistor connections
3. Connect a button to the Extruder Fan Pin (Start Button)
4. Connect a button to the CPU Fan Pin (Drop Button)

### Joystick

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

The Joy stick pins are as follows:

| Pin | Description                       |
| --- | -----------                       |
| GND | Ground Connection                 |
| VCC | Voltage                           |
| VRx | X output from Potentiometer       |
| VRy | Y output from Potentiometer       |
| SW  | Internal Switch output            |

The `VRx` and `VRy` output are from Potentiometers. We should be able to figure
out what pins they are using a DMM.

### Custom Buttons

From [Stack Overflow](https://3dprinting.stackexchange.com/questions/18015/how-to-add-custom-physical-buttons-to-a-3d-printer-in-marlin-software):

Modern versions of Marlin (as of 2021) actually has built-in support for this
feature, using the Custom User Menu Buttons configuration items in
configuration_adv.h! Using the `#define CUSTOM_USER_BUTTONS` configuration
options, you can enable up to 25 hardware buttons, and configure each with
custom G-Code to implement the functionality you want.

One of the examples included in the default `configuration_adv.h` is actually
just about exactly what you asked about, starting preheating for one of the
preset filaments when enabled. Simply uncomment the first of the following lines
in the configuration file, and choose a hardware button to use.

``` cpp
#define CUSTOM_USER_BUTTONS
#define BUTTON1_PIN -1 // Set to the actual pin number
#define BUTTON2_PIN -1 // Set to the actual pin number

#if ENABLED(CUSTOM_USER_BUTTONS)

  // Auto Home
  #if PIN_EXISTS(BUTTON1)
    #define BUTTON1_HIT_STATE     LOW       // State of the triggered button. NC=LOW. NO=HIGH.
    #define BUTTON1_WHEN_PRINTING false     // Button allowed to trigger during printing?
    #define BUTTON1_GCODE         "G28"
    #define BUTTON1_DESC          "Homing"  // Optional string to set the LCD status
  #endif

  // Preheat Bed and Extruder
  #if PIN_EXISTS(BUTTON2)
    #define BUTTON2_HIT_STATE     LOW
    #define BUTTON2_WHEN_PRINTING false
    #define BUTTON2_GCODE         "M140 S" STRINGIFY(PREHEAT_1_TEMP_BED) "\nM104 S" STRINGIFY(PREHEAT_1_TEMP_HOTEND)
    #define BUTTON2_DESC          "Preheat for " PREHEAT_1_LABEL
  #endif

  // ...

#endif
```

Assuming that the joystick will NOT work if the machine is locked, for the
"Start" button, all we need to do is unlock the machine. Optionally we can play
some sounds using the speaker, but that is not required for basic functionality:

``` cpp

#define CUSTOM_USER_BUTTONS

// TODO: Find the buttons to use for these
#define START_BUTTON (xxx)
#define START_GCODE  "M511"
#define START_DESC   "Start Button"

#define BUTTON1_PIN START_BUTTON

#define BUTTON1_HIT_STATE     LOW       // State of the triggered button. NC=LOW. NO=HIGH.
#define BUTTON1_WHEN_PRINTING false     // Button allowed to trigger during printing?
#define BUTTON1_GCODE         START_GCODE
#define BUTTON1_DESC          START_DESC
```

The Drop button is pretty simple too:

1. Configure for relative movement
1. Drop Z (X mm)
1. Grab (Run E motor basically)
1. Retract Z (Home Z)
1. Home X Y
1. UnGrab (Run E motor backwards)
1. Disable Joystick (Lock?)

``` cpp
// Custom Variables
#define DROP_HEIGHT (100) // mm
#define GRAB_AMOUNT (10)  // mm

#define DROP_BUTTON (xxx)
#define DROP_GCODE  "G91\n \
                    "G0 Z" STRINGIFY(DROP_HEIGHT) "\n" \
                    "G0 E" STRINGIFY(GRAB_AMOUNT) "\n" \
                    "G28 Z\n" \
                    "G28 X Y\n" \
                    "G0 E-" STRINGIFY(GRAB_AMOUNT) \
                    "M510\n" \ 
#define DROP_DESC   "Drop Button"

#define BUTTON2_PIN DROP_BUTTON 

#define BUTTON2_HIT_STATE     LOW
#define BUTTON2_WHEN_PRINTING false
#define BUTTON2_GCODE         START_GCODE
#define BUTTON2_DESC          START_DESCRIPTION
```

### Questions

- Q: Does the Joystick work if the machine is locked?
- Q: Can G code be negative? is it just `X-100` ?
    - Yeah basically, the internet (reprap forum) said as much
- Q: Can I create a Custom Print Timer GCode to "time out"?
- Q: Can I control a servo using the Stepper HBRIDGE? (Probably not)
