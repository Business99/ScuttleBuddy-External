# Define script specific settings
scriptSettings: dict = {
    'SummonerSpellESP': True
}

SUMMONER_SPELL_FP = 'D:\\Hacking\\ScuttlePy\\datadragon\\summonerSpells\\'
LAP_SUMMONER_FP = 'C:\\Github\\ScuttleBuddy-External\\datadragon\\summonerSpells\\'


class SummonerSpells:
    def __init__(self, lReader, pymeow):
        self.lReader = lReader
        self.pymeow = pymeow
        self.font = self.pymeow.font_init(20, "ComicSans")

        # Run script functions based on script settings
        if scriptSettings['SummonerSpellESP']:
            self.enemy_summonor_spells()

    def enemy_summonor_spells(self):
        for ePlayer in self.lReader.enemyPlayers:
            if ePlayer.health <= 0:
                continue

            i = 0
            for sumSpell in ePlayer.spells:
                if sumSpell.isSummoner:

                    texture = self.pymeow.load_texture(
                        f"{SUMMONER_SPELL_FP}{sumSpell.name}.png")

                    if i == 0:
                        self.pymeow.draw_texture(texture, ePlayer.screenPos['x'] - 60,
                                                 ePlayer.screenPos['y'] - 50, 30, 30)
                        self.pymeow.font_print(self.font, ePlayer.screenPos['x'] - 60,
                                               ePlayer.screenPos['y'] - 70,
                                               str(int(sumSpell.readyIn)), self.pymeow.rgb('white'))
                        i += 1
                    else:
                        self.pymeow.draw_texture(texture, ePlayer.screenPos['x'] - 15,
                                                 ePlayer.screenPos['y'] - 50, 30, 30)
                        self.pymeow.font_print(self.font, ePlayer.screenPos['x'] - 15,
                                               ePlayer.screenPos['y'] - 70,
                                               str(int(sumSpell.readyIn)), self.pymeow.rgb('white'))
                        i = 0
