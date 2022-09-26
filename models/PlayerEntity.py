from functools import cached_property
from models import Entity, Spell
from pymem import Pymem
from resources import Offsets
import pymeow

class PlayerEntity(Entity):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)

    def basic_attack_damage(self, target) -> float:
        return self.ad * (1 - self.armorPenPercent / 100) - target.armor

    def can_attack(self, target) -> bool:
        return self.is_alive and target.is_alive and target.isVisible

    def in_aa_range(self, target) -> bool:
        return (self.attackRange * 1.2) > self.distance_to(target)
    
    def get_fastest_to_aa_kill(self, targets: list):
        can_attack = [target for target in targets if self.in_aa_range(target) and self.can_attack(target)]
        if not can_attack:
            return None
        return min(can_attack, key=lambda x: self.basic_attack_needed(x))

    def get_lasthit_aa_target(self, targets: list):
        target = None
        can_attack = [target for target in targets if self.in_aa_range(target) and self.can_attack(target)]
        for target in can_attack:
            if self.basic_attack_needed(target) <= 1.1:                
                return target
        return None
    
    @cached_property
    def attack_speed_multiplier(self) -> float:
        return 1 + self.pm.read_float(self._addr + Offsets.ObjAtkSpeedMultiplier)
    
    @cached_property
    def attack_speed_bonus(self) -> float:
        return self.pm.read_float(self.entityAddress + Offsets.ObjAtkSpeedBonus)
    
    def basic_attack_needed(self, target) -> float:
        return target.health / self.basic_attack_damage(target)
    
    
    
    
    @cached_property
    def spells(self) -> list[Spell]:
        spells: list = []

        # Handle spells
        spellAddresses: list[int] = []
        j: int = 0
        while j <= 5:
            spellAddresses.append(self.entityAddress + (j * 4))
            j += 1

        i: int = 0
        while i < len(spellAddresses):
            spells.append(Spell(self.pm, spellAddresses[i]))
            i += 1
        return spells

