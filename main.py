from pymem import Pymem
import utils
from resources import LeagueReader
import pymeow
from utils.settings import SETTINGS
import scripts


if __name__ == '__main__':
    pm: Pymem = Pymem('League of Legends.exe')
    mem = pymeow.process_by_name("League of Legends.exe")

    overlay = pymeow.overlay_init("League of Legends (TM) Client")

    #pymeow.set_foreground("League of Legends (TM) Client")

    while pymeow.overlay_loop(overlay):
        settings: dict = SETTINGS

        view_proj_matrix = utils.find_view_proj_matrix(pm)
        lReader: LeagueReader = LeagueReader(pm, mem, overlay, view_proj_matrix)

        # Based on global script settings, load the scripts
        if settings['SummonerSpellScript']:
            scripts.SummonerSpells(lReader)
        if settings['VeigarScript']:
            scripts.Veigar(lReader)
