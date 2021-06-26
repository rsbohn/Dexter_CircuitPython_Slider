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
# pylint: disable=too-many-arguments

# imports
from adafruit_displayio_layout.widgets.widget import Widget
from adafruit_displayio_layout.widgets.control import Control
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
import terminalio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/rsbohn/Dexter_CircuitPython_Slider.git"


class BaseSlide:
    """Base class for Vertical/Horizontal Slide"""

    def __init__(self, limits=(0, 100), value=50):
        self.limits = limits
        self.value = value

    def _scale(self, new_value):
        """normalize new_value to a float [0.0:1.0)"""
        return (new_value - self.limits[0]) / (self.limits[1] - self.limits[0])

    def _set_value(self, new_value):
        """directly set a new value"""
        v = new_value
        if v < self.limits[0]:
            v = self.limits[0]
        if v > self.limits[1]:
            v = self.limits[1]
        self.value = v
        self.rect = self._as_rect()
        return self.value


class HorizontalSlide(BaseSlide):
    """A horizontal indicator, grows left to right"""

    def __init__(self, width, height, limits, value, fill):
        super().__init__(limits, value)
        self.width = width
        self.height = height
        self.fill = fill
        self.rect = self._as_rect()

    def _as_rect(self):
        scaled_width = int(self._scale(self.value) * self.width)
        scaled_width = max(3, scaled_width)
        return Rect(1, 1, scaled_width - 2, self.height - 2, fill=self.fill)

    def update(self, point):
        """Update the slider with a new position.

        :param point: x,y local coordinates of touch point
        :type point: Tuple[x,y]
        :return: Double

        """
        scaled_value = point[0] / self.width
        self.value = (self.limits[1] - self.limits[0]) * scaled_value + self.limits[0]
        self.rect = self._as_rect()
        return self.value


class VerticalSlide(BaseSlide):
    """A vertical indicator slide, grows upwards"""

    def __init__(self, width, height, limits, value, fill):
        super().__init__(limits, value)
        self.width = width
        self.height = height
        self.fill = fill
        self.rect = self._as_rect()

    def _as_rect(self):
        scaled_height = int(self._scale(self.value) * self.height)
        scaled_height = max(3, scaled_height)
        return Rect(
            1,
            self.height - scaled_height + 1,
            self.width - 2,
            scaled_height - 2,
            fill=self.fill,
        )

    def update(self, point):
        """Update with a new slider position."""
        scaled_value = (self.height - point[1]) / self.height
        self.value = (self.limits[1] - self.limits[0]) * scaled_value + self.limits[0]
        self.rect = self._as_rect()
        return self.value


class Slider(Widget, Control):
    """A slider control widget. Value is set within limits.

    -- I should have a long list of parameters here.

    """

    def __init__(self, x, y, width, height, name, limits=(0, 100), value=50, **kwargs):
        super().__init__(x=x, y=y, width=width, height=height, **kwargs)
        self.touch_boundary = (0, 0, width, height)
        self.name = name
        self.limits = limits
        self.frame_color = 0xFFFFFF
        self.slide_color = 0x666666
        self.error_color = 0xCC0000

        self.frame = Rect(0, 0, width, height, outline=self.frame_color)
        self.append(self.frame)
        if width >= height:
            self.slide = HorizontalSlide(
                width, height, limits=limits, value=value, fill=self.slide_color
            )
        else:
            self.slide = VerticalSlide(
                width, height, limits=limits, value=value, fill=self.slide_color
            )
        self.append(self.slide.rect)
        self.title = Label(
            terminalio.FONT, text=f"{self.name}:{self.slide.value}", color=self.frame_color
        )
        self.title.anchor_point = (0, 1 / 2)
        self.title.anchored_position = (8, height - 12)
        self.append(self.title)

    def contains(self, point):
        """Checks if the Control was touched.  Returns True if the touch_point is within the
         Control's touch_boundary.

        :param point: x,y screen location of the touch point.
        :type touch_point: Tuple[x,y]
        :return: Boolean

        """
        return super().contains((point[0] - self.x, point[1] - self.y))

    def selected(self, point):
        """Response function when Slider is 'selected' (touched).

        :param point: x,y screen location of the touch point.
        :type point: Tuple[x,y]
        :return: None

        """
        local_point = (point[0] - self.x, point[1] - self.y)
        self.remove(self.slide.rect)
        self.slide.update(local_point)
        self.insert(1, self.slide.rect)
        self.slide.rect.fill = self.slide_color
        self.title.text = f"{self.name}:{int(self.slide.value)}"

    @property
    def value(self):
        """The current Slider value (int)

        :return: int
        """
        return self.slide.value

    @value.setter
    def value(self, new_value):
        if new_value == self.slide.value:
            return
        self.remove(self.slide.rect)
        self.slide._set_value(new_value)
        self.insert(1, self.slide.rect)
        self.slide.rect.fill = 0xFFFF00 #self.slide_color
        self.title.text = f"{self.name}:{int(self.slide.value)}"
