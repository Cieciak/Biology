from .math import Vector
from tkinter import Canvas

# {"type": "Being",
#  "position": {"x": 0.0, "y": 0.0},
#  "size": {"x": 20,"y": 20},
# }

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

# {"type": "PoinOfInterest",
#  "position": {"x": 0.0, "y": 0.0},
#  "size": {"x": 20,"y": 20},
#  "color": "#345443"
# }

class PointOfInterest:

    @classmethod
    def fromDict(cls, data: dict):
        position = Vector(**data['position'])
        size     = Vector(**data['size'])
        color    = data['color']

        return cls(position, size, color)

    def __init__(self, position: Vector, size: Vector, color: str) -> None:
        self.position = position
        self.size = size
        self.color = color

    def draw(self, canvas: Canvas):
        dx, dy = tuple(canvas.global_offset)
        if canvas.max > canvas.render_offset.manhattan(self.position):
            canvas.create_oval(self.position.x - self.size.x / 2 + dx,
                               self.position.y - self.size.y / 2 + dy,
                               self.position.x + self.size.x / 2 + dx,
                               self.position.y + self.size.y / 2 + dy,
                               fill = self.color,
                               width = 5)