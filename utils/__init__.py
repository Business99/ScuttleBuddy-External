from resources import offsets
from models import PlayerEntity
import numpy as np
import struct


def find_view_proj_matrix(process):
    data = process.read_bytes(process.base_address + offsets.oViewProjMatrix, 0x128)
    view_matrix = list_to_matrix([float_from_buffer(data, i * 4) for i in range(16)])
    proj_matrix = list_to_matrix([float_from_buffer(data, 64 + (i * 4)) for i in range(16)])
    view_proj_matrix = np.matmul(view_matrix, proj_matrix)
    return view_proj_matrix.reshape(16)


def list_to_matrix(floats):
    m = np.array(floats)
    return m.reshape(4, 4)


def float_from_buffer(data, offset):
    f, = struct.unpack('f', data[offset:offset + 4])
    return f


def world_to_screen(view_proj_matrix, width, height, x, y, z):
    clip_coords_x = x * view_proj_matrix[0] + y * view_proj_matrix[4] + z * view_proj_matrix[8] + view_proj_matrix[12]
    clip_coords_y = x * view_proj_matrix[1] + y * view_proj_matrix[5] + z * view_proj_matrix[9] + view_proj_matrix[13]
    clip_coords_w = x * view_proj_matrix[3] + y * view_proj_matrix[7] + z * view_proj_matrix[11] + view_proj_matrix[15]

    if clip_coords_w < 1.:
        clip_coords_w = 1.

    M_x = clip_coords_x / clip_coords_w
    M_y = clip_coords_y / clip_coords_w

    out_x = (width / 2. * M_x) + (M_x + width / 2.)
    out_y = -(height / 2. * M_y) + (M_y + height / 2.)

    if 0 <= out_x <= width and 0 <= out_y <= height:
        return out_x, out_y, out_x, out_y

    return None, None, out_x, out_y


def convert_player_to_json(player: PlayerEntity):
    local: dict = {
        'championName': player.championName,
        'teamId': player.teamId,
        'health': player.health,
        'maxHealth': player.maxHealth,
        'mana': player.mana,
        'maxMana': player.maxMana,
        'spells': player.spells
    }

    localSpells: list = []
    for spell in player.spells:
        spellDict: dict = {
            'name': spell.name,
            'infoName': spell.infoName,
            'readyAt': spell.readyAt,
            'level': spell.level,
            'isReady': spell.isReady,
            'readyIn': spell.readyIn,
            'isSummoner': spell.isSummoner
        }
        localSpells.append(spellDict)

    local['spells'] = localSpells

    return local
