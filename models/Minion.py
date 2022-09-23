from . import Entity
from pymem import Pymem
from resources import Offsets

class MinionEntity(Entity):       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)