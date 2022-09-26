from pymem import Pymem
from functools import cached_property
from resources import offsets


class Buff:
    def __init__(self, pm: Pymem, entityAddress: int):
        self.pm = pm
        self.entityAddress = entityAddress

    @cached_property
    def __entry(self):
        return self.pm.read_int(self.entityAddress + offsets.BuffEntryBuff)

    @cached_property
    def type(self):
        return self.pm.read_int(self.entityAddress + offsets.BuffType)