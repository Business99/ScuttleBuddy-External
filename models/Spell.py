from pymem import Pymem
from resources import offsets
from functools import cache, cached_property


class Spell:
    def __init__(self, pm: Pymem, spellAddr: int):
        self.pm = pm
        self.spellAddr: int = spellAddr

    @cached_property
    def spellSlots(self) -> int:
        return self.pm.read_int(self.spellAddr + offsets.oSpellSlots)

    @cached_property
    def info(self) -> int:
        return self.pm.read_int(self.spellSlots + offsets.oSpellInfo)

    @cached_property
    def data(self) -> int:
        return self.pm.read_int(self.info + offsets.oSpellInfoData)

    # TODO: Implement this in an outside object such as GameState.py
    @cached_property
    def gameTime(self) -> float:
        return self.pm.read_float(self.pm.base_address + offsets.oGameTime)

    @cached_property
    def readyAt(self) -> float:
        return self.pm.read_float(self.spellSlots + offsets.oSpellReadyAt)

    @cached_property
    def readyIn(self) -> float:
        if (self.readyAt - self.gameTime) > 0:
            return self.readyAt - self.gameTime
        else:
            return 0

    @cached_property
    def level(self) -> int:
        return self.pm.read_int(self.spellSlots + offsets.oSpellLevel)

    @cached_property
    def nameAddr(self) -> int:
        return self.pm.read_int(self.data + offsets.oSpellInfoDataName)

    # TODO: Implement Smite variations, hex flash, and upgraded teleport (Band-aid fix implemented here already)
    @cached_property
    def name(self) -> str:
        result = self.pm.read_string(self.nameAddr)
        if 'Flash' in result:
            return 'SummonerFlash'
        elif 'Teleport' in result:
            return 'SummonerTeleport'
        elif 'Smite' in result:
            return 'SummonerSmite'

        return result

    @cached_property
    def isSummoner(self) -> bool:
        return 'Summoner' in self.name
