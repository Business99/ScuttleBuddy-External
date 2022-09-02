import pymeow
from pymem import Pymem
from models.Spell import Spell
from resources import offsets


class PlayerEntity:
    def __init__(self, pm: Pymem, mem, overlay, viewProjMatrix, entityAddress: int):
        self.pm = pm
        self.mem = mem
        self.overlay = overlay
        self.viewProjMatrix = viewProjMatrix
        self.entityAddress = entityAddress

        self.championName: str = None
        self.teamId: int = 0

        self.health: float = 0
        self.maxHealth: float = 0
        self.mana: float = 0
        self.maxMana: float = 0

        # Resistances
        self.magicResist: float = 0
        self.armor: float = 0

        self.ap: float = 0
        self.ad: float = 0

        # Penetrations
        self.magicPenFlat: float = 0
        self.magicPenPercent: float = 0
        self.armorPenPercent: float = 0
        self.lethality: float = 0

        self.gamePos = pymeow.vec3()
        self.screenPos = pymeow.vec2()

        self.spells: list = []

        self.isVisible = True
        self.level = 0

        self.update()

    def update(self):
        nameAddr: int = self.pm.read_int(self.entityAddress + offsets.oObjName)

        self.championName = self.pm.read_string(nameAddr)
        self.level = self.pm.read_int(self.entityAddress + offsets.oObjLevel)
        self.teamId = self.pm.read_int(self.entityAddress + offsets.oObjTeamId)
        self.health = self.pm.read_float(self.entityAddress + offsets.oObjHealth)
        self.maxHealth = self.pm.read_float(self.entityAddress + offsets.oObjMaxHealth)
        self.mana = self.pm.read_float(self.entityAddress + offsets.oObjMana)
        self.maxMana = self.pm.read_float(self.entityAddress + offsets.oObjMaxMana)

        self.ap = self.pm.read_float(self.entityAddress + offsets.oObjStatAp)
        self.ad = self.pm.read_float(
            self.entityAddress + offsets.oObjStatBaseAd
        ) + self.pm.read_float(self.entityAddress + offsets.oObjStatBonusAd)

        self.magicResist = self.pm.read_float(self.entityAddress + offsets.oObjMagicRes)
        self.armor = self.pm.read_float(self.entityAddress + offsets.oObjArmor)

        self.magicPenFlat = self.pm.read_float(self.entityAddress + offsets.oObjMagicPenFlat)
        self.magicPenPercent = (1 - self.pm.read_float(self.entityAddress + offsets.oObjMagicPenPercent)) * 100
        self.armorPenPercent = (1 - self.pm.read_float(self.entityAddress + offsets.oObjArmorPen)) * 100
        self.lethality = self.pm.read_float(self.entityAddress + offsets.oObjLethality)

        # Positions
        self.gamePos = pymeow.read_vec3(self.mem, self.entityAddress + offsets.oObjPosition)

        # WTS
        try:
            self.screenPos = pymeow.wts_ogl(self.overlay, self.viewProjMatrix.tolist(), self.gamePos)
        except:
            self.isVisible = False

        # Handle spells
        spellAddresses: list[int] = []
        for i in range(0, 6, 1):
            spellAddresses.append(self.entityAddress + (i * 4))

        for spellAddr in spellAddresses:
            self.spells.append(Spell(self.pm, spellAddr))