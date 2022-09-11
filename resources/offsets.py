# Game
oGameTime: int = 0x313AFF0 #0x3111E68
oViewProjMatrix: int = 0x316F328 #0x3148A20
oRenderer: int = 0x3174DF4 #0x314B90C
oGameWindowWidth: int = 0x8
oGameWindowHeight: int = 0xc

# Entities / Managers
oLocalPlayer: int = 0x3141554 #0x3118DDC
oHeroManager: int = 0x18A50D0 #0x187BF54

# Player Entity
oObjTeamId: int = 0x0034 #0x0034
oObjPlayerName: int = 0x54 + 30
oObjName: int = 0x2D3C #0x2BD4
oObjLevel: int = 0x351C #0x33B4
oObjPosition: int = 0x01DC #0x01DC  # Vector 3
oObjVisible: int = 0x0274 #0x0274
oObjHealth: int = 0x0E74 #0x0E74
oObjMaxHealth: int = 0x0E84 #0x0E84
oObjMana: int = 0x029C #0x029C
oObjMaxMana: int = 0x02AC #0x02AC


# Player Stats
statBase: int = 0x1270
oObjStatAp: int = 0x1750
oObjStatBonusAd: int = 0x12CC
oObjStatBaseAd: int = 0x1358
oObjArmor: int = 0x137C
oObjMagicRes: int = 0x1384
oObjMagicPenFlat: int = statBase + 0x0
oObjArmorPen: int = statBase + 0x4
oObjMagicPenPercent: int = statBase + 0x8
oObjLethality: int = statBase + 0x1C
statBase2: int = statBase + 0x124
oObjStatAttackRange: int = statBase2 + 0x8

# Spells
oSpellBook: int = 0x2330
oSpellSlots: int = 0x2950 #0x27E8
oSpellReadyAt: int = 0x24
oSpellLevel: int = 0x1C
oSpellDamage: int = 0x94
oSpellManaCost: int = 0x52C
oSpellInfo: int = 0x120
oSpellName: int = 0x18
oSpellDamage: int = 0x94

oSpellInfoName: int = 0x104

oSpellInfoData: int = 0x40
oSpellInfoDataName: int = 0x6C
