import math
import os
from types import PlayerEntity, TurretEntity, WardEntity


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
        },
        "enemyTurretRangeESP": {
            "displayName": "Turret Range ESP",
            "isEnabled": True
        }
    }
    return scriptSettings


# OnTick function | Runs every tick
def on_tick(lReader, pymeow, scriptSettings) -> None:
    font = pymeow.font_init(20, "ComicSans")

    enemies: list[PlayerEntity] = [enemy for enemy in lReader.enemyPlayers]
    turrets: list[TurretEntity] = [turret for turret in lReader.turrets]
    localPlayer: PlayerEntity = lReader.localPlayer
    wards: list[WardEntity] = [ward for ward in lReader.wards]
    overlay, viewProjMatrix = lReader.overlay, lReader.viewProjMatrix

    if scriptSettings['playerAttackRange']['isEnabled']:
        draw_player_attack_range(pymeow, localPlayer, overlay, viewProjMatrix)
    if scriptSettings['enemyAttackRange']['isEnabled']:
        draw_enemy_attack_range(pymeow, enemies, overlay, viewProjMatrix)
    if scriptSettings['summonerSpellESP']['isEnabled']:
        draw_summoner_spells(pymeow, font, enemies)
    if scriptSettings['enemyTurretRangeESP']['isEnabled']:
        draw_enemy_turret_range(pymeow, turrets, localPlayer, overlay, viewProjMatrix)


def draw_summoner_spells(pymeow, font, enemies):
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


def draw_player_attack_range(pymeow, localPlayer, overlay, viewProjMatrix):
    if localPlayer.onScreen and localPlayer.health > 0:
        player = localPlayer
        world_pos = player.gamePos
        radius: float = localPlayer.attackRange * 1.1
        draw_circle_at(pymeow, world_pos, radius, pymeow.rgb("blue"), overlay, viewProjMatrix)


def draw_enemy_attack_range(pymeow, enemies, overlay, viewProjMatrix):
    for enemy in enemies:
        if not enemy.onScreen or enemy.health <= 0:
            continue

        world_pos = enemy.gamePos
        radius: float = enemy.attackRange * 1.1
        draw_circle_at(pymeow, world_pos, radius, pymeow.rgb("red"), overlay, viewProjMatrix)


def draw_enemy_turret_range(pymeow, turrets, localPlayer, overlay, viewProjMatrix):
    for t in turrets:
        if not t.onScreen or t.teamId == localPlayer.teamId:
            continue

        world_pos = t.gamePos
        radius: float = t.turretAttackRange * 1.05
        draw_circle_at(pymeow, world_pos, radius, pymeow.rgb("red"), overlay, viewProjMatrix)
        

def draw_circle_at(pymeow, pos, radius, color, overlay, viewProjMatrix):
    theta: float = 0

    word_space = []
    while theta < 2 * 3.14:
        x = pos['x'] + radius * math.cos(theta)
        y = pos['y']
        z = radius * math.sin(theta) + pos['z']
        word_space.append(pymeow.wts_ogl(overlay, viewProjMatrix.tolist(),
                                         {'x': x, 'y': y, 'z': z}))
        theta += 0.01

    i = 0
    while i < len(word_space) - 1:
        pymeow.line_v(
            word_space[i],
            word_space[i + 1],
            3,
            color
        )
        i += 1