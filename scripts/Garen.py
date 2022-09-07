from utils import calculate

# Define script specific settings
scriptSettings: dict = {
    'RExecuteESP': True
}


class Garen:
    def __init__(self, lReader, pymeow):
        self.lReader = lReader
        self.pymeow = pymeow
        self.font = self.pymeow.font_init(20, "ComicSans")

        # Run script functions based on script settings
        if scriptSettings['RExecuteESP']:
            self.garen_r_execute_esp()

    def garen_r_execute_esp(self):
        # Check if the person is playing Veigar
        if not self.lReader.localPlayer.championName == 'Garen':
            return

        # Get Veigar's Ult
        ult_spell = self.lReader.localPlayer.spells[3]

        # Make sure the person has unlocked their ult
        if ult_spell.level == 0:
            return

        # Calculate total R damage
        baseDamage: int = [150, 300, 450][ult_spell.level - 1]
        missingHealthDamage: int = [.25, .35, .35][ult_spell.level - 1]

        # Loop through enemies and alert if one can be killed
        for enemy in self.lReader.enemyPlayers:
            if not enemy.isVisible or enemy.health <= 0:
                continue

            percentage_health: float = 100 / enemy.maxHealth * enemy.health
            percentMissingHp: float = 100 - percentage_health

            missingHp: float = enemy.maxHealth - enemy.health
            totalDamage: float = baseDamage + (missingHp * missingHealthDamage)

            if enemy.health <= totalDamage and ult_spell.readyIn == 0:
                self.pymeow.circle(
                    enemy.screenPos['x'],
                    enemy.screenPos['y'],
                    30,
                    self.pymeow.rgb('red'),
                    True,
                    1
                )
                self.pymeow.font_print(self.font, enemy.screenPos['x'] - 10,
                                       enemy.screenPos['y'],
                                       "R", self.pymeow.rgb('white'))
