import threading
from pymem import Pymem
import utils
from resources import LeagueReader
import pymeow
from utils.settings import SETTINGS
from scripts import SummonerSpells
import scripts
import time

if __name__ == '__main__':
    pm: Pymem = Pymem('League of Legends.exe')
    mem = pymeow.process_by_name("League of Legends.exe")

    overlay = pymeow.overlay_init("League of Legends (TM) Client")
    summonerFont = pymeow.font_init(20, "ComicSans")
    view_proj_matrix = utils.find_view_proj_matrix(pm)
    # pymeow.set_foreground("League of Legends (TM) Client")

    ex_times: list = []
    while pymeow.overlay_loop(overlay):
        settings: dict = SETTINGS

        st = time.time()

        lReader: LeagueReader = LeagueReader(pm, mem, overlay, view_proj_matrix)

        # Based on global script settings, load the scripts
        if settings['SummonerSpellScript']:
            SummonerSpells.onTick(lReader, pymeow)
        if settings['VeigarScript']:
            scripts.Veigar(lReader, pymeow)

        et = time.time()

        execution_time = (et - st) * 1000
        ex_times.append(execution_time)

        print(f"Average Execution time: {sum(ex_times) / len(ex_times)} ms")
