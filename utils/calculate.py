from models import PlayerEntity


def calculate_magic_damage(source: PlayerEntity, target: PlayerEntity, damage: float) -> float:
    targetMagicResist: float = target.magicResist
    sourceMagicPenFlat: float = source.magicPenFlat
    sourceMagicPenPerc: float = source.magicPenPercent

    unknown = targetMagicResist - sourceMagicPenFlat

    unknown = unknown / 100 * (100 - sourceMagicPenPerc)

    if unknown < 0:
        return damage * (2 - (100 / (100 - unknown)))

    return damage * (100 / (100 + unknown))


def calculate_physical_damage(source: PlayerEntity, target: PlayerEntity, damage: float) -> float:
    targetArmor: float = target.armor
    sourceLethality: float = source.lethality
    sourceArmorPenPerc: float = source.armorPenPercent

    flatArmorPen = sourceLethality * (0.6 + (0.4 * source.level / 18))

    unknown = targetArmor - flatArmorPen
    unknown = unknown / 100 * (100 - sourceArmorPenPerc)

    if unknown < 0:
        return damage * (2 - (100 / (100 - unknown)))

    return damage * (100 / (100 + unknown))
