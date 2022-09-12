from pymem import Pymem
from models import PlayerEntity
from models.Minion import MinionEntity
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
        
    @cached_property
    def minions(self) -> list:   
        all_minions_addr: list[int] = StructureReader.read_v_table(self.pm, self.lStorage.minion_manager_addr)        
        for minion_addr in all_minions_addr:            
            m = MinionEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix, minion_addr)
            if m.health > 0:
                yield m               
    @cached_property
    def get_local_player(self) -> PlayerEntity:
        return PlayerEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix, self.lStorage.localPlayerAddr)
    
    @cached_property
    def team_players(self) -> list[PlayerEntity]:
        for p in self.get_players():
            if p.teamId == self.localPlayer.teamId:
                yield p
    @cached_property
    def enemies_players(self) -> list[PlayerEntity]:
        for p in self.get_players():
            p.teamId != self.localPlayer.teamId
            yield p
    
    @cached_property
    def get_players(self) -> tuple[list[PlayerEntity], list[PlayerEntity]]:       
        
        allChampAddrs: list[int] = StructureReader.read_v_table(self.pm, self.lStorage.heroManagerAddr)

        for champ in allChampAddrs:
            yield champ