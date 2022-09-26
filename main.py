from pymem import Pymem
import utils
from resources import LeagueReader, LeagueStorage, Offsets, Orbwalker
import pymeow
import time
import importlib
import os
import json
from ui import SettingsWindow
import threading
from functools import cache
from pymem import exception as pymem_exception
import keyboard, math

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


class Client(LeagueReader):
    
    WINDOW_NAME = "League of Legends (TM) Client"
    PROCESS_NAME = "League of Legends.exe"
    
    def __init__(self) -> None:
        self.overlay = pymeow.overlay_init(Client.WINDOW_NAME)
        self.overlay_font = pymeow.font_init(20, "ComicSans")
        self.mem = self._mem()
        self.pm = self._pm
        self.lStorage: LeagueStorage = LeagueStorage(self.pm)
        self.view_proj_matrix = None
        
        
    @classmethod    
    @property
    @cache
    def _pm(self) -> Pymem:
        while True:
            try:                
                return Pymem("League of Legends.exe")
            except pymem_exception.ProcessNotFound:
                print('Client - Waiting game to start...')
                time.sleep(1) 
    
    def _mem(self):
        while True: 
            try:
                return pymeow.process_by_name(Client.PROCESS_NAME)
            except Exception as e:
                print(f'Client - Process not found, waiting...')
                time.sleep(1)

    def run(self):
        orbwalker = Orbwalker(self)
        
        while pymeow.overlay_loop(self.overlay):
            targets = None            
            debug = {}
            debug['Selected Mode:'] = ""
            debug['Execution time:'] = ""
            
            exec_start = time.time()
            self.view_proj_matrix = utils.find_view_proj_matrix(self.pm)            
            
            ############## ORBWALKER TEST ##############
            
            t = None
            mode_selected = None
            player = self.localPlayer            
            if keyboard.is_pressed('v'):
                mode_selected = "Farm"            
                targets = self.enemy_minions
                t = player.get_fastest_to_aa_kill(targets) 
            if keyboard.is_pressed('x'):
                mode_selected = "Last Hit"
                targets = self.enemy_minions
                t = player.get_lasthit_aa_target(targets)                                                
            if keyboard.is_pressed(' '):   
                mode_selected = "Attack Player"                
                t = player.get_fastest_to_aa_kill(self.enemyPlayers)                        
            debug['Selected Mode:'] = mode_selected
            if mode_selected:
                orbwalker.walk(target=t, pymeow=pymeow, overlay=self.overlay)
            
            ############################################
            
            debug['Execution time:'] = f"{(time.time() - exec_start)*1000:.2f}ms"
            
            # Draw
            draw_start = time.time()
            self.draw_circle_at(pymeow, player.gamePos, player.attackRange * 1.2, pymeow.rgb("red"), self.overlay),
            
            debug['Draw time:'] = f"{(time.time() - draw_start)*1000:.2f}ms"
            debug['Game time:'] = f"{self.game_time:.2f}s"
            debug['Attack Speed:'] = self.get_attack_speed(player)
            self.debug_draw(pymeow=pymeow, infos=debug, pos=player.screenPos)     

    def debug_draw(self, pymeow, pos,  infos: dict):
        qtd = 1
        for k, info in infos.items():
            pymeow.font_print(
                self.overlay_font, 
                    pos['x'],
                pos['y'] - 17 * qtd,
                f"{k}: {info}",
                pymeow.rgb('white')
                )
            qtd += 1

    def draw_circle_at(self, pymeow, pos, radius, color, overlay):
        theta: float = 0        
        word_space = []
        while theta < 2 * 3.14:
            x = pos['x'] + radius * math.cos(theta)
            y = pos['y']
            z = radius * math.sin(theta) + pos['z']
            try:
                word_space.append(pymeow.wts_ogl(overlay, self.view_proj_matrix.tolist(),
                                                {'x': x, 'y': y, 'z': z}))
            except:
                pass
            theta += 0.01

        i = 0
        while i < len(word_space) - 1:
            pymeow.line_v(
                word_space[i],
                word_space[i + 1],
                1,
                color
            )
            i += 1
    

    @property
    def game_time(self):
        return self.pm.read_float(self.mem['baseaddr'] + Offsets.oGameTime)

if __name__ == '__main__':
    
    Client().run()