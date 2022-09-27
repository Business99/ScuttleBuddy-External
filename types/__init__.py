from dataclasses import dataclass


# region League Reader
@dataclass
class LeagueReader:
    enemy_minions: list
    minions: list
    wards: list
    monsters: list
    turrets: list
    localPlayer: list
    teamPlayers: list
    enemyPlayers: list


# endregion

# region Other
@dataclass
class Spell:
    gameTime: float
    readyAt: float
    readyIn: float
    level: int
    name: str
    isSummoner: bool


@dataclass
class Buff:
    type: int


@dataclass
class AiManager:
    startPath: dict
    startPathScreen: dict
    endPath: dict
    endPathScreen: dict
    isDashing: bool
    isMoving: bool
    dashSpeed: int


# endregion

# region Entity Related
@dataclass
class Entity:
    name: str
    level: int
    teamId: int
    isTargetable: bool
    health: float
    is_alive: float
    maxHealth: float
    mana: float
    maxMana: float
    ap: float
    ad: float
    bonusAttackSpeedPercent: float
    magicResist: float
    armor: float
    magicPenFlat: float
    magicPenPercent: float
    armorPenPercent: float
    lethality: float
    attackRange: float
    gamePos: dict
    screenPos: dict
    isVisible: bool
    onScreen: bool
    AiManager: AiManager
    buffs: list[Buff]


@dataclass
class PlayerEntity(Entity):
    def __init__(self):
        super().__init__()

    spells: list[Spell]


@dataclass
class MinionEntity(Entity):
    def __init__(self):
        super().__init__()


@dataclass
class MonsterEntity(Entity):
    def __init__(self):
        super().__init__()


@dataclass
class TurretEntity(Entity):
    def __init__(self):
        super().__init__()

    turretAttackRange: float


@dataclass
class WardEntity(Entity):
    def __init__(self):
        super().__init__()

# endregion
