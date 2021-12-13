"""
Classes and functions for handling inputs.
"""

# ======================================================================

from abc    import ABC, abstractmethod
from typing import Tuple

# ======================================================================

class SimpleJoystick(ABC):
    """
    Base class for handling basic joystick inputs.
    """
    @abstractmethod
    def get_num_buttons(self) -> int:
        """
        Get the number of buttons.
        """
        return 0


    @abstractmethod
    def is_button_pressed(self, index: int) -> bool:
        """
        Whether the button with the given index is pressed or not.
        """
        return False


    @abstractmethod
    def get_direction(self) -> Tuple[int,int]:
        """
        Return a tuple of (X,Y) direction, with values being -1, 0, or +1.
        """
        return (0,0)


    @abstractmethod
    def quit(self) -> None:
        """
        Be done with this joystick.
        """
        pass
