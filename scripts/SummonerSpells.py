import pymeow
from resources import LeagueReader, constants

# Define script specific settings
scriptSettings: dict = {
    'SummonerSpellESP': True
}


class SummonerSpells:
    def __init__(self, lReader: LeagueReader):
        self.lReader = lReader
        self.font = pymeow.font_init(20, "ComicSans")

        # Run script functions based on script settings
        if scriptSettings['SummonerSpellESP']:
            self.enemy_summonor_spells()

    def enemy_summonor_spells(self):
        for ePlayer in self.lReader.enemyPlayers:
            if not ePlayer.isVisible:
                continue

            i = 0
            for sumSpell in ePlayer.spells:
                if sumSpell.isSummoner:

                    texture = pymeow.load_texture(
                        f"{constants.SUMMONER_SPELL_FP}{sumSpell.name}.png")

                    if i == 0:
                        pymeow.draw_texture(texture, ePlayer.screenPos['x'] - 60,
                                            ePlayer.screenPos['y'] - 50, 30, 30)
                        pymeow.font_print(self.font, ePlayer.screenPos['x'] - 60,
                                          ePlayer.screenPos['y'] - 70,
                                          str(int(sumSpell.readyIn)), pymeow.rgb('white'))
                        i += 1
                    else:
                        pymeow.draw_texture(texture, ePlayer.screenPos['x'] - 15,
                                            ePlayer.screenPos['y'] - 50, 30, 30)
                        pymeow.font_print(self.font, ePlayer.screenPos['x'] - 15,
                                          ePlayer.screenPos['y'] - 70,
                                          str(int(sumSpell.readyIn)), pymeow.rgb('white'))
                        i = 0