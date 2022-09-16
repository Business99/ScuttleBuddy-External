from pymem import Pymem
from models import PlayerEntity
from models.Entity import Entity
from models.Minion import MinionEntity
from models.Turret import TurretEntity
from models.Ward import WardEntity
from models.Monster import MonsterEntity
from resources import offsets, LeagueStorage
from resources.StructureReader import StructureReader
from functools import cached_property


class LeagueReader:
    def __init__(self, pm: Pymem, mem, overlay, viewProjMatrix, lStorage):
        self.pm = pm
        self.mem = mem
        self.overlay = overlay
        self.viewProjMatrix = viewProjMatrix
        self.lStorage: LeagueStorage = lStorage

        self.__ward_names: list[str] = ["BlueTrinket", "JammerDevice", "YellowTrinket"]

    @cached_property
    def minions(self) -> list[MinionEntity]:
        for entity in self.get_non_players():
            if 'Minion' in entity.name and entity.health > 0:
                yield MinionEntity(entity.pm, entity.mem, entity.overlay, entity.viewProjMatrix, entity.entityAddress)

    @cached_property
    def wards(self) -> list[WardEntity]:
        for entity in self.get_non_players():
            if entity.name in self.__ward_names:
                yield WardEntity(entity.pm, entity.mem, entity.overlay, entity.viewProjMatrix, entity.entityAddress)

    @cached_property
    def monsters(self) -> list[MonsterEntity]:
        for entity in self.get_non_players():
            if entity.name not in self.__ward_names and 'Minion' not in entity.name:
                yield MonsterEntity(entity.pm, entity.mem, entity.overlay, entity.viewProjMatrix, entity.entityAddress)

    @cached_property
    def turrets(self) -> list[TurretEntity]:
        allTurretAddrs: list[int] = StructureReader.read_v_table(self.pm, self.lStorage.turretManagerAddr)
        for turretAddr in allTurretAddrs:
            yield TurretEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix, turretAddr)

    @cached_property
    def localPlayer(self) -> PlayerEntity:
        return PlayerEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix, self.lStorage.localPlayerAddr)

    @cached_property
    def teamPlayers(self) -> list[PlayerEntity]:
        for p in self.get_players():
            if p.teamId == self.localPlayer.teamId:
                yield p

    @cached_property
    def enemyPlayers(self) -> list[PlayerEntity]:
        for p in self.get_players():
            if p.teamId != self.localPlayer.teamId:
                yield p

    def get_players(self) -> list[PlayerEntity]:
        allChampAddrs: list[int] = StructureReader.read_v_table(self.pm, self.lStorage.heroManagerAddr)
        for champ in allChampAddrs:
            yield PlayerEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix, champ)

    def get_non_players(self) -> list[Entity]:
        allAddrs: list[int] = StructureReader.read_v_table(self.pm, self.lStorage.minion_manager_addr)
        for addr in allAddrs:
            e: Entity = Entity(self.pm, self.mem, self.overlay, self.viewProjMatrix, addr)
            if 'PreSeason' not in e.name:
                yield e
