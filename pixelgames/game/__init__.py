"""
Classes and functions for the main game functionality.
"""

# ======================================================================

from   abc    import ABC, abstractmethod
from   typing import Tuple

import curses
import math
import pygame
import time

# ======================================================================

class Game(ABC):
    """
    The parent class for all games.
    """
    def __init__(self,
                 canvas,
                 scr         = None,
                 fps : float = math.inf) -> None:
        """
        Set up the game with the given Canvas.

        :param canvas: The Canvas instance.
        :param scr:    
        :param fps:    The max number of frames per second
        """
        self._canvas = canvas
        self._tween  = 1.0 / max(0.01, float(fps))
        self._scr    = scr

        # State
        self._keys_pressed = set()


    def start(self) -> None:
        """
        Start the game.
        """
        try:
            # Set up and run
            self.__init_main()
            self.__run()
        finally:
            # And we're done
            self.__quit_main()


    @property
    def canvas(self):
        """
        Get the canvas.
        """
        return self._canvas

    # ----------------------------------------------------------------------

    @abstractmethod
    def _init(self,
              game : pygame,
              scr) -> None:
        """
        Set up.

        :param game: The PyGame instance.
        """
        pass


    @abstractmethod
    def _update(self,
                now:    float,
                events: Tuple[object]) -> None:
        """
        Another iteration.

        :param now   : The current time, in seconds since epoch.
        :param events: PyGame events since the last update.

        :return: Whether the game is done
        """
        pass


    @abstractmethod
    def _quit(self) -> None:
        """
        Shut down.
        """
        pass

    # ----------------------------------------------------------------------

    def __init_main(self) -> None:
        """
        Set everything up.
        """
        if self._scr is None:
            self._scr = curses.initscr()
        pygame.init()
        self._init(pygame, self._scr)

 
    def __quit_main(self) -> None:
        """
        Shut down the game.
        """
        try:
            self._quit()
        except:
            pass

        try:
            self._canvas.quit()
        except:
            pass

        try:
            pygame.quit()
        except:
            pass

        try:
            curses.endwin()
        except:
            pass
        


    def __run(self) -> None:
        """
        Set the game running.
        """
        # State
        last_time = 0
        events    = []

        # Update forever (ish)!
        while True:
            # Don't update too fast
            since = time.time() - last_time
            if since < self._tween:
                time.sleep(max(0, self._tween - since))
                continue

            # Update the game
            if self._update(time.time(), tuple(pygame.event.get())):
                # We're done
                break

            # We iterated
            last_time = time.time()
