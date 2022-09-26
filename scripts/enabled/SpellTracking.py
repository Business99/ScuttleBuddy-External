# Importing LeagueReader for typing intellisense
import math
import os
from scripts.helpers import Draw
from utils import world_to_screen


# Setup function | only runs once on script load
def setup() -> dict:
    scriptSettings: dict = {
        "DrawCDSelf": {
            "displayName": "DrawCDSelf",
            "isEnabled": False
        },
        "DrawCDEnemy": {
            "displayName": "DrawCDEnemy",
            "isEnabled": True
        },
    }

    return scriptSettings


# OnTick function | Runs every tick
def on_tick(lReader, pymeow, scriptSettings) -> None:
    if scriptSettings["DrawCDSelf"]["isEnabled"]:
        draw_champion_spells(lReader.localPlayer, pymeow, lReader.viewProjMatrix)
    if scriptSettings["DrawCDEnemy"]["isEnabled"]:
        for champ in lReader.get_players():
            if champ.teamId != lReader.localPlayer.teamId:
                draw_champion_spells(champ, pymeow, lReader.viewProjMatrix)


def draw_champion_spells(champion, pymeow, vpmatrix):
    if not (champion.isVisible and champion.onScreen):
        return
    globaloffset = -70
    diff = 50
    yoff = 200
    zoff = 50
    worldx, worldy, worldz = champion.gamePos.values()
    qreadyin, wreadyin, ereadyin, rreadyin = [(-1 if champion.spells[x].level == 0 else champion.spells[x].readyIn) for
                                              x in range(4)]
    qspell = world_to_screen(vpmatrix, 1920, 1080, worldx + globaloffset, worldy + yoff, worldz + zoff)
    wspell = world_to_screen(vpmatrix, 1920, 1080, worldx + globaloffset + diff, worldy + yoff, worldz + zoff)
    espell = world_to_screen(vpmatrix, 1920, 1080, worldx + globaloffset + 2 * diff, worldy + yoff, worldz + zoff)
    rspell = world_to_screen(vpmatrix, 1920, 1080, worldx + globaloffset + 3 * diff, worldy + yoff, worldz + zoff)
    draw_spell(qspell, pymeow, qreadyin)
    draw_spell(wspell, pymeow, wreadyin)
    draw_spell(espell, pymeow, ereadyin)
    draw_spell(rspell, pymeow, rreadyin)


def draw_spell(position, pymeow, isReady):
    if position[0] is None:
        return
    if isReady == 0:
        c = "green"
    elif 0< isReady <= 1:
        c = "orange"
    else:
        c = "red"
    Draw.circle(
        pymeow,
        x=lr_correction(position[2]),
        y=1080 - position[3],
        radius=10,
        filled=True,
        color=c
    )


def lr_correction(x):
    mid = 970
    toofarright = x - mid
    return x - toofarright / 50