from ..math import Vector, RGB, tkiner_color
from tkinter import Canvas

from typing import Callable, Self, Any

class Dummy:

    def __init__(self, position: Vector, color: RGB, *, updater: Callable[[Self], Self] = lambda D, t, s: D):
        self.position = position
        self.color    = color
        self.updater  = updater

    def draw(self, canvas: Canvas):
        if canvas.render_offset.taxicab(self.position) > canvas.max: return

        dx, dy = tuple(canvas.global_offset)
        canvas.create_oval(self.position.x - 5 + dx,
                           self.position.y - 5 + dy,
                           self.position.x + 5 + dx,
                           self.position.y + 5 + dy,
                           fill = tkiner_color(self.color),)
        
    def update(self, dt: float, sim: Any):
        self = self.updater(self, dt, sim)