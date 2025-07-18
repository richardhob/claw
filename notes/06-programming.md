# Programming the Board

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

Simple!
