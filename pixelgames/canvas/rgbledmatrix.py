"""
LED matrix displays.
"""

from   typing import Tuple
from   .      import Display

# ----------------------------------------------------------------------

class RGBLEDMatrix(Display):
    """
    A RGB LED matrix, driven by the Pi RGB LED Matrix software.

    # Some options are needed to make things work okay with a Pi4.
    
    https://github.com/hzeller/rpi-rgb-led-matrix
    """
    def __init__(self,
                 rows         =32,
                 columns      =32,
                 chain_length =1,
                 gpio_slowdown=2,
                 hw_pulsing   =False):
        from rgbmatrix import RGBMatrix, RGBMatrixOptions
        options = RGBMatrixOptions()
        options.rows                     = int(rows)
        options.cols                     = int(columns)
        options.chain_length             = int(chain_length)
        options.gpio_slowdown            = int(gpio_slowdown)
        options.disable_hardware_pulsing = not hw_pulsing
        self._matrix = RGBMatrix(options=options)
        self._canvas = self._matrix.CreateFrameCanvas()


    def get_shape(self) -> Tuple[int,int]:
        return (self._matrix.width, self._matrix.height)


    def set_orientation(self, orientation: int) -> None:
        raise NotImplementedError()


    def clear(self):
        self._canvas.Clear()


    def set(self,
            x: int,
            y: int,
            r: float,
            g: float,
            b: float) -> None:
        # Bounds check since the call with throw otherwise
        if 0 <= x < self._matrix.width and 0 <= y < self._matrix.height:
            # Okay to set
            self._canvas.SetPixel(
                x,
                y,
                int(255 * min(max(r, 0.0), 1.0)),
                int(255 * min(max(g, 0.0), 1.0)),
                int(255 * min(max(b, 0.0), 1.0))
            )


    def show(self):
        self._canvas = self._matrix.SwapOnVSync(self._canvas)
