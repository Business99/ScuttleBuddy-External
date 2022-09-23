from pymem import Pymem
from resources import Offsets


class LeagueStorage:
    def __init__(self, pm: Pymem):
        self.pm = pm

        self.localPlayerAddr: int = self.pm.read_int(self.pm.base_address + Offsets.oLocalPlayer)
        self.heroManagerAddr: int = self.pm.read_int(self.pm.base_address + Offsets.oHeroManager)
        self.minion_manager_addr: int = self.pm.read_int(self.pm.base_address + Offsets.oMinionList)
        self.turretManagerAddr: int = self.pm.read_int(self.pm.base_address + Offsets.oTurretList)
