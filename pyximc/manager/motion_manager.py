"""
motion_manager.py

Movement Manager.
"""
from time import sleep
from typing import Tuple

import numpy as np

import libximc.highlevel as ximc
from libximc.highlevel import MvcmdStatus

class MotionManager:
    """ Movement Manager. """
    def __init__(self, axis: ximc.Axis):
        self.axis = axis

    def _decompose_pos(self, step: float) -> Tuple[int, int]:
        """ Decompose the step into integer and fractional part. """
        return map(int, [step, np.round((step - int(step))*1E+03)])

    def move(self, step: float) -> None:
        """ Move to the position. """
        self.axis.command_move(*self._decompose_pos(step))

    def shift(self, step: float) -> None:
        """ Shift on the position delta. """
        self.axis.command_movr(*self._decompose_pos(step))

    def move_user(self, step: int) -> None:
        """ Move to the position in user unit mode. """
        self.axis.command_move_calb(step)

    def shift_user(self, step: int) -> None:
        """ Shift on the position delta in user unit mode. """
        self.axis.command_movr_calb(step)

    def wait_for_stop_ms(self, interval: int) -> None:
        """
        This function performs dynamic output coordinate in the process of moving.

        Parameter
        ---------
        interval : int
            The interval in second
        """
        while self.axis.get_status().MvCmdSts & MvcmdStatus.MVCMD_RUNNING:
            sleep(interval/1000)

    def home(self) -> None:
        """ Go back home! """
        self.axis.command_home()

    def get_pos(self) -> None:
        """ Get the current position. """
        return self.axis.get_position()

    def get_pos_user(self) -> None:
        """ Get the current position in user unit mode. """
        return self.axis.get_position_calb()
    
    def get_status(self) -> None:
        """ Get the current status. """
        return self.axis.get_status()
