"""
general_manager.py

General manager to initiliase required specific managers.
"""
from typing import Tuple, Callable

import numpy as np
import libximc.highlevel as ximc

from .extio_manager import EXTIOManager
from .motion_manager import MotionManager
from .setting_manager import SettingManager
from .chip_manager import ChipConfig

class GeneralManager:
    """
    General manager to initiliase required specific managers.
    """
    def __init__(self, xaxis: ximc.Axis, yaxis: ximc.Axis, chip_config: ChipConfig):
        self.chip_config = chip_config
        self.xaxis = xaxis
        self.xmotion_manager = MotionManager(xaxis)
        self.xextio_manager = EXTIOManager(xaxis)
        self.xsettings_manager = SettingManager(xaxis)

        self.yaxis = yaxis
        self.ymotion_manager = MotionManager(yaxis)
        self.yextio_manager = EXTIOManager(yaxis)
        self.ysettings_manager = SettingManager(yaxis)

        self.xaxis.open_device()
        self.yaxis.open_device()

    def move(self, x: float, y: float):
        """ Move the arm to the specified position. """
        self.xmotion_manager.move(x)
        self.ymotion_manager.move(y)

    def move_user(self, x: float, y: float):
        """ Move the arm to the specified position with user specified unit. """
        self.xmotion_manager.move_user(x)
        self.ymotion_manager.move_user(y)

    def wait_for_stop_ms(self, interval: int):
        """ Wait for the arm to stop moving. """
        self.xmotion_manager.wait_for_stop_ms(interval)
        self.ymotion_manager.wait_for_stop_ms(interval)

    def get_pos(self):
        """ Get the current position of the arm. """
        return self.xmotion_manager.get_pos(), self.ymotion_manager.get_pos()

    def get_pos_user(self):
        """ Get the current position of the arm with user specified unit. """
        return self.xmotion_manager.get_pos_user(), self.ymotion_manager.get_pos_user()

    @staticmethod
    def _calc_position(x: float, y: float, angle: float) -> Tuple[float, float]:
        """
        Given an x and y coordinate, calculate the correct position after rotation.

        Parameters
        ----------
        x : float
            The x position of the grating coupler.
        y : float
            The y position of the grating coupler.
        angle : float
            The rotated angle of the chip. This should be in radian format.
        """
        rotation_matrix = np.array(
            [[np.cos(angle), -np.sin(angle)],
                [np.sin(angle), np.cos(angle)]]
        )
        points = np.array([x, y])
        return rotation_matrix.dot(points)

    def align_to_max_pos(self, x: float, y: float, func: Callable) -> None:
        """
        Align the grating coupler to the chip.
        
        Parameters
        ----------
        x : float
            The x position of the grating coupler.
        y : float
            The y position of the grating coupler.
        func : Callable
            The search algorithm
        """
        pos = self._calc_position(self.chip_config.x - x,
                                  self.chip_config.y + y, self.chip_config.angle)
        xs, ys = func(*pos)
        for x in xs:
            self.xmotion_manager.move(x)
            self.xmotion_manager.wait_for_stop_ms(1)
            for y in ys:
                self.ymotion_manager.move(y)
                self.ymotion_manager.wait_for_stop_ms(1)
                # record the power
