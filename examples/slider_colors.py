# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Randall Bohn (dexter)
#
# SPDX-License-Identifier: Unlicense

# Run me on the 3.5" TFT FeatherWing
import time
import displayio

from adafruit_featherwing import tft_featherwing_35
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from dexter_slider import Slider

displayio.release_displays()
wing = tft_featherwing_35.TFTFeatherWing35()
display = wing.display
display.rotation = 180
touchscreen = wing.touchscreen

color0 = 0x666666
color1 = 0xCCCCCC

lora32 = bitmap_font.load_font("/fonts/Lora-32.pcf")
top_group = displayio.Group()
title = displayio.Group()
ribbon = Rect(0, 0, 480, 60, fill=color0)
title.append(ribbon)
ttext = Label(lora32, text="Color Select RGB", color=color1)
ttext.anchor_point = (0, 1 / 2)
ttext.anchored_position = (8, 30)
title.append(ttext)
top_group.append(title)

ruby = Slider(
    5 * 480 // 8,
    100,
    54,
    160,
    name="red",
    limits=(0, 255),
    value=60,
    slide_color=0xFF0000,
)
ruby.title.anchored_position = [0, ruby.height + 12]
top_group.append(ruby)
gus = Slider(
    6 * 480 // 8,
    100,
    54,
    160,
    name="green",
    limits=(0, 255),
    value=12,
    slide_color=0x00FF00,
)
gus.title.anchored_position = [0, gus.height + 12]
top_group.append(gus)
billie = Slider(
    7 * 480 // 8,
    100,
    54,
    160,
    name="blue",
    limits=(0, 255),
    value=80,
    slide_color=0x0000FF,
)
billie.title.anchored_position = [0, billie.height + 12]
top_group.append(billie)

swatch = Rect(1 * 480 // 8, 100, 3 * 480 // 8, 160, outline=color0, stroke=3)
swatch.fill = (ruby.value, gus.value, billie.value)
top_group.append(swatch)

display.show(top_group)


def selected_color():
    return int(ruby.value), int(gus.value), int(billie.value)


def scale(raw):
    "scale a raw touch point to the screen, adapt for rotation=180"
    x0 = 140
    y0 = 120
    x = display.width - (raw["y"] - x0) * display.width // (3809 - x0)
    y = (raw["x"] - y0) * display.height // (3800 - y0)
    return x, y


def dispatch(touchpoints):
    for touch in touchpoints:
        point = scale(touch)
    for slider in [ruby, gus, billie]:
        if slider.contains(point):
            slider.selected(point)


if __name__ == "__main__":
    while True:
        if touchscreen.touched:
            while not touchscreen.buffer_empty:
                dispatch(touchscreen.touches)
        swatch.fill = selected_color()
        time.sleep(0.1)
