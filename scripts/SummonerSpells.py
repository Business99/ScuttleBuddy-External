# Importing LeagueReader for typing intellisense
from resources import LeagueReader

SUMMONER_SPELL_FP = 'D:\\Hacking\\ScuttlePy\\datadragon\\summonerSpells\\'
LAP_SUMMONER_FP = 'C:\\Github\\ScuttleBuddy-External\\datadragon\\summonerSpells\\'


# Setup function | only runs once on script load
def setup():
    pass


# OnTick function | Runs every tick
def on_tick(lReader: LeagueReader, pymeow):
    font = pymeow.font_init(20, "ComicSans")
    enemy_summonor_spells(lReader, pymeow, font)


def enemy_summonor_spells(lReader: LeagueReader, pymeow, font):
    for ePlayer in lReader.enemyPlayers:
        if ePlayer.health <= 0 or not ePlayer.onScreen:
            continue

        i = 0
        for sumSpell in ePlayer.spells:
            if sumSpell.isSummoner:

                texture = pymeow.load_texture(
                    f"{SUMMONER_SPELL_FP}{sumSpell.name}.png")

                if i == 0:
                    pymeow.draw_texture(texture, ePlayer.screenPos['x'] - 60,
                                        ePlayer.screenPos['y'] - 50, 30, 30)
                    pymeow.font_print(font, ePlayer.screenPos['x'] - 60,
                                      ePlayer.screenPos['y'] - 70,
                                      str(int(sumSpell.readyIn)), pymeow.rgb('white'))
                    i += 1
                else:
                    pymeow.draw_texture(texture, ePlayer.screenPos['x'] - 15,
                                        ePlayer.screenPos['y'] - 50, 30, 30)
                    pymeow.font_print(font, ePlayer.screenPos['x'] - 15,
                                      ePlayer.screenPos['y'] - 70,
                                      str(int(sumSpell.readyIn)), pymeow.rgb('white'))
                    i = 0


# Run the setup function
setup()
