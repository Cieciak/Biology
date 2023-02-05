from .math import Vector
from tkinter import Canvas

class RenderBeing:

    @classmethod
    def fromDict(cls, data: dict):
        position = Vector(**data['position'])
        size     = Vector(**data['size'])

        return cls(position, size)

    def __init__(self, position: Vector, size: Vector) -> None:
        self.position = position
        self.size = size

    def draw(self, canvas: Canvas):
        dx, dy = tuple(canvas.global_offset)
        if canvas.max > canvas.render_offset.manhattan(self.position):
            canvas.create_rectangle(self.position.x - self.size.x / 2 + dx,
                                    self.position.y - self.size.y / 2 + dy,
                                    self.position.x + self.size.x / 2 + dx,
                                    self.position.y + self.size.y / 2 + dy,
                                    fill = '#D68915')