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

## boards.h

This `boards.h` file can be found at `Marlin/src/core/boards.h`, and contains
the board definitions for every board Marlin supports. 

It's really just a file with a bunch of `#define` statements:

``` cpp
#include "macros.h"

#define BOARD_UNKNOWN -1

//
// RAMPS 1.3 / 1.4 - ATmega1280, ATmega2560
//

#define BOARD_RAMPS_OLD               1000  // MEGA/RAMPS up to 1.2

#define BOARD_RAMPS_13_EFB            1010  // RAMPS 1.3 (Power outputs: Hotend, Fan, Bed)
#define BOARD_RAMPS_13_EEB            1011  // RAMPS 1.3 (Power outputs: Hotend0, Hotend1, Bed)
#define BOARD_RAMPS_13_EFF            1012  // RAMPS 1.3 (Power outputs: Hotend, Fan0, Fan1)
#define BOARD_RAMPS_13_EEF            1013  // RAMPS 1.3 (Power outputs: Hotend0, Hotend1, Fan)
#define BOARD_RAMPS_13_SF             1014  // RAMPS 1.3 (Power outputs: Spindle, Controller Fan)

// Continues forever
```

Simple. Not really interesting for me right now though.

## pins.h

The `pins.h` file can be found at `Marlin/src/pins/pins.h`. This file does
_some_ definitions of some things, and also imports the pins based on the
defined Board.

After some cool patching of things, the board specific pins file is imported:

``` cpp 
//
// RAMPS 1.3 / 1.4 / 1.6+ - ATmega1280, ATmega2560
//

#if MB(RAMPS_OLD)
  #include "ramps/pins_RAMPS_OLD.h"                 // ATmega2560, ATmega1280               env:mega2560 env:mega1280
#elif MB(RAMPS_13_EFB, RAMPS_13_EEB, RAMPS_13_EFF, RAMPS_13_EEF, RAMPS_13_SF)
  #include "ramps/pins_RAMPS_13.h"                  // ATmega2560, ATmega1280               env:mega2560 env:mega1280
#elif MB(RAMPS_14_EFB, RAMPS_14_EEB, RAMPS_14_EFF, RAMPS_14_EEF, RAMPS_14_SF)
  #include "ramps/pins_RAMPS.h"                     // ATmega2560, ATmega1280               env:mega2560 env:mega1280
#elif MB(RAMPS_PLUS_EFB, RAMPS_PLUS_EEB, RAMPS_PLUS_EFF, RAMPS_PLUS_EEF, RAMPS_PLUS_SF)
  #include "ramps/pins_RAMPS_PLUS.h"                // ATmega2560, ATmega1280               env:mega2560 env:mega1280

// Continued ....
```

For the `MELZI` configuration, we want the `sanguino/pins_MELZI_CREALITY.h`
file.

## pins_BOARDNAME.h

The `pins_BOARDNAME.h` can be found in the `Marlin/src/pins` directory, where
the files are sorted and organized into many folders and files.

For our board, we can use the `sanguino/pins_MELZI_CREALITY.h` pins file. This
file contains the definitions required for Marlin to drive the various
functions. The pins file here also includes the `sanguino/pins_MELZI.h` file,
which includes the `sanguino/pins_SANGUINOLOLU_12.h` file, which THEN includes
the `sanguino/pins_SANGUINOLOLU_11.h`. 

Finally we hit the bottom - this has most of the cool stuff we need to do our
project.

## pins_postprocess.h

The `pins_postprocess.h` file can be found at
`Marlin/src/pins/pins_postprocess.h`. This file does some clean up of the pin
definitions:

- set pins to `-1` if they are undefined.
- Throw `#error` in some conditions
- Define new variables and auto assign stuffs.

Pretty cool - I hope we don't have to understand this one.

## platformio.ini

This one is easy, it's just at `platformio.ini` in the Marlin root directory.
Each board family has a config file in the `ini` directory, which are a nested
chain of INI fields... great stuff.

For the `melzi` environment, here are the options from various files that are
used:

