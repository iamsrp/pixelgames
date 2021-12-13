#!/usr/bin/env python3

from   pixelgames.canvas               import Canvas, Display, NullDisplay
from   pixelgames.canvas.pimoroni      import UnicornHatHD
from   pixelgames.canvas.rgbledmatrix  import RGBLEDMatrix
from   pixelgames.canvas.terminal      import Curses
from   pixelgames.game                 import Game
from   pixelgames.inputs.joysticks     import AtariJoystick
from   random                          import randint
from   typing                          import Tuple

import curses
import logging
import pygame
import time

# ----------------------------------------------------------------------

LOG = logging.getLogger()

# ----------------------------------------------------------------------

class Pacman(Game):
    # Movement
    _UP    = ( 0, -1)
    _DOWN  = ( 0,  1)
    _LEFT  = (-1,  0)
    _RIGHT = ( 1,  0)
    _DIRECTIONS = (_UP, _DOWN, _LEFT, _RIGHT)

    # Keyboard controls
    _CONTROLS = {
        ord('w')        : _UP   ,
        ord('s')        : _DOWN ,
        ord('a')        : _LEFT ,
        ord('d')        : _RIGHT,
        curses.KEY_UP   : _UP   ,
        curses.KEY_DOWN : _DOWN ,
        curses.KEY_LEFT : _LEFT ,
        curses.KEY_RIGHT: _RIGHT
    }

    # The Gird:
    _EMPTY = 0
    _WALL  = 1
    _PILL  = 2
    _EATER = 3
    _EXIT  = 4
    _GRID  = (
      #  0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1
      #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5
        (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), # 00
        (1,2,2,2,2,2,2,1,1,2,2,2,2,2,2,1), # 01
        (1,2,1,1,1,1,2,2,2,2,1,1,1,1,2,1), # 02
        (1,2,3,2,2,1,2,1,1,2,1,2,2,3,2,1), # 03
        (1,1,1,1,2,2,2,1,1,2,2,2,1,1,1,1), # 04
        (1,2,2,2,2,1,1,1,1,1,1,2,2,2,2,1), # 05
        (1,1,2,1,2,2,2,2,2,2,2,2,1,2,1,1), # 06
        (0,0,2,1,1,2,1,4,4,1,2,1,1,2,0,0), # 07
        (0,0,2,2,1,2,1,0,0,1,2,1,2,2,0,0), # 08
        (1,2,1,1,1,2,1,0,0,1,2,1,1,1,2,1), # 09
        (1,2,2,1,2,2,2,1,1,2,2,2,1,2,2,1), # 10
        (1,1,2,1,2,1,2,1,1,2,1,2,1,2,1,1), # 11
        (1,2,2,2,2,1,2,1,1,2,1,2,2,2,2,1), # 12
        (1,2,1,1,1,1,2,0,0,2,1,1,1,1,2,1), # 13
        (1,2,3,2,2,2,2,1,1,2,2,2,2,3,2,1), # 14
        (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1), # 15
    )
    _WIDTH  = len(_GRID[0])
    _HEIGHT = len(_GRID   )

    # How long ghosts can be eaten for (in seconds)
    _GHOST_EAT_TIME   = 10
    _GHOST_EAT_REVERT =  3

    # How many seconds between ghost steps
    _GHOST_STEP_TIME = 0.3

    # The locations where the pacman and ghosts start
    _PACMAN_STARTS = (
        (7, 13), (8, 13),
    )
    _GHOST_STARTS = (
        (7, 8), (8, 8),
        (7, 9), (8, 9),
    )

    # Colours of things
    _PACMAN_COLOUR    =  (1.0, 1.0,   0)
    _GHOST_COLOURS    = ((1.0,   0, 1.0),
                         (1.0,   0, 1.0),
                         (1.0,   0, 1.0),
                         (1.0,   0, 1.0),)
    _GHOST_EAT_COLOUR = (  0, 1.0, 1.0)
    _GRID_COLOURS     = ((  0,   0,   0),  # Empty
                         (  0,   0, 1.0),  # Wall
                         (0.5,   0,   0),  # Pill
                         (1.0, 1.0, 1.0),  # Ghost eating pill
                         (  0,   0, 0.5),) # Ghost start exit

    def __init__(self,
                 display : Display) -> None:
        """
        CTOR

        :param display: The `Display` instance to use.
        """
        # Create using an appropriate canvas
        super(Pacman, self).__init__(
            Canvas(display, width=self._WIDTH, height=self._HEIGHT),
            scr=getattr(display, 'curses_screen', None)
        )

        # Copy the grid in. We have to switch from row-major to column-major for
        # [x,y] access to work here.
        self._grid = [[0] * self._HEIGHT for i in range(self._WIDTH)]
        for x in range(self._WIDTH):
            for y in range(self._HEIGHT):
                self._grid[x][y] = self._GRID[y][x]

        # Frameworks
        self._pygame = None
        self._scr    = None

        # State
        self._ghost_posns = None
        self._ghost_moves = None
        self._ghost_times = None
        self._pacman_posn = None
        self._score       = None
        self._eating_time = None

        # Controls
        self._joystick = None


    def _init(self,
              game : pygame,
              scr) -> None:
        """
        Set up the game state.
        """
        scr.nodelay(True)
        scr.noecho()

        self._pygame = game
        self._scr    = scr

        self._ghost_posns = [list(self._GHOST_STARTS[i % len(self._GHOST_STARTS)])
                             for i in range(len(self._GHOST_COLOURS))]
        self._ghost_moves = [self._DIRECTIONS[randint(0, len(self._DIRECTIONS)-1)]
                             for i in range(len(self._ghost_posns))]
        self._ghost_times = [0 for i in range(len(self._ghost_posns))]
        self._pacman_posn = list(self._PACMAN_STARTS[0])
        self._score       = 0
        self._eating_time = 0

        # We might not have a joystick attached
        try:
            self._joystick = AtariJoystick(game)
            LOG.debug("Got a joystick %s", self._joystick)
        except ValueError:
            pass


    def _update(self,
                now    : float,
                events : Tuple) -> bool:
        """
        A tick of the clock.
        """
        LOG.debug("Events %s", events)

        # Draw the display
        self._canvas.clear()

        # The static parts of the grid. And count any pills at the same time
        has_pill = False
        for x in range(len(self._grid)):
            for y in range(len(self._grid[x])):
                try:
                    e = self._grid[x][y]
                    (r, g, b) = self._GRID_COLOURS[e]
                    self._canvas.set(x, y, r, g, b)
                    if e in (self._PILL, self._EATER):
                        has_pill = True
                except IndexError:
                    pass

        # No pills means that we're done
        if not has_pill:
            return True

        # Now handle joystick input
        xd = 0
        yd = 0
        if self._joystick:
            # Defer to the joystick first
            (jx, jy) = self._joystick.get_direction()
            if jx != 0 or jy != 0:
                LOG.debug("Joystick %d %d", xd, yd)
                if jx < 0:
                    xd = -1
                elif jx > 0:
                    xd = 1
                if jy < 0:
                    yd = 1
                elif jy > 0:
                    yd = -1

        # Always check the keyboard
        key = 0
        while key != -1:
            key = self._scr.getch()
            if key in self._CONTROLS:
                (xd, yd) = self._CONTROLS[key]

        # Where are we going, who knows...
        LOG.debug("Direction %d %d", xd, yd)

        # Move pacman?
        (px, py) = (self._pacman_posn[0] + xd,
                    self._pacman_posn[1] + yd)
        if px < 0:
            px += len(self._grid)
        elif px >= len(self._grid):
            px -= len(self._grid)
        elif py < 0:
            py += len(self._grid[0])
        elif py >= len(self._grid[0]):
            py -= len(self._grid[0])
        if self._grid[px][py] not in (self._WALL, self._EXIT):
            self._pacman_posn[0] = px
            self._pacman_posn[1] = py

        # What did pacman eat, if anything
        e = self._grid[self._pacman_posn[0]][self._pacman_posn[1]]
        if e == self._PILL:
            self._score += 1
        elif e == self._EATER:
            self._eating_time = now

        # Whether ghosts can be eaten
        eating = now - self._eating_time < self._GHOST_EAT_TIME

        # Move the ghosts
        for i in range(len(self._ghost_posns)):
            # Too soon?
            if now - self._ghost_times[i] < self._GHOST_STEP_TIME:
                continue

            # Try to move the ghost
            while True:
                # Current state
                (px, py) = self._ghost_posns[i]
                (dx, dy) = self._ghost_moves[i]

                # First see if the ghost might want to change direction
                # because of a junction
                for d in self._DIRECTIONS:
                    # See if it's a change and not a reversal
                    if ((d[0] == dx and d[1] == dy) and
                        (d[0] !=  0 and d[0] == -dx or
                         d[1] !=  0 and d[1] == -dy)):
                        continue

                    # See if it will hit the wall
                    nx = px + d[0]
                    ny = py + d[1]
                    if (nx < 0 or nx >= len(self._grid   ) or
                        ny < 0 or ny >= len(self._grid[0]) or
                        self._grid[nx][ny] == self._WALL):
                        continue

                    # See if we want to choose it
                    if randint(0, 1):
                        self._ghost_moves[i] = d
                        (dx, dy)       = d
                        break

                # Now move the ghost
                nx = px + dx
                ny = py + dy
                if nx < 0:
                    nx += len(self._grid)
                elif nx >= len(self._grid):
                    nx -= len(self._grid)
                elif ny < 0:
                    ny += len(self._grid[0])
                elif ny >= len(self._grid[0]):
                    ny -= len(self._grid[0])
                # See if it will hit to wall (or, if can be eaten, the exit
                # since we don't want them to leave in that case).
                if (self._grid[nx][ny] != self._WALL and
                    (not eating or self._grid[nx][ny] != self._EXIT)):
                    self._ghost_posns[i][0] = nx
                    self._ghost_posns[i][1] = ny
                    self._ghost_times[i]    = now
                    break
                else:
                    self._ghost_moves[i] = self._DIRECTIONS[randint(0, len(self._DIRECTIONS)-1)]

        # Whatever was there is now wiped out
        self._grid[self._pacman_posn[0]][self._pacman_posn[1]] = self._EMPTY

        # Draw pacman and the ghosts
        for i in range(len(self._ghost_posns)):
            # The colour of the ghosts will be eatable if we are eating, but
            # we flash we as get close to reverting to normal
            if (eating and
                (now - self._eating_time < (self._GHOST_EAT_TIME - self._GHOST_EAT_REVERT) or
                 (int(now * 10) % 2) == 0)):
                (r, g, b) = self._GHOST_EAT_COLOUR
            else:
                (r, g, b) = self._GHOST_COLOURS[i]
            (x, y) = self._ghost_posns[i]
            self._canvas.set(x, y, r, g, b)
        (x, y)    = self._pacman_posn
        (r, g, b) = self._PACMAN_COLOUR
        self._canvas.set(x, y, r, g, b)

        # And display it all
        self._canvas.show()

        # See if pacman met a ghost
        for (i, (x, y)) in enumerate(self._ghost_posns):
            if self._pacman_posn[0] == x and self._pacman_posn[1] == y:
                if eating:
                    # The ghost was eaten, put it back to the start
                    self._score += 20
                    self._ghost_posns[i][0] = self._GHOST_STARTS[i][0]
                    self._ghost_posns[i][1] = self._GHOST_STARTS[i][1]
                else:
                    # Oh dear, the ghost ate pacman. We're done
                    return True

        # Not yet done
        return False


    def _quit(self) -> None:
        # Best effort
        try:
            scr.nodelay(False)
            scr.echo()
            self._joystick.close()
        except:
            pass

        # What did you get?
        print('You scored: {}\n'.format(self._score))

# ----------------------------------------------------------------------

if __name__ == '__main__':
    #LOG.setLevel('DEBUG')
    display = Curses()
    #display = NullDisplay(64, 64)
    game = Pacman(display)
    game.start()
