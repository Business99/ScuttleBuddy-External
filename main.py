from pymem import Pymem
import utils
from resources import LeagueReader, LeagueStorage
import pymeow
import time
import importlib
import os
import json
import tkinter as tk
import threading

loaded_scripts: list = []


def load_user_scripts() -> None:
    with open("settings.json", "r") as f:
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

    with open("settings.json", "w") as j:
        json.dump(data, j, indent=4)


def tkinter_window():
    window = tk.Tk()
    window.geometry('300x200')
    window.title('ScuttleBuddy')
    test_icon = tk.PhotoImage(file='./datadragon/summonerSpells/SummonerSmite.png')
    testButton = tk.Button(
        window,
        image=test_icon,
        text='Test',
        compound=tk.LEFT,
        command=lambda: window.quit()
    )
    testButton.pack(
        ipadx=5,
        ipady=5,
        expand=True
    )
    window.mainloop()


if __name__ == '__main__':
    # t2 = threading.Thread(target=tkinter_window)
    # t2.start()
    load_user_scripts()
    pm: Pymem = Pymem('League of Legends.exe')
    mem = pymeow.process_by_name("League of Legends.exe")

    overlay = pymeow.overlay_init("League of Legends (TM) Client")
    summonerFont = pymeow.font_init(20, "ComicSans")

    lStorage: LeagueStorage = LeagueStorage(pm)

    # pymeow.set_foreground("League of Legends (TM) Client")

    while pymeow.overlay_loop(overlay):
        st = time.time()

        view_proj_matrix = utils.find_view_proj_matrix(pm)
        lReader: LeagueReader = LeagueReader(pm, mem, overlay, view_proj_matrix, lStorage)

        with open("settings.json", "r") as f:
            settings = json.load(f)

        for user_script in loaded_scripts:
            script_key = list(settings["scripts"].keys())[loaded_scripts.index(user_script)]
            user_script.on_tick(lReader, pymeow, settings["scripts"][script_key])

        et = time.time()

        execution_time = (et - st) * 1000

        print(f"Average Execution time: {execution_time} ms")
