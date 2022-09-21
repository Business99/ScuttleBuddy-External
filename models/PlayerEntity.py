from functools import cached_property
from models import Entity, Spell
from pymem import Pymem


class PlayerEntity(Entity):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def spells(self) -> list[Spell]:
        spells: list = []

        # Handle spells
        spellAddresses: list[int] = []
        j: int = 0
        while j <= 5:
            spellAddresses.append(self.entityAddress + (j * 4))
            j += 1

        i: int = 0
        while i < len(spellAddresses):
            spells.append(Spell(self.pm, spellAddresses[i]))
            i += 1
        return spells

