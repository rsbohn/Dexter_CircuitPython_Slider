# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Randall Bohn (dexter)
#
# SPDX-License-Identifier: MIT
"""
`dexter_slider`
================================================================================

A slider widget for DisplayIO-Layout


* Author(s): Randall Bohn (dexter)

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports
from adafruit_displayio_layout.widgets.widget import Widget
from adafruit_displayio_layout.widgets.control import Control
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
import terminalio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/rsbohn/Dexter_CircuitPython_Slider.git"

class Slider(Widget, Control):
    def __init__(self, x, y, width, height, name, limits=(0,100), value=50, **kwargs):
        super().__init__(x=x,y=y,width=width,height=height, **kwargs)
        self.touch_boundary=(0,0,width,height)
        self.name = name
        self.limits = limits
        self.value = value
        self.frame_color=0xFFFFFF
        self.bar_color=0x666666
        self.error_color=0xCC0000

        self.frame = Rect(0,0,width,height,outline=self.frame_color)
        self.append(self.frame)
        self.bar = self._make_bar(value)
        self.append(self.bar)
        self.title = Label(terminalio.FONT, text=f"{self.name}:{self.value}", color=self.frame_color)
        self.title.anchor_point = (0,1/2)
        self.title.anchored_position = (8, height-12)
        self.append(self.title)
    def contains(self, point):
        return super().contains(
                (point[0]-self.x, point[1]-self.y))
    def _make_bar(self, value):
        vmin = self.limits[0]
        vmax = self.limits[1]
        width = int(self.width * (value - vmin) / (vmax - vmin))
        return Rect(1,1, width-2, self.height-2, fill=self.bar_color)
    def _scale(self, value):
        vmin = self.limits[0]
        vmax = self.limits[1]
        new_value = int(vmin + (vmax-vmin) * (value - self.x) / self.width)
        limited = False
        if new_value > vmax:
            new_value = vmax
            limited = True
        if new_value <= vmin:
            new_value = vmin
            limited = True
        return new_value, limited
    def set_value(self, value):
        new_value, limited = self._scale(value)
        self.value = new_value
        self.remove(self.bar)
        self.bar = self._make_bar(new_value)
        if limited:
            self.bar.fill = self.error_color
        self.insert(1, self.bar)
        self.title.text = f"{self.name}:{self.value}"
        return self.value
