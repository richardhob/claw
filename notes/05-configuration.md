# Configuration

## Joystick

In `Configuration_adv.h` the Joystick configuration is as follows:

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
  //#define JOYSTICK_DEBUG
#endif
```

Definition will be as follows:

``` cpp
#define JOYSTICK
#if ENABLED(JOYSTICK)
  #define JOY_X_PIN    6  // RAMPS: Suggested pin A5  on AUX2
  #define JOY_Y_PIN    7  // RAMPS: Suggested pin A10 on AUX2
  #define JOY_Z_PIN  (-1) // RAMPS: Suggested pin A12 on AUX2
  #define JOY_EN_PIN (-1) // RAMPS: Suggested pin D44 on AUX2

  //#define INVERT_JOY_X  // Enable if X direction is reversed
  //#define INVERT_JOY_Y  // Enable if Y direction is reversed
  //#define INVERT_JOY_Z  // Enable if Z direction is reversed

  // Use M119 with JOYSTICK_DEBUG to find reasonable values after connecting:
  #define JOY_X_LIMITS { 5600, 8190-100, 8190+100, 10800 } // min, deadzone start, deadzone end, max
  #define JOY_Y_LIMITS { 5600, 8250-100, 8250+100, 11000 }
  #define JOY_Z_LIMITS { 4800, 8080-100, 8080+100, 11550 }
  #define JOYSTICK_DEBUG
#endif
```

Let's see if this works!

## Debug Tasks

So I don't have an Analog Joy stick. I thought I did! But it's a _digital_
joystick. Which won't work here. 

So instead, I'll use my Analog Discovery to test the Joy stick. Also, this
printer board has a Broken Y Axis, so I'm going to use X and Z for now.

``` patch
  #define JOY_X_PIN    6  // RAMPS: Suggested pin A5  on AUX2
- #define JOY_Y_PIN    7  // RAMPS: Suggested pin A10 on AUX2
+ #define JOY_Y_PIN  (-1) // RAMPS: Suggested pin A10 on AUX2
- #define JOY_Z_PIN  (-1) // RAMPS: Suggested pin A12 on AUX2
+ #define JOY_Z_PIN    7  // RAMPS: Suggested pin A12 on AUX2
  #define JOY_EN_PIN (-1) // RAMPS: Suggested pin D44 on AUX2
```

This will simplify things a bit - we need to ground the Analog Discovery to the
common ground on the board, and just _set_ the voltage. With a voltage set,
we'll be able to configure the dead zone, etc.

We can configure and set the voltage from Python as well. With Waveforms
installed:

    https://lp.digilent.com/complete-waveforms-download/

We can find the sample applications at:

    /usr/share/digilent/waveforms/samples/py

The one that's most useful for us today is `AnalogOut_Sine.py`, in which the
good stuff is:

``` python
# UGH Bad
from ctypes import *

dwf = cdll.LoadLibrary("libdwf.so")

hdwf = c_int()
channel = c_int(0)
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+str(version.value))

# prevent temperature drift
dwf.FDwfParamSet(DwfParamOnClose, c_int(0)) # 0 = run, 1 = stop, 2 = shutdown

#open device
print("Opening first device...")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))


if hdwf.value == hdwfNone.value:
    print("failed to open device")
    quit()

# 0 = the device will be configured only when calling FDwf###Configure
dwf.FDwfDeviceAutoConfigureSet(hdwf, c_int(0))

dwf.FDwfAnalogOutNodeEnableSet(hdwf, channel, AnalogOutNodeCarrier, c_int(1))
dwf.FDwfAnalogOutNodeFunctionSet(hdwf, channel, AnalogOutNodeCarrier, funcSine)
dwf.FDwfAnalogOutNodeFrequencySet(hdwf, channel, AnalogOutNodeCarrier, c_double(1000))
dwf.FDwfAnalogOutNodeAmplitudeSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.41))
dwf.FDwfAnalogOutNodeOffsetSet(hdwf, channel, AnalogOutNodeCarrier, c_double(1.41))

print("Generating sine wave...")
dwf.FDwfAnalogOutConfigure(hdwf, channel, c_int(1))

dwf.FDwfDeviceClose(hdwf)
```

Simple enough - the script sets the "Node Function" to `funcSine`, sets the
frequency to 1000 Hz, and the Amplitude and Offset to 1.41 V. Neat.

Looking though the `dwfconstants.py`, I can see that there is a `funcDC` option
for the "Node Function", so that's probably what we'll need. The
`AnalogOutIn_DC.py` sample uses the `OffsetSet` only to set the output Offset,
so we'll just use that.



### Joystick (M119)

### Lock and Joystick
