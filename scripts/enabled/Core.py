# Importing LeagueReader for typing intellisense
from resources import LeagueReader
import math
import os


# Setup function | only runs once on script load
def setup() -> dict:
    scriptSettings: dict = {
        "playerAttackRange": {
            "displayName": "Player Attack Range",
            "isEnabled": True
        },
        "enemyAttackRange": {
            "displayName": "Enemy Attack Ranges",
            "isEnabled": True
        },
        "summonerSpellESP": {
            "displayName": "Summoner Spell ESP",
            "isEnabled": True
        }
    }
    return scriptSettings


# OnTick function | Runs every tick
def on_tick(lReader: LeagueReader, pymeow, scriptSettings) -> None:
    font = pymeow.font_init(20, "ComicSans")

    enemies: list = []
    for enemy in lReader.enemyPlayers:
        enemies.append(enemy)

    if scriptSettings['playerAttackRange']['isEnabled']:
        attack_range(lReader, pymeow)
    if scriptSettings['enemyAttackRange']['isEnabled']:
        enemy_attack_range(lReader, pymeow, enemies)
    if scriptSettings['summonerSpellESP']['isEnabled']:
        summoner_spells(lReader, pymeow, font, enemies)


def summoner_spells(lReader: LeagueReader, pymeow, font, enemies):
    for enemy in enemies:
        if enemy.health <= 0 or not enemy.onScreen:
            continue

        i = 0
        for sumSpell in enemy.spells:
            if sumSpell.isSummoner:
                texture = pymeow.load_texture(
                    f"{os.path.abspath('datadragon/summonerSpells')}\\{sumSpell.name}.png")

                if i == 0:
                    pymeow.draw_texture(texture, enemy.screenPos['x'] - 60,
                                        enemy.screenPos['y'] - 50, 30, 30)
                    pymeow.font_print(font, enemy.screenPos['x'] - 60,
                                      enemy.screenPos['y'] - 70,
                                      str(int(sumSpell.readyIn)), pymeow.rgb('white'))
                    i += 1
                else:
                    pymeow.draw_texture(texture, enemy.screenPos['x'] - 15,
                                        enemy.screenPos['y'] - 50, 30, 30)
                    pymeow.font_print(font, enemy.screenPos['x'] - 15,
                                      enemy.screenPos['y'] - 70,
                                      str(int(sumSpell.readyIn)), pymeow.rgb('white'))
                    i = 0


def attack_range(lReader: LeagueReader, pymeow):
    if lReader.localPlayer.onScreen and lReader.localPlayer.health > 0:
        player = lReader.localPlayer
        world_pos = player.gamePos
        radius: float = lReader.localPlayer.attackRange * 1.1
        theta: float = 0

        word_space = []
        while theta < 2 * 3.14:
            x = world_pos['x'] + radius * math.cos(theta)
            y = world_pos['y']
            z = radius * math.sin(theta) + world_pos['z']
            word_space.append(pymeow.wts_ogl(lReader.overlay, lReader.viewProjMatrix.tolist(),
                                             {'x': x, 'y': y, 'z': z}))
            theta += 0.01

        i = 0
        while i < len(word_space) - 1:
            pymeow.line_v(
                word_space[i],
                word_space[i + 1],
                3,
                pymeow.rgb("blue")
            )
            i += 1


def enemy_attack_range(lReader: LeagueReader, pymeow, enemies):
    for enemy in enemies:
        if not enemy.onScreen or enemy.health <= 0:
            continue

        world_pos = enemy.gamePos
        radius: float = enemy.attackRange * 1.1
        theta: float = 0

        word_space = []
        while theta < 2 * 3.14:
            x = world_pos['x'] + radius * math.cos(theta)
            y = world_pos['y']
            z = radius * math.sin(theta) + world_pos['z']
            word_space.append(pymeow.wts_ogl(lReader.overlay, lReader.viewProjMatrix.tolist(),
                                             {'x': x, 'y': y, 'z': z}))
            theta += 0.01

        i = 0
        while i < len(word_space) - 1:
            pymeow.line_v(
                word_space[i],
                word_space[i + 1],
                3,
                pymeow.rgb("red")
            )
            i += 1


def game_analytics(lReader: LeagueReader, pymeow):
    pass
