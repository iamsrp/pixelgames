"""
Pimoroni displays.
"""

from   typing import Tuple
from   .      import Display

# ----------------------------------------------------------------------

class UnicornHatHD(Display):
    """
    The 16x16 RGB Unicorn HAT.
    """
    def __init__(self):
        import unicornhathd
        self._display = unicornhathd


    def get_shape(self) -> Tuple[int,int]:
        return self._display.get_shape()


    def set_orientation(self, orientation: int) -> None:
        self._display.rotation(orientation)


    def clear(self):
        self._display.clear()


    def set(self,
            x: int,
            y: int,
            r: float,
            g: float,
            b: float) -> None:
        # Bounds check since the call with throw otherwise
        w = self._display.get_shape()[0]
        h = self._display.get_shape()[1]
        if 0 <= x < w and 0 <= y < h:
            # Okay to set
            self._display.set_pixel(
                x,
                y,
                int(255 * min(max(r, 0.0), 1.0)),
                int(255 * min(max(g, 0.0), 1.0)),
                int(255 * min(max(b, 0.0), 1.0))
            )


    def show(self):
        self._display.show()
