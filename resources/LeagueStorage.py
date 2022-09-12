from pymem import Pymem
from resources import offsets


class LeagueStorage:
    def __init__(self, pm: Pymem):
        self.pm = pm

        self.localPlayerAddr: int = self.pm.read_int(self.pm.base_address + offsets.oLocalPlayer)
        self.heroManagerAddr: int = self.pm.read_int(self.pm.base_address + offsets.oHeroManager)
        self.minion_manager_addr: int = self.pm.read_int(self.pm.base_address + offsets.oMinionList)
