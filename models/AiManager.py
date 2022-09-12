from pymem import Pymem
import pymeow
from resources import offsets
from functools import cached_property


class AiManager:
    def __init__(self, pm: Pymem, mem, viewProjMatrix, overlay, managerAddr: int):
        self.pm = pm
        self.mem = mem
        self.viewProjMatrix = viewProjMatrix
        self.overlay = overlay
        self.managerAddr = managerAddr

    @cached_property
    def startPath(self) -> dict:
        return pymeow.read_vec3(self.mem, self.managerAddr + offsets.oAiManagerStartPath)

    @cached_property
    def startPathScreen(self) -> dict:
        try:
            wts = pymeow.wts_ogl(self.overlay, self.viewProjMatrix.tolist(), self.startPath)
        except:
            wts = pymeow.vec2()

        return wts

    @cached_property
    def endPath(self) -> dict:
        return pymeow.read_vec3(self.mem, self.managerAddr + offsets.oAiManagerEndPath)

    @cached_property
    def endPathScreen(self):
        try:
            wts = pymeow.wts_ogl(self.overlay, self.viewProjMatrix.tolist(), self.endPath)
        except:
            wts = pymeow.vec2()

        return wts

    @cached_property
    def isDashing(self) -> bool:
        return self.pm.read_bool(self.managerAddr + offsets.oAiManagerIsDashing)

    @cached_property
    def isMoving(self) -> bool:
        return self.pm.read_bool(self.managerAddr + offsets.oAiManagerIsMoving)

    @cached_property
    def dashSpeed(self) -> int:
        return self.pm.read_int(self.managerAddr + offsets.oAiManagerDashSpeed)
