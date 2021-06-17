# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Randall Bohn (dexter)
#
# SPDX-License-Identifier: Unlicense
"""
Simple example of vertical and horizontal sliders.

"""
import math
import random
import time

import board
import displayio
from dexter_slider import Slider

# use built in display (FunHouse etc.)
# see guide for setting up external displays (TFT / OLED breakouts, RGB matrices, etc.)
# https://learn.adafruit.com/circuitpython-display-support-using-displayio/display-and-display-bus
display = board.DISPLAY

main_group = displayio.Group()
display.show(main_group)

minor_axis = 60
vertical_slider = Slider(
    display.width - minor_axis,
    minor_axis,
    minor_axis,
    display.height - minor_axis,
    "ruby",
)
vertical_slider.slide_color = 0xFF0000
main_group.append(vertical_slider)

horizontal_slider = Slider(
    0, 0, display.width - minor_axis, minor_axis, "sparky", limits=(0, 30), value=15
)
horizontal_slider.slide_color = 0x0099FF
main_group.append(horizontal_slider)


def dispatch(touch_point):
    if vertical_slider.contains(touch_point):
        vertical_slider.selected(touch_point)
    if horizontal_slider.contains(touch_point):
        horizontal_slider.selected(touch_point)


time_step = 0.2
last_step = time.monotonic()
ticker = 0
while True:
    now = time.monotonic()
    if time_step < now - last_step:
        # since the FunHouse doesn't have a touchscreen
        # update the sliders using math
        ticker += 1
        last_step = now
        value = math.sin(2 * math.pi * ticker / 100) * vertical_slider.height / 2
        vertical_point = (
            display.width - 20,
            minor_axis + (display.height - minor_axis) / 2 + value,
        )
        dispatch(vertical_point)

        horizontal_point = (int(random.random() * horizontal_slider.width), 0)
        dispatch(horizontal_point)
