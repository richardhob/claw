# CLAW GAME from Ender 3

Who doesn't love a claw game? In this project, I will attempt to make a claw
game from an (extra) Ender 3 printer I have lying around. 

## Software Required for development

- [PlatformIO](https://platformio.org/)
- Make (for Unit tests)
- GCC (for Unit test)
- Unity by Throw The Switch (for Unit Tests)

## Marlin PlatformIO Cheat Sheet

For more CLI information, see the [User Guide](https://docs.platformio.org/en/latest/core/index.html)

| FUNCTION      | COMMAND                                        |
| --------      | -------                                        |
| PIO Build     | platformio run -e melzi                        |
| PIO Clean     | platformio run --target clean -e melzi         |
| PIO Upload    | platformio run --target upload -e melzi        |
| PIO Traceback | platformio run --target upload -e melzi        |
| PIO Program   | platformio run --target program -e melzi       |
| PIO Test      | platformio test upload -e melzi                |
| PIO Remote    | platformio remote run --target upload -e melzi |
| PIO Debug     | platformio debug -e melzi                      |