``` ini

# from ini/avr.ini
[common_avr8]
platform          = atmelavr@~4.0.1
build_flags       = ${common.build_flags} -std=gnu++1z -Wl,--relax
build_unflags     = -std=gnu++11
board_build.f_cpu = 16000000L
build_src_filter  = ${common.default_src_filter} +<src/HAL/AVR>

[env:sanguino1284p]
extends                   = common_avr8
board                     = sanguino_atmega1284p
board_upload.maximum_size = 126976

[env:melzi]
extends      = env:sanguino1284p
upload_speed = 57600

# from platformio.ini
[common]
build_flags        = -g3 -D__MARLIN_FIRMWARE__ -DNDEBUG
                     -fmax-errors=5
extra_scripts      =
  pre:buildroot/share/PlatformIO/scripts/configuration.py
  pre:buildroot/share/PlatformIO/scripts/common-dependencies.py
  pre:buildroot/share/PlatformIO/scripts/common-cxxflags.py
  pre:buildroot/share/PlatformIO/scripts/preflight-checks.py
  post:buildroot/share/PlatformIO/scripts/common-dependencies-post.py
lib_deps           =
default_src_filter = +<src/*> -<src/config> -<src/tests>
  ; LCDs and Controllers
  -<src/lcd/HD44780> -<src/lcd/dogm> -<src/lcd/TFTGLCD> -<src/lcd/tft> -<src/lcd/tft_io>
  -<src/lcd/e3v2> -<src/lcd/sovol_rts> -<src/lcd/menu> -<src/lcd/extui> -<src/lcd/touch>
  -<src/lcd/lcdprint.cpp>
  ; Marlin HAL
  -<src/HAL>
  +<src/HAL/shared>
  -<src/HAL/shared/backtrace>
  -<src/HAL/shared/cpu_exception>
  -<src/HAL/shared/eeprom_if_i2c.cpp>
  -<src/HAL/shared/eeprom_if_spi.cpp>
  ; Features and G-Codes
  -<src/feature>
  -<src/gcode/bedlevel>
  -<src/gcode/calibrate>
  -<src/gcode/config>
  -<src/gcode/control>
  -<src/gcode/feature>
  -<src/gcode/geometry>
  -<src/gcode/host>
  -<src/gcode/lcd>
  -<src/gcode/motion>
  -<src/gcode/ota>
  -<src/gcode/probe>
  -<src/gcode/scara>
  -<src/gcode/sd>
  -<src/gcode/temp>
  -<src/gcode/units>
  ; Library Code
  -<src/libs/heatshrink>
  -<src/libs/BL24CXX.cpp> -<src/libs/W25Qxx.cpp>
  -<src/libs/MAX31865.cpp>
  -<src/libs/hex_print.cpp>
  -<src/libs/least_squares_fit.cpp>
  -<src/libs/nozzle.cpp>
  ; Modules
  -<src/module>
  -<src/module/stepper>
  ; Media Support
  -<src/sd>
  ;
  ; Minimal Requirements
  ;
  +<src/gcode/calibrate/G28.cpp>
  +<src/gcode/config/M200-M205.cpp>
  +<src/gcode/config/M220.cpp>
  +<src/gcode/control/M17_M18_M84.cpp>
  +<src/gcode/control/M80_M81.cpp>
  +<src/gcode/control/M85.cpp>
  +<src/gcode/control/M108_*.cpp>
  +<src/gcode/control/M111.cpp>
  +<src/gcode/control/M120_M121.cpp>
  +<src/gcode/control/M999.cpp>
  +<src/gcode/geometry/G92.cpp>
  +<src/gcode/host/M110.cpp>
  +<src/gcode/host/M114.cpp>
  +<src/gcode/host/M118.cpp>
  +<src/gcode/host/M119.cpp>
  +<src/gcode/motion/G0_G1.cpp>
  +<src/gcode/motion/G4.cpp>
  +<src/gcode/motion/M400.cpp>
  +<src/gcode/temp/M105.cpp>
  +<src/module/endstops.cpp>
  +<src/module/motion.cpp>
  +<src/module/planner.cpp>
  +<src/module/settings.cpp>
  +<src/module/stepper.cpp>
  +<src/module/temperature.cpp>
  +<src/module/tool_change.cpp>
  +<src/module/stepper/indirection.cpp>

[env]
framework         = arduino
extra_scripts     = ${common.extra_scripts}
build_flags       = ${common.build_flags}
lib_deps          = ${common.lib_deps}
monitor_speed     = 250000
monitor_eol       = LF
monitor_echo      = yes
monitor_filters   = colorize, time, send_on_enter

[env:include_tree]
platform         = atmelavr
board            = megaatmega2560
build_flags      = -c -H -std=gnu++11 -Wall -Os -D__MARLIN_FIRMWARE__
build_src_filter = +<src/MarlinCore.cpp>
```

Lots of stuff. Build flags, source files, all kinds of goodies. I wonder where
the main function is?

## MarlinCore.cpp

The main pins of code are kept in `Marlin/src/MarlinCore.cpp`, and the two main
functions are `setup` and `loop`. `loop` calls `idle` and `queue.advance()`.
According to the code comments, the `queue` holds G-Code commands to be
executed, and NO G-Code commands should be executed during `idle`

Neat stuff - only 1744 lines in this file or so, no big deal :) 

## Conclusion

So we have a _rough_ layout of the land here - we know where the pins are
defined, and where the main function is and stuff. The next step is to poke
around and see where the COOL STUFF happens.
