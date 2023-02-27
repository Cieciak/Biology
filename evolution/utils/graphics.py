from .math import Vector, tkiner_color
from tkinter import Canvas

# {"type": "Being",
#  "position": {"x": 0.0, "y": 0.0},
#  "size": {"x": 20,"y": 20},
#  "other": {...}
# }

class RenderBeing:

    @classmethod
    def fromDict(cls, data: dict):
        position = Vector(**data['position'])
        size     = Vector(**data['size'])
        other    = data['other']

        return cls(position, size, other)

    def __init__(self, position: Vector, size: Vector, other = {}) -> None:
        self.position = position
        self.size = size
        self.other = other

    def draw(self, canvas: Canvas):
        dx, dy = tuple(canvas.global_offset)
        if canvas.max > canvas.render_offset.manhattan(self.position):
            canvas.create_rectangle(self.position.x - self.size.x / 2 + dx,
                                    self.position.y - self.size.y / 2 + dy,
                                    self.position.x + self.size.x / 2 + dx,
                                    self.position.y + self.size.y / 2 + dy,
                                    fill = tkiner_color((self.other['red']*128, self.other['green']*128, self.other['blue']*128)))

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
                               width = 2)