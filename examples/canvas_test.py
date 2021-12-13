#!/usr/bin/env python3
"""
Bounce some pixels around the canvas to make sure it works.
"""

from   pixelgames.canvas               import Canvas
from   pixelgames.canvas.pimoroni      import UnicornHatHD
from   pixelgames.canvas.rgbledmatrix  import RGBLEDMatrix
from   pixelgames.canvas.terminal      import Curses

import time
import math
import numpy
import random

# Rock until you drop
try:
    # Bounce something around
    display = Curses()
    #display = RGBLEDMatrix(rows=64, columns=64, gpio_slowdown=2)
    #display = UnicornHatHD()
    canvas  = Canvas(display, xwrap=True, ywrap=True)

    # Limits
    w = canvas.width  - 1
    h = canvas.height - 1
    c = 3

    # Framerate
    fps  = 100
    rate = 1 / fps

    # Point position and velocity
    x  = numpy.zeros(c)
    y  = numpy.zeros(c)
    vx = numpy.zeros(c)
    vy = numpy.zeros(c)
    for i in range(c):
        x [i] = random.randint(0, w)
        y [i] = random.randint(0, h)
        vx[i] = 0.3 + random.random() * 0.2
        vy[i] = 0.4 + random.random() * 0.1

    # Colour position and velocity
    r  = numpy.zeros(c)
    g  = numpy.zeros(c)
    b  = numpy.zeros(c)
    vr = numpy.zeros(c)
    vg = numpy.zeros(c)
    vb = numpy.zeros(c)
    for i in range(c):
        r [i] = random.random()
        g [i] = random.random()
        b [i] = random.random()
        vr[i] = (random.random() - 0.5) * 0.01
        vg[i] = (random.random() - 0.5) * 0.01
        vb[i] = (random.random() - 0.5) * 0.01

    # And set them going
    last = 0
    while True:
        since = time.time() - last
        while since < rate:
            time.sleep(rate - since)
            since = time.time() - last

        canvas.clear()
        for i in range(c):
            # Move the point
            if x[i] < 0:
                vx[i] =  random.random() * 0.25 + 0.25
            if x[i] > w:
                vx[i] = -random.random() * 0.25 - 0.25
            if y[i] < 0:
                vy[i] =  random.random() * 0.25 + 0.25
            if y[i] > h:
                vy[i] = -random.random() * 0.25 - 0.25
            x[i] += vx[i]
            y[i] += vy[i]

            # Move the colour
            r[i] += vr[i]
            g[i] += vg[i]
            b[i] += vb[i]
            if r[i] < 0 or r[i] > 1.0:
                vr[i] = -vr[i]
            if g[i] < 0 or g[i] > 1.0:
                vg[i] = -vg[i]
            if b[i] < 0 or b[i] > 1.0:
                vb[i] = -vb[i]

            # Display the (big) pixel
            canvas.set(x[i], y[i], r[i], g[i], b[i], 5.0)
        canvas.show()
        last = time.time()

except:
    # Tidy and rethrow
    display.quit()
    canvas.clear()
    canvas.show()
    canvas.quit()
    raise
