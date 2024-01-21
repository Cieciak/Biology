from typing import Any, Callable
from .organism import Organism
from .profile import Profile

class CreatorContext:

    def __init__(self) -> None:    
        self.stack: list = []
        self.accumulator: int = 0
        self.properties: dict[int, Any] = {}

class Creator:

    def __init__(self, profile: Profile, microcode: dict[str, Callable]):
        self.profile = profile
        self.microcode = microcode

    def make(self, executable: str) -> dict[int, Any]:
        ctx = CreatorContext()

        while executable:
            codon:      str = executable[:3]
            executable: str = executable[3:]

            amino = self.profile.codons[codon]

            action = self.microcode[amino]

            result = action(ctx)
            if result: ctx = result

        return ctx.properties


def ZER_action(ctx: CreatorContext) -> CreatorContext:
    ctx.accumulator *= 2

    return ctx

def ONE_action(ctx: CreatorContext) -> CreatorContext:
    ctx.accumulator *= 2
    ctx.accumulator += 1

    return ctx

def KEY_action(ctx: CreatorContext) -> CreatorContext:
    ctx.stack += [ctx.accumulator]
    ctx.accumulator = 0

    return ctx

def VAL_action(ctx: CreatorContext) -> CreatorContext:
    ctx.stack += [ctx.accumulator]
    ctx.accumulator = 0

    val = ctx.stack.pop()
    key = ctx.stack.pop()

    ctx.properties[key] = val


A = {
    'START': lambda x: None,
    'STOP': lambda x: None,
    'KEY': KEY_action,
    'VAL': VAL_action,
    'DOM': lambda c: None,
    'ZER': ZER_action,
    'ONE': ONE_action,
}

class Being:

    def __init__(self):
        self.properties = {}