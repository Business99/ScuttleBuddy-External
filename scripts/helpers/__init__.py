# region Calculate Class
class Calculate:
    @staticmethod
    def calculate_magic_damage(source, target, damage: float) -> float:
        targetMagicResist: float = target.magicResist
        sourceMagicPenFlat: float = source.magicPenFlat
        sourceMagicPenPerc: float = source.magicPenPercent

        unknown = targetMagicResist - sourceMagicPenFlat

        unknown = unknown / 100 * (100 - sourceMagicPenPerc)

        if unknown < 0:
            return damage * (2 - (100 / (100 - unknown)))

        return damage * (100 / (100 + unknown))

    @staticmethod
    def calculate_physical_damage(source, target, damage: float) -> float:
        targetArmor: float = target.armor
        sourceLethality: float = source.lethality
        sourceArmorPenPerc: float = source.armorPenPercent

        flatArmorPen = sourceLethality * (0.6 + (0.4 * source.level / 18))

        unknown = targetArmor - flatArmorPen
        unknown = unknown / 100 * (100 - sourceArmorPenPerc)

        if unknown < 0:
            return damage * (2 - (100 / (100 - unknown)))

        return damage * (100 / (100 + unknown))

    @staticmethod
    def world_to_screen(view_proj_matrix, width, height, x, y, z):
        clip_coords_x = x * view_proj_matrix[0] + y * view_proj_matrix[4] + z * view_proj_matrix[8] + view_proj_matrix[
            12]
        clip_coords_y = x * view_proj_matrix[1] + y * view_proj_matrix[5] + z * view_proj_matrix[9] + view_proj_matrix[
            13]
        clip_coords_w = x * view_proj_matrix[3] + y * view_proj_matrix[7] + z * view_proj_matrix[11] + view_proj_matrix[
            15]

        if clip_coords_w < 1.:
            clip_coords_w = 1.

        M_x = clip_coords_x / clip_coords_w
        M_y = clip_coords_y / clip_coords_w

        out_x = (width / 2. * M_x) + (M_x + width / 2.)
        out_y = -(height / 2. * M_y) + (M_y + height / 2.)

        if 0 <= out_x <= width and 0 <= out_y <= height:
            return out_x, out_y, out_x, out_y

        return None, None, out_x, out_y

# endregion

class Draw:
    @staticmethod
    def circle(pymeow, x: float, y: float, radius: float, color: str, filled: bool = False, lineWidth: float = 1.0):
        pymeow.circle(x, y, radius, pymeow.rgb(color), filled, lineWidth)
