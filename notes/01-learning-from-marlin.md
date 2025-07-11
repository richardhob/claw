# Learning from Marlin (2025-07-10)

I know almost nothing about the Ender 3 hardware! Luckily, the 3D printer
firmware is open source:

- [Marlin FW](https://marlinfw.org/)

To "install" Marlin, there's a few guides to read through:

1. [Installing Marlin](https://marlinfw.org/docs/basics/install.html)
2. [Installing PlatformIO](https://marlinfw.org/docs/basics/install_platformio.html)
3. [Installing from the CLI](https://marlinfw.org/docs/basics/install_platformio_cli.html)
    - [Installing Platform IO](https://docs.platformio.org/en/latest/core/installation/index.html)
    - [Installing Platform IO with the Installer Script](https://docs.platformio.org/en/latest/core/installation/methods/installer-script.html)
4. [Configuring Marlin](https://marlinfw.org/docs/configuration/configuration.html)

## Install Marlin

There are two parts: get the firmware, and load the configuration.

``` bash
git clone https://github.com/MarlinFirmware/Marlin.git libs/Marlin
```

We can grab the Ender 3 configuration from the example configurations:

``` bash
git clone https://github.com/MarlinFirmware/Configurations.git libs/Configurations
```

## Install Platform IO

We can install Platform IO using the installer script (which is the recommended
method). From the Guide:

To install or upgrade PlatformIO Core paste that at a Terminal prompt:

Using curl:

``` bash
curl -fsSL -o get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py
python3 get-platformio.py
```

or using wget:

``` bash
wget -O get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py
python3 get-platformio.py
```

For our purpose, I'll download this into the libs directory:

``` bash
> wget -O ./libs/get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py
> python3 ./libs/get-platformio
PlatformIO Core has been successfully installed into an isolated environment `/home/rick/.platformio/penv`!

The full path to `platformio.exe` is `/home/rick/.platformio/penv/bin/platformio`

If you need an access to `platformio.exe` from other applications, please install Shell Commands
(add PlatformIO Core binary directory `/home/rick/.platformio/penv/bin` to the system environment PATH variable):

See https://docs.platformio.org/page/installation.html#install-shell-commands
```

Neat - we get a Python Environment to play with things. Nice.

## Building Marlin

Now that we have platform IO, we should build Marlin. I'll make a quick script
called `platformio.env` which we can source to get the Python Environment:

``` bash
source ~/.platformio/penv/bin/activate
```

We can make sure this works by sourcing this, and checking the installed
packages:

``` bash
> source platformio.env
(penv) > python -m pip freeze
ajsonrpc==1.2.0
anyio==4.9.0
bottle==0.13.4
certifi==2025.7.9
charset-normalizer==3.4.2
click==8.1.7
colorama==0.4.6
exceptiongroup==1.3.0
h11==0.16.0
idna==3.10
marshmallow==3.26.1
packaging==25.0
platformio==6.1.18
pyelftools==0.32
pyserial==3.5
requests==2.32.4
semantic-version==2.10.0
sniffio==1.3.1
starlette==0.46.2
tabulate==0.9.0
typing_extensions==4.14.1
urllib3==2.5.0
uvicorn==0.34.3
wsproto==1.2.0
```

PlatformIO is in there, so we're all good.

Next, we'll get into the environment, create a Marlin branch:

``` bash
(penv) > cd libs/Marlin/
(penv) > git checkout -b my-ender3
```

We'll have to figure out which version of the board we have. I'm like 99% sure I
have a "v1" board, with the `Sanguino` chip on board. So we just need to make
sure whichever configuration we select has that.

``` bash
(penv) > cd ../Configuration/config/examples/Creality
(penv) > grep -rh "MOTHERBOARD BOARD" |  sort | uniq
  #define MOTHERBOARD BOARD_BTT_E3_RRF
  #define MOTHERBOARD BOARD_BTT_MANTA_E3_EZ_V1_0
  #define MOTHERBOARD BOARD_BTT_SKR_E3_DIP
  #define MOTHERBOARD BOARD_BTT_SKR_E3_TURBO
  #define MOTHERBOARD BOARD_BTT_SKR_MINI_E3_V1_0
  #define MOTHERBOARD BOARD_BTT_SKR_MINI_E3_V1_2
  #define MOTHERBOARD BOARD_BTT_SKR_MINI_E3_V2_0
  #define MOTHERBOARD BOARD_BTT_SKR_MINI_E3_V3_0
  #define MOTHERBOARD BOARD_BTT_SKR_PRO_V1_2
  #define MOTHERBOARD BOARD_BTT_SKR_V1_4
  #define MOTHERBOARD BOARD_BTT_SKR_V1_4_TURBO
  #define MOTHERBOARD BOARD_BTT_SKR_V2_0_REV_B
  #define MOTHERBOARD BOARD_BTT_SKR_V3_0
  #define MOTHERBOARD BOARD_CCROBOT_MEEB_3DP
  #define MOTHERBOARD BOARD_CREALITY_CR4NTXXC10
  #define MOTHERBOARD BOARD_CREALITY_ENDER2P_V24S4
  #define MOTHERBOARD BOARD_CREALITY_F401RE
  #define MOTHERBOARD BOARD_CREALITY_V24S1_301
  #define MOTHERBOARD BOARD_CREALITY_V24S1_301F4
  #define MOTHERBOARD BOARD_CREALITY_V4
  #define MOTHERBOARD BOARD_CREALITY_V4210
  #define MOTHERBOARD BOARD_CREALITY_V422
  #define MOTHERBOARD BOARD_CREALITY_V423
  #define MOTHERBOARD BOARD_CREALITY_V427
  #define MOTHERBOARD BOARD_CREALITY_V431
  #define MOTHERBOARD BOARD_CREALITY_V452
  #define MOTHERBOARD BOARD_FYSETC_CHEETAH
  #define MOTHERBOARD BOARD_FYSETC_CHEETAH_V12
  #define MOTHERBOARD BOARD_FYSETC_CHEETAH_V20
  #define MOTHERBOARD BOARD_MELZI_CREALITY
  #define MOTHERBOARD BOARD_MINITRONICS20
  #define MOTHERBOARD BOARD_MKS_ROBIN_E3
  #define MOTHERBOARD BOARD_MKS_ROBIN_E3P
  #define MOTHERBOARD BOARD_MKS_ROBIN_E3_V1_1
  #define MOTHERBOARD BOARD_RAMPS_14_EFB
  #define MOTHERBOARD BOARD_RAMPS_CREALITY
  #define MOTHERBOARD BOARD_RAMPS_ENDER_4
  #define MOTHERBOARD BOARD_TH3D_EZBOARD_V2
```

Neat! Ok so the "MELZI" is the one I want for sure for this board. This is an OG
Ender 3. If I wasn't sure, I'd have to go through what the CPU is on the board,
and correlate it with one of these boards. 

Which configurations are there for the MELZI?

``` bash
(penv) > grep -r "MOTHERBOARD BOARD_MELZI"
Ender-5 Pro/CrealityV1/Configuration.h:  #define MOTHERBOARD BOARD_MELZI_CREALITY
Ender-5/CrealityV1/Configuration.h:  #define MOTHERBOARD BOARD_MELZI_CREALITY
Ender-3/CrealityV1/Configuration.h:  #define MOTHERBOARD BOARD_MELZI_CREALITY
Ender-3 Pro/CrealityV1/Configuration.h:  #define MOTHERBOARD BOARD_MELZI_CREALITY
CR-10/CrealityV1/Configuration.h:  #define MOTHERBOARD BOARD_MELZI_CREALITY
CR-10 Mini/CrealityV1/Configuration.h:  #define MOTHERBOARD BOARD_MELZI_CREALITY
Ender-2/Configuration.h:  #define MOTHERBOARD BOARD_MELZI_CREALITY
```

Let's go with the `Ender-3` V1 version:

``` bash
(penv) > cp ./Ender-3/CrealityV1/* ../../../Marlin/Marlin/
(penv) > cd ../../../Marlin/
(penv) > git status
On branch my-ender3
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   Marlin/Configuration.h
        modified:   Marlin/Configuration_adv.h

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        Marlin/_Bootscreen.h
        Marlin/_Statusscreen.h

no changes added to commit (use "git add" and/or "git commit -a")
```

Finally, let's try to build this thing.

From the Marlin PlatformIO CLI Guide:

| FUNCTION      | COMMAND                                               |
| --------      | -------                                               |
| PIO Build     | platformio run -e target_env                          |
| PIO Clean     | platformio run --target clean -e target_env           |
| PIO Upload    | platformio run --target upload -e target_env          |
| PIO Traceback | platformio run --target upload -e target_env          |
| PIO Program   | platformio run --target program -e target_env         |
| PIO Test      | platformio test upload -e target_env                  |
| PIO Remote    | platformio remote run --target upload -e target_env   |
| PIO Debug     | platformio debug -e target_env                        |

where `target_env` is more than likely "mega2560" (and is the case for the melzi
sanguino board).

So let's try to build:

``` bash
(pyenv) > pio run -e melzi
**ERROR**
```

Oh sure there's an error pragma in the Configuration file, let's just comment
that out and continue:

``` bash
(pyenv) > pio run -e melzi
RAM:   [===       ]  29.1% (used 4770 bytes from 16384 bytes)
Flash: [==========]  100.3% (used 127410 bytes from 126976 bytes)
Error: The program size (127410 bytes) is greater than maximum allowed (126976 bytes)
*** [checkprogsize] Explicit exit, status 1
```

Oh great! We've exceeded the maximum allotted size. Let's make some
configuration modifications and come back. 

This is kinda expected now that I'm thinking about it - the default Ender 3 did
not ship with the Arduino Bootloader, most likely because it exceeded the size
like this did...

If I remember right, we can turn off the speaker, and get the image size small
enough to build:

``` bash
- #define SPEAKER
+ // #define SPEAKER
```

And rebuilding:

```  bash
RAM:   [===       ]  29.0% (used 4746 bytes from 16384 bytes)
Flash: [==========]  99.0% (used 125744 bytes from 126976 bytes)
Building .pio/build/melzi/firmware.hex
===================== [SUCCESS] Took 8.74 seconds =============================

Environment    Status    Duration
-------------  --------  ------------
melzi          SUCCESS   00:00:08.742
```

Neat! We're IN. We'll save our changes to our branch and ... blow the dust off
the board next?
