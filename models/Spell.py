from pymem import Pymem
from resources import offsets


class Spell:
    def __init__(self, pm: Pymem, spellAddr: int):
        self.pm = pm
        self.spellAddr: int = spellAddr

        self.name: str = None
        self.infoName: str = None
        self.readyAt: float = 0
        self.level: int = 0
        self.isReady: bool = False
        self.readyIn: float = 0
        self.isSummoner: bool = False

        self.update()

    def update(self):
        spellSlots: int = self.pm.read_int(self.spellAddr + offsets.oSpellSlots)
        gameTime: float = self.pm.read_float(self.pm.base_address + offsets.oGameTime)

        self.readyAt = self.pm.read_float(spellSlots + offsets.oSpellReadyAt)

        if (self.readyAt - gameTime) > 0:
            self.readyIn = self.readyAt - gameTime
        else:
            self.readyIn = 0

        info: int = self.pm.read_int(spellSlots + offsets.oSpellInfo)
        data: int = self.pm.read_int(info + offsets.oSpellInfoData)

        nameAddr: int = self.pm.read_int(data + offsets.oSpellInfoDataName)
        self.name = self.pm.read_string(nameAddr)

        if 'Flash' in self.name:
            self.name = 'SummonerFlash'
        elif 'Teleport' in self.name:
            self.name = 'SummonerTeleport'
        elif 'Smite' in self.name:
            self.name = 'SummonerSmite'

        self.level = self.pm.read_int(spellSlots + offsets.oSpellLevel)

        if 'Summoner' in self.name:
            self.isSummoner = True