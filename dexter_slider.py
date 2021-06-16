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

class BaseBar():
    def __init__(self, limits=(0,100), value=50):
        self.limits = limits
        self.value = value

    def scale(self, new_value):
        """normalize new_value to a float [0.0:1.0)"""
        return (new_value-self.limits[0])/(self.limits[1]-self.limits[0])

class VerticalBar(BaseBar):
    def __init__(self, width, height, limits, value, fill):
        super().__init__(limits, value)
        self.width = width
        self.height = height
        self.fill = fill
        self.rect = self._Rect()

    def _Rect(self):
        scaled_height = int(self.scale(self.value)*self.height)
        scaled_height = max(3,scaled_height)
        return Rect(1, self.height-scaled_height+1, self.width-2, scaled_height-2, fill=self.fill)

    def update(self, point):
        a = (self.height-point[1])/self.height
        self.value = (self.limits[1]-self.limits[0]) * a + self.limits[0]
        self.rect = self._Rect()
        return self.value

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
        if width >= height:
            self.bar = HorizontalBar(width, height, limits=limits, value=value, fill=self.bar_color)
        else:
            self.bar = VerticalBar(width, height, limits=limits, value=value, fill=self.bar_color)
        self.append(self.bar.rect)
        self.title = Label(terminalio.FONT, text=f"{self.name}:{self.value}", color=self.frame_color)
        self.title.anchor_point = (0,1/2)
        self.title.anchored_position = (8, height-12)
        self.append(self.title)
    def contains(self, point):
        return super().contains(
                (point[0]-self.x, point[1]-self.y))
    def selected(self, point):
        local_point = (point[0]-self.x, point[1]-self.y)
        self.remove(self.bar.rect)
        self.value = self.bar.update(local_point)
        self.insert(1,self.bar.rect)
        self.title.text = f"{self.name}:{int(self.value)}"
