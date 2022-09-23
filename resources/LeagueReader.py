import gevent.monkey
gevent.monkey.patch_all()

import requests
import grequests
from pymem import Pymem
from models import PlayerEntity
from models.Entity import Entity
from models.Minion import MinionEntity
from models.Turret import TurretEntity
from models.Ward import WardEntity
from models.Monster import MonsterEntity
from resources import Offsets, LeagueStorage
from resources.StructureReader import StructureReader
from functools import cached_property, cache


GAME_DATA_ENDPOINT = 'https://127.0.0.1:2999/liveclientdata/allgamedata'
CHAMPION_INFO_ENDPOINT = 'https://raw.communitydragon.org/latest/game/data/characters/{champion}/{champion}.bin.json'
DATA_ROOT_KEY = 'Characters/{champion}/CharacterRecords/Root'
DEFAULT_RADIUS = 65.
DEFAULT_WINDUP = 0.3
class LeagueReader:
    
    champs_data = None
    __ward_names: list[str] = ["BlueTrinket", "JammerDevice", "YellowTrinket"]
    __ignored__entities: list[str] = [
        'PreSeason_Turret_Shield',
        'SRU_Plant_Vision',
        'SRU_Plant_Satchel'
    ]
    
    @property
    def enemy_minions(self) -> list[MinionEntity]:        
        lp_team_id = self.localPlayer.teamId
        for minion in self.get_non_players():
            if minion.teamId != lp_team_id and minion.is_alive:
                yield MinionEntity(self.pm, self.mem, self.overlay, self.view_proj_matrix, minion.entityAddress)

    
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


    @property
    def localPlayer(self) -> PlayerEntity:
        return PlayerEntity(self.pm, self.mem, self.overlay, self.view_proj_matrix, self.lStorage.localPlayerAddr)


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
            yield PlayerEntity(self.pm, self.mem, self.overlay, self.view_proj_matrix, champ)


    def get_non_players(self) -> list[Entity]:
        allAddrs: list[int] = StructureReader.read_v_table(self.pm, self.lStorage.minion_manager_addr)
        for addr in allAddrs:
            e: Entity = Entity(self.pm, self.mem, self.overlay, self.view_proj_matrix, addr)
            if e.name not in self.__ignored__entities:
                yield e

    
    def wrapper_root_key(func):
        def wrapper(self, champion: PlayerEntity):
            if not self.champs_data:
                self.get_game_data()
            return func(self, champion=champion, data=self.champs_data[champion.name.lower()][DATA_ROOT_KEY.format(champion=champion.name)])
        return wrapper
    
    def get_game_data(self) -> dict:
            if self.champs_data:
                return self.champs_data 
            champions_name = [champion['championName'].lower() for champion in requests.get(GAME_DATA_ENDPOINT, verify=False).json()['allPlayers']]
            
            while 'boneco-alvo' in champions_name:
                champions_name.remove('boneco-alvo')
                    
            responses = [ r.json() for r in grequests.map((grequests.get(CHAMPION_INFO_ENDPOINT.format(champion=name)) for name in champions_name), size=10)]
            self.champs_data = { name: response for name in champions_name for response in responses for key in response.keys() if name in key.lower()}
            return self.champs_data
    
    @cache
    @wrapper_root_key
    def get_windup(self, champion:PlayerEntity, data) -> float:
        basic_attack = data['basicAttack']    
        windup_percent = 0.3
        windup_modifier = 0.        
        if 'mAttackDelayCastOffsetPercent' in basic_attack:
            windup_percent = basic_attack['mAttackDelayCastOffsetPercent'] + DEFAULT_WINDUP
        if 'mAttackDelayCastOffsetPercentAttackSpeedRatio' in basic_attack:
            windup_modifier = basic_attack['mAttackDelayCastOffsetPercentAttackSpeedRatio']
        return windup_percent, windup_modifier
    
    @cache
    @wrapper_root_key
    def get_base_attack_speed(self, champion: PlayerEntity, data) -> float:
        return data['attackSpeed'], data['attackSpeedRatio']
    
    @cache
    @wrapper_root_key
    def get_attack_speed(self, champion: PlayerEntity, data) -> float:
        return data['attackSpeed'] * champion.attack_speed_bonus #, data['attackSpeedRatio']