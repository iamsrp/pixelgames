#!/usr/bin/env python3
"""
A simple test game.
"""

# ======================================================================

from   pixelgames.game                 import Game
from   pixelgames.canvas               import Canvas
from   pixelgames.canvas.pimoroni      import UnicornHatHD
from   pixelgames.canvas.rgbledmatrix  import RGBLEDMatrix
from   pixelgames.canvas.terminal      import Curses
from   pixelgames.inputs.joysticks     import AtariJoystick
from   typing                          import Tuple

# ======================================================================

class SimpleGame(Game):
    """
    A simple game for testing with
    """
    def __init__(self, display):
        super().__init__(Canvas(display, xwrap=True, ywrap=True))

        # Limits
        self._w = display.width  - 1
        self._h = display.height - 1

        # Point position, size and colour
        self._x = int(self._w / 2)
        self._y = int(self._h / 2)
        self._s = 2
        self._r = 0.5
        self._g = 0.5
        self._b = 0.5

        # No bigger than this
        self._mx = min(self._w, self._h) / 2

        # Created later
        self._joystick = None

        # Last update time
        self._lasttime = 0


    def _init(self, pygame) -> None:
        """
        Set up.

        :param game: The PyGame instance.
        """
        self._joystick = AtariJoystick(pygame)


    def _update(self,
                now:    float,
                events: Tuple[object]) -> None:
        """
        Another iteration.

        :param now   : The current time, in seconds since epoch.
        :param events: PyGame events since the last update.
        """
        # Not too quick
        if now - self._lasttime < 0.01:
            return
        else:
            self._lasttime = now

        # Get the joystick state
        (jx, jy) = self._joystick.get_direction()
        jb       = self._joystick.is_button_pressed(0)

        # Different actions depending on whether the button is pressed or not
        if not jb:
            # Move the point?
            if   jx < 0 and self._x > 0:
                self._x -= 0.1
            elif jx > 0 and self._x+1 < self._w:
                self._x += 0.1
            if   jy < 0 and self._y > 0:
                self._y -= 0.1
            elif jy > 0 and self._y+1 < self._h:
                self._y += 0.1
        else:
            # Change the size of the point or the colour
            if   jx < 0 and self._s > 1:
                self._s -= 1
            elif jx > 0 and self._s < self._mx:
                self._s += 1
            elif jy < 0 and self._r > 0:
                self._r -= 0.1
            elif jy > 0 and self._r < 1:
                self._r += 0.1

        # Display the (big) pixel
        self._canvas.clear()
        self.canvas.set(self._x,
                        self._h - self._y,
                        self._r,
                        self._g,
                        self._b,
                        self._s)
        self._canvas.show()


    def _quit(self):
        self._joystick.quit()

# ==============================================================================

if __name__ == "__main__":
    display = Curses() # RGBLEDMatrix() # UnicornHatHD()
    game    = SimpleGame(display)
    game.start()
