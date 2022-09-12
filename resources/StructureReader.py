from pymem import Pymem


class StructureReader:

    @staticmethod
    def read_v_table(pm: Pymem, addr: int) -> list[int]:
        lst: int = pm.read_int(addr + 0x4)
        size: int = pm.read_int(addr + 0x8)
        
        for i in range(0, size, 1):
            yield pm.read_int(lst + (i * 0x4))
