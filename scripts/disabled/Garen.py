# Importing LeagueReader for typing intellisense
from resources import LeagueReader


# Setup function | only runs once on script load
def setup():
    pass


# OnTick function | Runs every tick
def on_tick(lReader: LeagueReader, pymeow):
    font = pymeow.font_init(20, "ComicSans")
    garen_r_execute_esp(lReader, pymeow, font)


def garen_r_execute_esp(lReader: LeagueReader, pymeow, font):
    # Check if the person is playing Garen
    if not lReader.localPlayer.name == 'Garen':
        return

    # Get Veigar's Ult
    ult_spell = lReader.localPlayer.spells[3]

    # Make sure the person has unlocked their ult
    if ult_spell.level == 0:
        return

    # Calculate total R damage
    baseDamage: int = [150, 300, 450][ult_spell.level - 1]
    missingHealthDamage: int = [.25, .35, .35][ult_spell.level - 1]

    # Loop through enemies and alert if one can be killed
    for enemy in lReader.enemyPlayers:
        if not enemy.isVisible or enemy.health <= 0:
            continue

        percentage_health: float = 100 / enemy.maxHealth * enemy.health
        percentMissingHp: float = 100 - percentage_health

        missingHp: float = enemy.maxHealth - enemy.health
        totalDamage: float = baseDamage + (missingHp * missingHealthDamage)

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
