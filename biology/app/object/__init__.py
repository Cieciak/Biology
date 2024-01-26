from .dummy import Dummy
from .being import Being

type SimObject = Dummy | Being

class Frame(list):

    def draw(self, ctx):

        for obj in self:
            obj.draw(ctx)