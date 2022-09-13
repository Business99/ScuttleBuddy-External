# Importing LeagueReader for typing intellisense
from resources import LeagueReader
from utils import calculate


# Setup function | only runs once on script load
def setup():
    pass


# OnTick function | Runs every tick
def on_tick(lReader: LeagueReader, pymeow):
    font = pymeow.font_init(20, "ComicSans")


def veigar_r_execute_esp(lReader: LeagueReader, pymeow, font):
    # Check if the person is playing Veigar
    if not lReader.localPlayer.championName == 'Veigar':
        return

    # Get Veigar's Ult
    ult_spell = None
    for spell in lReader.localPlayer.spells:
        if spell.name == 'VeigarR':
            ult_spell = spell
            break

    # Make sure the person has unlocked their ult
    if ult_spell.level == 0:
        return

    # Calculate total R damage
    baseDamage: int = [175, 250, 325][ult_spell.level - 1]
    scalingDamage: float = 0.75 * lReader.localPlayer.ap

    # Loop through enemies and alert if one can be killed
    for enemy in lReader.enemyPlayers:
        if not enemy.isVisible or enemy.health <= 0:
            continue

        percentage_health: float = 100 / enemy.maxHealth * enemy.health
        percentMissingHp: float = 100 - percentage_health

        bonusDamagePercent: float = max(percentMissingHp * 1.5, 100)

        beforeResistDmg: float = (baseDamage + scalingDamage) + (
                (baseDamage + scalingDamage) / 100 * bonusDamagePercent)

        totalDamage: float = calculate.calculate_magic_damage(lReader.localPlayer, enemy, beforeResistDmg)

        if enemy.health <= totalDamage and ult_spell.readyIn == 0:
            pymeow.circle(
                enemy.screenPos['x'],
                enemy.screenPos['y'],
                30,
                pymeow.rgb('red'),
                True,
                1
            )
            pymeow.font_print(font, enemy.screenPos['x'] - 10,
                              enemy.screenPos['y'],
                              "R", pymeow.rgb('white'))


# Run the setup function
setup()
