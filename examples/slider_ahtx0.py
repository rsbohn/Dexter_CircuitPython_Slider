# SPDX-FileCopyrightText: Copyright (c) 2021 Randall Bohn (dexter)
# SPDX-License-Identifier: MIT

import time
import board
import displayio
from adafruit_ssd1327 import SSD1327
from adafruit_ahtx0 import AHTx0
from dexter_slider import Slider

"""Display temperature and relative humidity.

Equipment:
 - Feather or Metro board that runs CircuitPython
 - SSD1327 128x128 OLED Display
    https://www.adafruit.com/product/4741
 - AHT20 Sensor Breakout
    https://www.adafruit.com/product/4566
"""

i2c = board.I2C()
displayio.release_displays()
bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = SSD1327(bus, width=127, height=127)
front = displayio.Group()
display.show(front)

sensor = AHTx0(i2c)
temperature = Slider(128 - 40 * 2, 4, 32, 120, name="T", limits=(68, 82))
temperature.title.anchored_position = [2, 8]
front.append(temperature)
humidity = Slider(128 - 40 * 1, 4, 32, 120, name="H")
humidity.title.anchored_position = [2, 8]
front.append(humidity)

last_update = 0
refresh = 5

while True:
    now = time.monotonic()
    if refresh < now - last_update:
        last_update = now
        temperature.value = sensor.temperature * 1.8 + 32.0
        humidity.value = sensor.relative_humidity
    time.sleep(1)
