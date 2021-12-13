#!/usr/bin/env python3
"""
Exercise the various parts of the system.
"""

from   pixelgames.canvas              import Canvas
from   pixelgames.canvas.pimoroni     import UnicornHatHD
from   pixelgames.canvas.rgbledmatrix import RGBLEDMatrix
from   pixelgames.canvas.terminal     import Curses
from   pixelgames.inputs.joysticks    import AtariJoystick

import pygame
import time

# Set up the display and the Joystick
display  = Curses()
#display  = RGBLEDMatrix()
#display  = UnicornHatHD()
canvas   = Canvas(display, xwrap=True, ywrap=True)
joystick = AtariJoystick(pygame)

# Rock until you drop
try:
    # Limits
    w = display.width  - 1
    h = display.height - 1

    # Point position, size and colour
    x = w / 2
    y = h / 2
    s = 1
    r = 0.5
    g = 0.5
    b = 0.5

    # No bigger than this
    mx = min(w, h) / 2

    # And set them going
    while True:
        # Limit things
        start = time.time()

        # Get the canvas ready to draw
        canvas.clear()

        # Get the joystick state
        (jx, jy) = joystick.get_direction()
        jb       = joystick.is_button_pressed(0)
        
        # Different actions depending on whether the button is pressed or not
        if not jb:
            # Move the point?
            if   jx < 0 and x > 0:
                x -= 1
            elif jx > 0 and x+1 < w:
                x += 1
            if   jy < 0 and y > 0:
                y -= 1
            elif jy > 0 and y+1 < h:
                y += 1
        else:
            # Change the size of the point or the colour
            if   jx < 0 and s > 1:
                s -= 1
            elif jx > 0 and s < mx:
                s += 1
            elif jy < 0 and r > 0:
                r -= 0.1
            elif jy > 0 and r < 1:
                r += 0.1

        # Display the (big) pixel
        canvas.set(x, h - y, r, g, b, s)
        canvas.show()

        # Don't go crazy
        while time.time() - start < 0.01:
            time.sleep(0.001)

except:
    # Tidy and rethrow
    canvas  .clear()
    canvas  .show()
    canvas  .close()
    joystick.close()
    raise
