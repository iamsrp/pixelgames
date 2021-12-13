"""
Inputs from the joystick.
"""

from .      import SimpleJoystick
from math   import copysign
from typing import Tuple

# ----------------------------------------------------------------------

class AtariJoystick(SimpleJoystick):
    """
    A joystick which looks like the standard Atari one. Simple axes and one
    button.
    """
    def __init__(self, pygame):
        self._pygame = pygame
        pygame.joystick.init()

        # All the joysticks which we know about
        joysticks = [pygame.joystick.Joystick(i)
                     for i in range(pygame.joystick.get_count())]

        # Just pick the first working one for now, and set it up
        self._joystick = None
        for joystick in joysticks:
            try:
                # Set it up
                self._joystick = joystick
                self._joystick.init()

                # And make sure it has the bits which we need
                if self._joystick.get_numbuttons() > 0 and \
                   (self._joystick.get_numaxes() >= 2 or
                    self._joystick.get_numhats() > 0):
                    break
            except:
                # Best effort clean-up
                try:
                    joystick.quit()
                except:
                    pass

        # Anything?
        if self._joystick is None:
            raise ValueError("No good joysticks found")


    def get_num_buttons(self) -> int:
        return 1


    def is_button_pressed(self, index: int) -> bool:
        # We only have one button (honest!)
        if index != 0:
            return False

        # We say yes for any button pressed
        for i in range(self._joystick.get_numbuttons()):
            if self._joystick.get_button(i):
                return True
        return False


    def get_direction(self) -> Tuple[int,int]:
        # We will give back the X and Y values. We make these compound based on
        # all the inputs which we can find.
        x = 0
        y = 0

        # Poll the hats, if any
        for i in range(self._joystick.get_numhats()):
            # These are -1, 0, +1 value
            (hx, hy) = self._joystick.get_hat(i)
            x += hx
            y += hy

        # Now any axes
        for i in range(self._joystick.get_numaxes()):
            # Get the value of the axis and apply it to the x or y value. x is
            # even, y is odd (and its value is inverted).
            value = int(round(self._joystick.get_axis(i)))
            if (i & 1) == 0:
                x += value
            else:
                # The Y-axis is inverted
                y -= value

        # And give back the values, capped at -1 and +1
        return (max(-1, min(1, x)),
                max(-1, min(1, y)))


    def quit(self) -> None:
        # Shut it all down
        self._joystick       .quit()
        self._pygame.joystick.quit()
