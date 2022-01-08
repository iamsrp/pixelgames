"""
Displays which use Python's PIL to drive them.
"""

from   PIL    import Image
from   typing import Tuple
from   .      import Display

# ----------------------------------------------------------------------

class _PIL(Display):
    """
    The base class for thre PIL-based displays.
    """
    def __init__(self,
                 width  : int,
                 height : int):
        """
        :param width:  The display width.
        :param height: The display height.
        """
        self._image = Image.new('RGB',
                                (int(width), int(height)),
                                color=(0,0,0))
        self._clear = (b'\x00' *
                       self._image.width *
                       self._image.height *
                       3)
        self._orientation = 0


    def get_shape(self) -> Tuple[int,int]:
        return self._image.size


    def set_orientation(self, orientation: int) -> None:
        if orientation not in (0, 90, 180, 270):
            raise ValueError("Bad orientation: %s" % (orientation,))
        self._orientation = orientation


    def clear(self):
        self._image.frombytes(self._clear)


    def set(self,
            x: int,
            y: int,
            r: float,
            g: float,
            b: float) -> None:
        if   self._orientation ==   0:
            dx = x
            dy = y
        elif self._orientation ==  90:
            dx = y
            dy = x
        elif self._orientation == 180:
            dx = self._image.width  - x
            dy = self._image.height - y
        elif self._orientation == 270:
            dx = self._image.width  - y
            dy = self._image.height - x
        else:
            raise ValueError("Bad orientation: %s" % (self._orientation,))

        # Bounds check since the call with throw otherwise
        if 0 <= dx < self._image.width and 0 <= dy < self._image.height:
            # Okay to set
            self._image.putpixel(
                (dx, dy),
                (int(255 * min(max(r, 0.0), 1.0)),
                 int(255 * min(max(g, 0.0), 1.0)),
                 int(255 * min(max(b, 0.0), 1.0)))
            )


    def show(self):
        # Subclasses must implement this
        raise NotImplementedError()


class ST7789TFT(_PIL):
    """
    The display for a Pimoroni ST7789 TFT display.

    See https://github.com/pimoroni/st7789-python
    """
    def __init__(self,
                 width  : int = 240,
                 height : int = 240):
        super(ST7789TFT, self).__init__(width, height)

        import ST7789

        self._display = disp = ST7789.ST7789(
            width       =width,
            height      =height,
            port        =0,
            cs          =ST7789.BG_SPI_CS_FRONT,
            dc          =9,
            backlight   =19,
            rotation    =90,
            spi_speed_hz=80 * 1000 * 1000,
            offset_left =0,
            offset_top  =0
        )
        self._display.begin()


    def show(self) -> None:
        self._display.display(self._image)


    def quit(self) -> None:
        super(ST7789TFT, self).quit()
        self._display.reset()
