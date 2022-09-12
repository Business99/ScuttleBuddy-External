import pymeow
from pymem import Pymem
from models.Spell import Spell
from resources import offsets
from functools import cache


class PlayerEntity:
    def __init__(self, pm, mem, overlay, viewProjMatrix, entityAddress: int):
        self.pm = pm
        self.mem = mem
        self.overlay = overlay
        self.viewProjMatrix = viewProjMatrix
        self.entityAddress = entityAddress

    @property
    def championName(self) -> str:
        nameAddr: int = self.pm.read_int(self.entityAddress + offsets.oObjName)
        return self.pm.read_string(nameAddr)

    @property
    def level(self) -> int:
        return self.pm.read_int(self.entityAddress + offsets.oObjLevel)

    @property
    def teamId(self) -> int:
        return self.pm.read_int(self.entityAddress + offsets.oObjTeamId)

    @property
    def health(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjHealth)

    @property
    def maxHealth(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMaxHealth)

    @property
    def mana(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMana)

    @property
    def maxMana(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMaxMana)

    @property
    def ap(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjStatAp)

    @property
    def ad(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjStatBaseAd) + self.pm.read_float(self.entityAddress + offsets.oObjStatBonusAd)

    @property
    def magicResist(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMagicRes)

    @property
    def armor(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjArmor)

    @property
    def magicPenFlat(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMagicPenFlat)

    @property
    def magicPenPercent(self) -> float:
        return (1 - self.pm.read_float(self.entityAddress + offsets.oObjMagicPenPercent)) * 100

    @property
    def armorPenPercent(self) -> float:
        return (1 - self.pm.read_float(self.entityAddress + offsets.oObjArmorPen)) * 100

    @property
    def lethality(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjLethality)

    @property
    def attackRange(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjStatAttackRange)

    @property
    def gamePos(self) -> dict:
        return pymeow.read_vec3(self.mem, self.entityAddress + offsets.oObjPosition)

    @property
    def screenPos(self) -> dict:
        try:
            wts = pymeow.wts_ogl(self.overlay, self.viewProjMatrix.tolist(), self.gamePos)
        except:
            wts = pymeow.vec2()
        return wts

    @property
    def isVisible(self) -> bool:
        return self.pm.read_bool(self.entityAddress + offsets.oObjVisible)

    @property
    def onScreen(self):
        return self.screenPos['x'] > 0 and self.screenPos['x'] < self.overlay['width'] and self.screenPos['y'] > 0 and self.screenPos['y'] < self.overlay['height']

    @property
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
