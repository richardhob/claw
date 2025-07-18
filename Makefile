
HEADERS := config/_Bootscreen.h \
           config/Configuration_adv.h \
           config/Configuration.h \
           config/_Statusscreen.h \
           config/_Version.h

LIB_DIR := libs
MARLIN  := libs/Marlin
FIRMWARE := $(MARLIN)/.pio/build/melzi/firmware.elf
PLATFORMIO := ~/.platformio/penv/bin/pio
UDEV_RULES := /etc/udev/rules.d/99-platformio-udev.rules

PY_SRC := scripts/set_voltage.py scripts/test/test_set_voltage.py
PYTEST := ./pytest-env/bin/pytest

.PHONY: all
all: $(FIRMWARE)

.PHONY: program
program: $(HEADERS) | $(UDEV_RULES)
	cd $(MARLIN); $(PLATFORMIO) run --target upload -e melzi

$(UDEV_RULES):
	@echo "Please install the UDEV rules (https://docs.platformio.org/en/latest/core/installation/udev-rules.html)"
	@echo ""
	@echo "1. curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules | 99-platformio-udev.rules"
	@echo "2. sudo mv 99-platformio-udev.rules $(UDEV_RULES)"
	@echo "3. sudo service udev restart"
	@echo "4. Disconnect and Reconnect the board"
	@exit 10

## Marlin PlatformIO Cheat Sheet
# 
# For more CLI information, see the [User Guide](https://docs.platformio.org/en/latest/core/index.html)
# 
# | FUNCTION      | COMMAND                                        |
# | --------      | -------                                        |
# | PIO Build     | platformio run -e melzi                        |
# | PIO Clean     | platformio run --target clean -e melzi         |
# | PIO Upload    | platformio run --target upload -e melzi        |
# | PIO Traceback | platformio run --target upload -e melzi        |
# | PIO Program   | platformio run --target program -e melzi       |
# | PIO Test      | platformio test upload -e melzi                |
# | PIO Remote    | platformio remote run --target upload -e melzi |
# | PIO Debug     | platformio debug -e melzi                      |
# 
$(FIRMWARE): $(HEADERS) | $(MARLIN) $(PLATFORMIO)
	cp config/* $(MARLIN)/Marlin
	cd $(MARLIN); $(PLATFORMIO) run -e melzi

# Clone Marlin
$(MARLIN):
	git clone https://github.com/MarlinFirmware/Marlin.git $@

# Install PlatformIO
$(PLATFORMIO):
	wget -O get-platformio.py https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py
	python3 get-platformio.py

.PHONY: selftest
selftest: $(PY_SRC) | $(PYTEST)
	$(PYTEST) scripts/test

# Install Pytest
$(PYTEST): 
	python3 -m venv pytest-env
	pytest-env/bin/python -m pip install pytest
