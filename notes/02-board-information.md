# Board Information

According to the [Marlin Documentation](https://marlinfw.org/docs/hardware/boards.html): 

Several files in the Marlin source code provide hardware support, but the files supporting the core electronics are:

- boards.h -> Contains the full list of boards supported by Marlin. Set MOTHERBOARD to one of the boards listed here.
- pins.h -> Includes the appropriate pins_BOARD.h file for the specified MOTHERBOARD. See Board Pins for more details.
- pins_BOARDNAME.h -> Each of these files assigns pins to Marlin functions. Some of these files are shared by related boards.
- pins_postprocess.h ->  Auto-assign stepper and endstop pins for extra axes. Define pins as -1 where needed. Undefine pins that are not needed.
- platformio.ini -> Some boards will need a new PlatformIO environment with custom build settings.

We can use these files to determine:

1. The Build information to make our custom firmware
2. The pins and configuration needed to do our stuff


