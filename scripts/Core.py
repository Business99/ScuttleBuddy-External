# Define script specific settings
scriptSettings: dict = {
    'AttackRangeESP': True,
    'TestAiManager': True
}

import os
import keyboard
import mouse
import time
import math
class Core:
    def __init__(self, lReader, pymeow):
        self.lReader = lReader
        self.pymeow = pymeow

        if scriptSettings['AttackRangeESP']:
            self.attack_range()
        if scriptSettings['TestAiManager']:
            self.test_ai_manager()
        self.orbwalk()

    def attack_range(self):       
        if self.lReader.localPlayer.onScreen:
            player = self.lReader.localPlayer
            world_pos = player.gamePos
            radius: float = self.lReader.localPlayer.attackRange * 1.1
            theta: float = 0       
            
            word_space = []
            while theta < 2 * 3.14:
                x = world_pos['x'] + radius * math.cos(theta)
                y = world_pos['y']
                z = radius * math.sin(theta) + world_pos['z']
                word_space.append(self.pymeow.wts_ogl(self.lReader.overlay, self.lReader.viewProjMatrix.tolist(), {'x': x, 'y': y, 'z': z}))
                theta += 0.01

            i = 0
            while i < len(word_space) - 1:
                self.pymeow.line_v(
                    word_space[i],
                    word_space[i + 1],
                    3,
                    self.pymeow.rgb("red")
                )
                i += 1
            
            # self.pymeow.ellipse_v(
            #     pos,
            #     self.lReader.localPlayer.attackRange - ((43 * self.lReader.localPlayer.attackRange) / 100.0),#170 * 0.5,
            #     self.lReader.localPlayer.attackRange - ((55 * self.lReader.localPlayer.attackRange) / 100.0),
            #     #self.lReader.localPlayer,#150 * 0.3,
            #     self.pymeow.rgb("red")
            # )

    def test_ai_manager(self):
        for ePlayer in self.lReader.enemyPlayers:

            self.pymeow.ellipse_v(
                ePlayer.AiManager.endPathScreen,
                10,
                10,
                self.pymeow.rgb("red")
            )
