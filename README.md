# PixelGames

## Overview

A simple framework for writing games (or whatever) for ultra-low resolution devices. (Here we're talking 16x16, 32x32, etc. _Yeah, ultra low_.)  This is mostly just some display "drivers" sitting along side standard things like [pygame](https://www.pygame.org/).

This is very much toy code but, then again, toys are fun :)


## But, but . . . why?!

Oh, I don't know. Just seemed like a fun challenge to some degree. It's fun to see what you can do with really limited resources and all that.

Right now this is mostly targeting Raspberry Pi devices, and their associated HAT hardware. You can even get something going on a Pi Zero, though it's not exactly speedy.


## What's in the box

At the time of writing the following displays are supported:
 - Colour xterm, or equivalent
 - Pimoroni [Unicorn HAT HD](https://github.com/pimoroni/unicorn-hat-hd)
 - RPi LED Matrix (e.g. from [Adafruit](https://www.adafruit.com/product/3649)

There is a framework for making a game in, with _one whole game_ written for it (a simple PacMan clone).

Finally, there is some example code, for doing simple things with the displays.


## TODO

Well, pretty much everything really. Still, it does kinda work. 