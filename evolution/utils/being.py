from math import exp
from .math import Vector
from tkinter import Tk


    # def update(self, ctx: tkinter.Tk, dt: float):
    #     self.make_decision(ctx, dt)

    #     self.force = self.flap_force * Being.time_coeff(self.since_flap) + Vector2(0, 90)

    #     prev_acceleration = self.acceleration
    #     self.acceleration = self.force / self.mass
    #     self.position += self.velocity * dt + .5 * prev_acceleration * dt ** 2
    #     self.velocity += .5 *(self.acceleration + prev_acceleration) * dt

    #     self.since_flap += dt

class Being:

    @staticmethod
    def time_coeff(t: float):
        return exp(-(4*t -2)**2)

    def __init__(self, position: Vector) -> None:
        self.position: Vector = position         # [m]
        self.velocity: Vector = Vector(0, 0)     # [m/s]
        self.acceleration: Vector = Vector(0, 0) # [m/s^2]
        self.force: Vector = Vector(0, 0)        # [N]

        self.vertical_force: Vector  = Vector(0, 90)
        self.horizontal_force: Vector = Vector(40, 0)
        self.since_flap: float = 1e10

        self.mass: float = 1.0

    def make_decision(self, ctx: Tk, dt: float):
        if self.since_flap > 1:
            self.since_flap = 0

    def update(self, ctx: Tk, dt: float):
        self.make_decision(ctx, dt)

        self.force = self.vertical_force * Being.time_coeff()