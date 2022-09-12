from pymem import Pymem
from models import PlayerEntity
from resources import offsets, LeagueStorage
from resources.StructureReader import StructureReader


class LeagueReader:
    def __init__(self, pm: Pymem, mem, overlay, viewProjMatrix, lStorage):
        self.pm = pm
        self.mem = mem
        self.overlay = overlay
        self.viewProjMatrix = viewProjMatrix
        self.lStorage: LeagueStorage = lStorage

        self.localPlayer: PlayerEntity = self.get_local_player()
        self.teamPlayers, self.enemyPlayers = self.get_players()

    def get_local_player(self) -> PlayerEntity:
        return PlayerEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix, self.lStorage.localPlayerAddr)

    def get_players(self) -> tuple[list[PlayerEntity], list[PlayerEntity]]:
        allChampAddrs: list[int] = StructureReader.read_v_table(self.pm, self.lStorage.heroManagerAddr)

        teamPlayers, enemyPlayers = [], []
        i: int = 0
        while i < len(allChampAddrs):
            isVisible: bool = self.pm.read_bool(allChampAddrs[i] + offsets.oObjVisible)
            health: float = self.pm.read_float(allChampAddrs[i] + offsets.oObjHealth)

            if isVisible or health <= 0:
                player: PlayerEntity = PlayerEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix,
                                                    allChampAddrs[i])
                if player.teamId == self.localPlayer.teamId:
                    teamPlayers.append(player)
                else:
                    enemyPlayers.append(player)
            i += 1

        return teamPlayers, enemyPlayers
