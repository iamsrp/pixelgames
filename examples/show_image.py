#!/usr/bin/env python3
"""
Display an image.
"""

from   pixelgames.canvas               import Canvas, NullDisplay
from   pixelgames.canvas.pimoroni      import UnicornHatHD
from   pixelgames.canvas.rgbledmatrix  import RGBLEDMatrix
from   pixelgames.canvas.terminal      import Curses
from   PIL                             import Image

import sys
import time

# Args?
if len(sys.argv) != 2:
    print("Usage: %s <image>" % sys.argv[0])
    sys.exit(1)

# What we display on
#display = NullDisplay(64, 64)
display = Curses()
#display = RGBLEDMatrix()
#display = UnicornHatHD()
canvas  = Canvas(display, xwrap=False, ywrap=False)

try:
    # Load in the image
    image = Image.open(sys.argv[1])

    # Display the image
    canvas.set_image(image)
    canvas.show()

    # Wait for a bit
    time.sleep(60)

finally:
    # Tidy and rethrow
    canvas.clear()
    canvas.show()
    canvas.quit()
