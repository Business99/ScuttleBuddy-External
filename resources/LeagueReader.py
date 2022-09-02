from pymem import Pymem
from models import PlayerEntity
from resources import offsets
from resources.StructureReader import StructureReader


class LeagueReader:
    def __init__(self, pm: Pymem, mem, overlay, viewProjMatrix):
        self.pm = pm
        self.mem = mem
        self.overlay = overlay
        self.viewProjMatrix = viewProjMatrix

        self.localPlayer: PlayerEntity = self.get_local_player()
        self.teamPlayers, self.enemyPlayers = self.get_players()

    def get_local_player(self) -> PlayerEntity:
        lpAddr: int = self.pm.read_int(self.pm.base_address + offsets.oLocalPlayer)
        return PlayerEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix, lpAddr)

    def get_players(self) -> tuple[list[PlayerEntity], list[PlayerEntity]]:
        heroManagerAddr: int = self.pm.read_int(self.pm.base_address + offsets.oHeroManager)
        allChampAddrs: list[int] = StructureReader.read_v_table(self.pm, heroManagerAddr)

        teamPlayers, enemyPlayers = [], []
        i: int = 0
        while i < len(allChampAddrs):
            isVisible: bool = self.pm.read_bool(allChampAddrs[i] + offsets.oObjVisible)
            if isVisible:
                player: PlayerEntity = PlayerEntity(self.pm, self.mem, self.overlay, self.viewProjMatrix,
                                                    allChampAddrs[i])
                if player.teamId == self.localPlayer.teamId:
                    teamPlayers.append(player)
                else:
                    enemyPlayers.append(player)
            i += 1

        return teamPlayers, enemyPlayers
