from typing import Self

class Vector:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'({self.x}; {self.y})'

    def __add__(self, other: Self):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other: float):
        return self * other

    def __truediv__(self, other: float):
        return Vector(self.x / other, self.y / other)

    def __round__(self, n: int):
        return Vector(round(self.x, n), round(self.y, n))

    def __iter__(self):
        for val in [self.x, self.y]: yield val

    def __abs__(self): return (self.x ** 2 + self.y ** 2) ** .5

    def taxicab(self, other: Self) -> float:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def dot(self, other: Self):
        return self.x * other.x + self.y * other.y

    def update(self, ctx, dt: float):
        pass

    def draw(self, canvas):
        dx, dy = tuple(canvas.global_offset)
        canvas.create_oval(self.x + dx, self.y + dy, self.x + dx, self.y + dy)    