from functools import cached_property
from models import Entity
from pymem import Pymem


class TurretEntity(Entity):
    def __init__(self, pm: Pymem, mem, overlay, viewProjMatrix, entityAddress: int):
        super().__init__(pm, mem, overlay, viewProjMatrix, entityAddress)

    @cached_property
    def turretAttackRange(self) -> float:
        return 800.0
