# Define script specific settings
scriptSettings: dict = {
    'AttackRangeESP': False,
    'TestAiManager': True
}


class Core:
    def __init__(self, lReader, pymeow):
        self.lReader = lReader
        self.pymeow = pymeow

        if scriptSettings['AttackRangeESP']:
            self.attack_range()
        if scriptSettings['TestAiManager']:
            self.test_ai_manager()

    def attack_range(self):
        if self.lReader.localPlayer.on_screen:
            self.pymeow.ellipse_v(
                self.lReader.localPlayer.screenPos,
                self.lReader.localPlayer.attackRange,
                self.lReader.localPlayer.attackRange,
                self.pymeow.rgb("red")
            )

    def test_ai_manager(self):
        for ePlayer in self.lReader.enemyPlayers:

            self.pymeow.ellipse_v(
                ePlayer.AiManager.endPathScreen,
                10,
                10,
                self.pymeow.rgb("red")
            )
