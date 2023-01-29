from typing import Self
from tkinter import Canvas, Tk

class Vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'({self.x}, {self.y})'

    def __add__(self, other: Self):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other: float):
        return self * other

    def __truediv__(self, other: float):
        return Vector(self.x / other, other.y / other)

    def __round__(self, n: int):
        return Vector(round(self.x, n), round(self.y, n))

    def __iter__(self):
        for val in [self.x, self.y]: yield val

    def manhattan(self, other: Self) -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def update(self, ctx: Tk, dt: float):
        pass

    def draw(self, canvas: Canvas):
        dx, dy = tuple(canvas.global_offset)
        canvas.create_oval(self.x + dx, self.y + dy, self.x + dx, self.y + dy)