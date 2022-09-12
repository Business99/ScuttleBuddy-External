# Define script specific settings
scriptSettings: dict = {
    'AttackRangeESP': True
}


class Core:
    def __init__(self, lReader, pymeow):
        self.lReader = lReader
        self.pymeow = pymeow

        if scriptSettings['AttackRangeESP']:
            self.attack_range()

    def attack_range(self):
        if self.lReader.localPlayer.on_screen:
            self.pymeow.ellipse_v(
                self.lReader.localPlayer.screenPos,
                self.lReader.localPlayer.attackRange,
                self.lReader.localPlayer.attackRange,
                self.pymeow.rgb("red")
            )
