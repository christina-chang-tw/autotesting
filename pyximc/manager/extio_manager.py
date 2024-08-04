"""
extio_manager.py

External input / output settings Manager.
"""
from enum import Enum

import libximc.highlevel as ximc
from libximc.highlevel import ExtioModeFlags, ExtioSetupFlags

class EXTIOManager:
    """External input / output settings Manager."""
    class InputFlag(Enum):
        EXTIO_SETUP_MODE_IN_STOP = 1
        EXTIO_SETUP_MODE_IN_PWOF = 2
        EXTIO_SETUP_MODE_IN_MOVR = 3
        EXTIO_SETUP_MODE_IN_HOME = 4
        EXTIO_SETUP_MODE_IN_ALARM = 5

    class OutputFlag(Enum):
        EXTIO_SETUP_MODE_OUT_MOVING = 1
        EXTIO_SETUP_MODE_OUT_ALARM = 2
        EXTIO_SETUP_MODE_OUT_MOTOR_ON = 3

    class Direction(Enum):
        INPUT = "i"
        OUTPUT = "o"
        INV_OUTPUT = "r"

    def __init__(self, axis: ximc.Axis):
        self.axis = axis

    def set_flags(self, direction: Direction, flag: ExtioModeFlags) -> None:
        """
        Set the input and output flags for the external input / output.

        Parameter
        ---------
        direction : Direction
            The direction of the external input / output.
        flag : ExtioModeFlags
            The flag to set.
        """
        extio_settings = self.axis.get_extio_settings()
        if direction == EXTIOManager.Direction.INPUT:
            extio_settings.EXTIOSetupFlags = 0
        if direction in [EXTIOManager.Direction.OUTPUT, EXTIOManager.Direction.INV_OUTPUT]:
            extio_settings.EXTIOSetupFlags = ExtioSetupFlags.EXTIO_SETUP_OUTPUT
            if direction == EXTIOManager.Direction.INV_OUTPUT:
                extio_settings.EXTIOSetupFlags |= ExtioSetupFlags.EXTIO_SETUP_INVERT

        extio_settings.EXTIOModeFlags = flag
        self.axis.set_extio_settings(extio_settings)
