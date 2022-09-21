from pymem import Pymem
import utils
from resources import LeagueReader, LeagueStorage
import pymeow
import time
import importlib
import os
import json
from ui import SettingsWindow
import threading

loaded_scripts: list = []


def load_user_scripts() -> None:
    with open(os.path.abspath("settings.json"), "r") as f:
        data = json.load(f)

    data["scripts"] = {}

    for filename in os.listdir('scripts/enabled'):
        if filename == '__pycache__':
            continue

        module = importlib.import_module(f'scripts.enabled.{filename[:-3]}')
        loaded_scripts.append(module)
        print(f"Loaded: {filename}")

        moduleSettings: dict = module.setup()
        data['scripts'][filename] = moduleSettings

    with open(os.path.abspath("settings.json"), "w") as j:
        json.dump(data, j, indent=4)


if __name__ == '__main__':
    # t2 = threading.Thread(target=SettingsWindow.tkinter_window)
    # t2.start()
    load_user_scripts()
    pm: Pymem = Pymem('League of Legends.exe')
    mem = pymeow.process_by_name("League of Legends.exe")

    overlay = pymeow.overlay_init("League of Legends (TM) Client")
    summonerFont = pymeow.font_init(20, "ComicSans")

    lStorage: LeagueStorage = LeagueStorage(pm)

    # pymeow.set_foreground("League of Legends (TM) Client")

    while pymeow.overlay_loop(overlay): 
        
        targets = None            
        debug = {}
        debug['Selected Mode:'] = ""
        debug['Execution time:'] = ""
               

        st = time.time()

        view_proj_matrix = utils.find_view_proj_matrix(pm)
        lReader: LeagueReader = LeagueReader(pm, mem, overlay, view_proj_matrix, lStorage)
        lReader.get_attack_speed(lReader.localPlayer)
        with open(os.path.abspath("settings.json"), "r") as f:
            settings = json.load(f)

        for user_script in loaded_scripts:
            script_key = list(settings["scripts"].keys())[loaded_scripts.index(user_script)]
            user_script.on_tick(lReader, pymeow, settings["scripts"][script_key])

        et = time.time()

        execution_time = (et - st) * 1000

        # print(f"Average Execution time: {execution_time} ms")
