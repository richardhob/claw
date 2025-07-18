# Programming the Board

Created a Makefile recipe to program the device, but it doesn't quite work...
getting a few errors.

## Error: UDEV Rules not installed

Links to:

    https://docs.platformio.org/en/latest/core/installation/udev-rules.html

Solution:

1. `curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules | 99-platformio-udev.rules`
2. `sudo mv 99-platformio-udev.rules /etc/udev/rules.d/99-platformio-udev.rules`
3. `sudo service udev restart`
4. Disconnect and Reconnect the board

Programming progresses from PlatformIO, but isn't working now... what's the
deal?

## Debug

Looking at the USB connections:

``` bash
> lsusb
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 004: ID 0e8d:0608 MediaTek Inc. Wireless_Device
Bus 003 Device 003: ID 0d8c:0014 C-Media Electronics, Inc. Audio Adapter (Unitek Y-247A)
Bus 003 Device 002: ID 046d:c534 Logitech, Inc. Unifying Receiver
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 003: ID 1a86:7523 QinHeng Electronics CH340 serial converter
Bus 001 Device 002: ID 320f:5000 Evision RGB Keyboard
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

My best guess is that the "CH340" device is the USB device we care about. I
confirmed this by unplugging and replugging the device and checking the `lsusb`
output.

Next, I'll check the `dmesg` output to see if anything interesting happened over
there:

``` bash
> sudo dmesg | tail -10
[  343.347601] usb 1-4: new full-speed USB device number 5 using xhci_hcd
[  343.489365] usb 1-4: New USB device found, idVendor=1a86, idProduct=7523, bcdDevice= 2.63
[  343.489383] usb 1-4: New USB device strings: Mfr=0, Product=2, SerialNumber=0
[  343.489389] usb 1-4: Product: USB2.0-Serial
[  343.495774] ch341 1-4:1.0: ch341-uart converter detected
[  343.507873] usb 1-4: ch341-uart converter now attached to ttyUSB0
[  344.067782] input: BRLTTY 6.4 Linux Screen Driver Keyboard as /devices/virtual/input/input34
[  344.072298] usb 1-4: usbfs: interface 0 claimed by ch341 while 'brltty' sets config #1
[  344.075463] ch341-uart ttyUSB0: ch341-uart converter now disconnected from ttyUSB0
[  344.075499] ch341 1-4:1.0: device disconnected
```

Oh ok! So the USB device is connected, and the UART converter is detected, but
it was "claimed" by BRLTTY? huh.

Some web searching provided two interesting links:

- [GITHUB Issue: usbfs: interface 0 claimed by ch34x while 'brltty' sets config #1](https://github.com/juliagoda/CH341SER/issues/18)
- [StackOverflow: Unable to use USB dongle base on USB-serial converter chip](https://unix.stackexchange.com/questions/670636/unable-to-use-usb-dongle-based-on-usb-serial-converter-chip)
- [ArchLinux: Arduino not working after brltty update](https://bbs.archlinux.org/viewtopic.php?id=269975)
- [HackaDay: How to Write UDEV Rules](https://hackaday.com/2009/09/18/how-to-write-udev-rules/)

There were a few solutions metioned, including outright disabling brltty ... but
the issue seems to stem from a USB ID Overlap between a Brail TTY device and the
Sanguino board.

From the Arch Linux post (reposted on StackOverflow):

`brltty` has a rule for `idVendor=1a86, idProduct=7523`, which is the same as
the CH340 serial converter on my Mega clone.

You can see your device id by using lsusb to get a list of your devices (unplug
your Arduino, run lsusb then plug in your Arduino and run lsusb again to see
which device appears).

In my case:

``` bash
Bus 003 Device 005: ID 1a86:7523 QinHeng Electronics CH340 serial converter
```

Take a note of the ID and then open the brltty rules file:

``` bash
sudo nano /usr/lib/udev/rules.d/90-brltty-device.rules
```

Search through the file until you find the entry for your ID:

```
# Device: 1A86:7523
# Baum [NLS eReader Zoomax (20 cells)]
ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"
```

Now comment out the line:

```
# Device: 1A86:7523
# Baum [NLS eReader Zoomax (20 cells)]
# ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"
```

Save and close the file then reboot.

After the reboot the `/dev/ttyUSB0` port was available again in the Arduino IDE.

### Solution

OK so let's open the brltty device rules. On my device, the brltty rules were
found at:

``` bash
> ls /usr/lib/udev/rules.d/* | grep brltty
/usr/lib/udev/rules.d/85-brltty.rules
```

There were no `brltty` rules in `/etc/udev/rules.d` so we can start tagging this
one. Let's see if our device is in there:

``` bash
> cat /usr/lib/udev/rules.d/85-brltty.rules | grep 1a86
ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"
```

There we go! We just have to comment out this line and (to be safe) restart the
machine... and we'll be all good.

Here are the lines in question:

``` bash
# Device: 1A86:7523
# Baum [NLS eReader Zoomax (20 cells)]
ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"
```

Which changes as follows:

``` bash
# Device: 1A86:7523
# Baum [NLS eReader Zoomax (20 cells)]
- ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"
+# ENV{PRODUCT}=="1a86/7523/*", ENV{BRLTTY_BRAILLE_DRIVER}="bm", GOTO="brltty_usb_run"
```

Simple! After a quick reboot, we can find the magic message in the `dmesg`
output:

``` bash
> sudo dmesg | grep ttyUSB
[    2.790365] usb 1-4: ch341-uart converter now attached to ttyUSB0
```

And now we can see the device as expected in PlatformIO:

``` bash
> pio device list
...
/dev/ttyUSB0
------------
Hardware ID: USB VID:PID=1A86:7523 LOCATION=1-4
Description: USB2.0-Serial
```

NEAT. 

## Error: Not in sync

While trying to program the device, I am getting an error:

``` bash
> make program
...
CURRENT: upload_protocol = arduino
Looking for upload port...
Auto-detected: /dev/ttyUSB0
Uploading .pio/build/melzi/firmware.hex
avrdude: stk500_getsync() attempt 1 of 10: not in sync: resp=0x67
avrdude: stk500_getsync() attempt 2 of 10: not in sync: resp=0xea
avrdude: stk500_getsync() attempt 3 of 10: not in sync: resp=0x5a
avrdude: stk500_getsync() attempt 4 of 10: not in sync: resp=0xd8
avrdude: stk500_getsync() attempt 5 of 10: not in sync: resp=0xbf
avrdude: stk500_getsync() attempt 6 of 10: not in sync: resp=0xbe
avrdude: stk500_getsync() attempt 7 of 10: not in sync: resp=0x0d
avrdude: stk500_getsync() attempt 8 of 10: not in sync: resp=0x21
avrdude: stk500_getsync() attempt 9 of 10: not in sync: resp=0x9f
avrdude: stk500_getsync() attempt 10 of 10: not in sync: resp=0xbd

avrdude done.  Thank you.

*** [upload] Error 1
====================================== [FAILED] Took 5.02 seconds ======================================

Environment    Status    Duration
-------------  --------  ------------
melzi          FAILED    00:00:05.020
================================= 1 failed, 0 succeeded in 00:00:05.020 =================================
```

So we have a USB connection (`ttyUSB`) and we are _trying_ to program... first,
let's try and figure out if we can talk to the USB device using serial.

To do this, we can use `serial.tools.miniterm` (which is installed in the
PlatformIO environment), or we can use `pio device monitor` which launches this
for us basically.

``` bash
(penv) > python -m serial.tools.miniterm - 115200

--- Available ports:
---  1: /dev/ttyS0           'n/a'
---  2: /dev/ttyS1           'n/a'
---  3: /dev/ttyS2           'n/a'
---  4: /dev/ttyS3           'n/a'
---  5: /dev/ttyS4           'n/a'
---  6: /dev/ttyS5           'n/a'
---  7: /dev/ttyS6           'n/a'
---  8: /dev/ttyS7           'n/a'
---  9: /dev/ttyS8           'n/a'
--- 10: /dev/ttyS9           'n/a'
--- 11: /dev/ttyS10          'n/a'
--- 12: /dev/ttyS11          'n/a'
--- 13: /dev/ttyS12          'n/a'
--- 14: /dev/ttyS13          'n/a'
--- 15: /dev/ttyS14          'n/a'
--- 16: /dev/ttyS15          'n/a'
--- 17: /dev/ttyS16          'n/a'
--- 18: /dev/ttyS17          'n/a'
--- 19: /dev/ttyS18          'n/a'
--- 20: /dev/ttyS19          'n/a'
--- 21: /dev/ttyS20          'n/a'
--- 22: /dev/ttyS21          'n/a'
--- 23: /dev/ttyS22          'n/a'
--- 24: /dev/ttyS23          'n/a'
--- 25: /dev/ttyS24          'n/a'
--- 26: /dev/ttyS25          'n/a'
--- 27: /dev/ttyS26          'n/a'
--- 28: /dev/ttyS27          'n/a'
--- 29: /dev/ttyS28          'n/a'
--- 30: /dev/ttyS29          'n/a'
--- 31: /dev/ttyS30          'n/a'
--- 32: /dev/ttyS31          'n/a'
--- 33: /dev/ttyUSB0         'USB2.0-Serial'
--- Enter port index or full name: 33
--- Miniterm on /dev/ttyUSB0  115200,8,N,1 ---
--- Quit: Ctrl+] | Menu: Ctrl+T | Help: Ctrl+T followed by Ctrl+H ---
echo:Unknown command: ""
ok
```

The hot-keys in Miniterm don't work too well in a vim controlled terminal (which
makes sense, there's a lot of `<CTRL> ...` hot keys).

Using a baudrate of 115000 works though - perhaps the Arduino can't do a clock
rate of 115200? 

We can test this by sending some GCODE to the device over serial, using a
baudrate of 115000:

``` bash
(pio) > python -m serial.tools.miniterm /dev/ttyUSB0 115000
G28 XY ;
echo:busy: processing
echo:busy: processing
X:0.00 Y:0.00 Z:5.00 E:0.00 Count X:0 Y:0 Z:2000
ok
```

Note that the GCODE isn't echo'd to the terminal, so you kinda just have to
type. Make sure that the command ends with a semicolon.

### Update Baudrate for the Programmer

The configuration of the programmer is configured in the `avr.ini` file
in the `libs/Marlin/ini` folder:

``` ini
# Marlin/ini/avr.ini

...

[env:melzi]
extends      = env:sanguino1284p
upload_speed = 57600

...
```

Updating the speed in the `Melzi` environment should fix the programming issue:

``` ini
[env:melzi]
extends      = env:sanguino1284p
- upload_speed = 57600
+ upload_speed = 115000
```

This also fails to program .... I think the solution here is to reflash the
bootloader with a known good baudrate configured.

### Flash the Bootloader

Information from Arduino:

    https://docs.arduino.cc/built-in-examples/arduino-isp/ArduinoISP/

The short version of this:

1. Program an arduino as an ISP programmer
2. Connect the Arduino pins to the ISP Header on the Target board
3. Burn the bootloader

This is easiest 1`
