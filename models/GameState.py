from functools import cached_property
from pymem import Pymem
from resources import Offsets


class GameState:
    def __init__(self, pm: Pymem):
        self.pm = pm

    @cached_property
    def gameTime(self) -> float:
        return self.pm.read_float(self.pm.base_address + Offsets.oGameTime)

