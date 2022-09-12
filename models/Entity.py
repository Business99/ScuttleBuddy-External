import pymeow
from models.Spell import Spell
from resources import offsets
from functools import cached_property


class Entity:
    def __init__(self, pm, mem, overlay, viewProjMatrix, entityAddress: int) -> None:
        self.pm = pm
        self.mem = mem
        self.overlay = overlay
        self.viewProjMatrix = viewProjMatrix
        self.entityAddress = entityAddress

    @cached_property
    def champNameAddr(self) -> int:
        return self.pm.read_int(self.entityAddress + offsets.oObjName)

    @cached_property
    def name(self) -> str:
        return self.pm.read_string(self.champNameAddr)

    @cached_property
    def level(self) -> int:
        return self.pm.read_int(self.entityAddress + offsets.oObjLevel)

    @cached_property
    def teamId(self) -> int:
        return self.pm.read_int(self.entityAddress + offsets.oObjTeamId)

    @cached_property
    def health(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjHealth)

    @cached_property
    def maxHealth(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMaxHealth)

    @cached_property
    def mana(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMana)

    @cached_property
    def maxMana(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMaxMana)

    @cached_property
    def ap(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjStatAp)

    @cached_property
    def ad(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjStatBaseAd) + self.pm.read_float(self.entityAddress + offsets.oObjStatBonusAd)

    @cached_property
    def magicResist(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMagicRes)

    @cached_property
    def armor(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjArmor)

    @cached_property
    def magicPenFlat(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjMagicPenFlat)

    @cached_property
    def magicPenPercent(self) -> float:
        return (1 - self.pm.read_float(self.entityAddress + offsets.oObjMagicPenPercent)) * 100

    @cached_property
    def armorPenPercent(self) -> float:
        return (1 - self.pm.read_float(self.entityAddress + offsets.oObjArmorPen)) * 100

    @cached_property
    def lethality(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjLethality)

    @cached_property
    def attackRange(self) -> float:
        return self.pm.read_float(self.entityAddress + offsets.oObjStatAttackRange)

    @cached_property
    def gamePos(self) -> dict:
        return pymeow.read_vec3(self.mem, self.entityAddress + offsets.oObjPosition)

    @cached_property
    def screenPos(self) -> dict:
        try:
            wts = pymeow.wts_ogl(self.overlay, self.viewProjMatrix.tolist(), self.gamePos)
        except:
            wts = pymeow.vec2()
        return wts

    @cached_property
    def isVisible(self) -> bool:
        return self.pm.read_bool(self.entityAddress + offsets.oObjVisible)

    @cached_property
    def onScreen(self):
        return self.screenPos['x'] > 0 and self.screenPos['x'] < self.overlay['width'] and self.screenPos['y'] > 0 and self.screenPos['y'] < self.overlay['height']

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
