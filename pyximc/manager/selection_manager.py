"""
selection_manager.py

Device selection Manager.
"""
import os
import platform
from enum import Enum
from typing import List, Union

import libximc.highlevel as ximc
from libximc.highlevel import EnumerateFlags

class SelectionManager:
    """ Device selection Manager. """
    class DeviceType(Enum):
        COM_DEVICE = 1
        VIRT_DEVICE = 2
        NETWORK_DEVICE = 3
        ALL_DEVICES = 4

    def get_uri(self, device_type: DeviceType, param: Union[int, str]=None) -> str:
        """
        Device selection Manager.

        Parameters:
        -----------
        device_type [DeviceType]
            Type of the device to connect to.

        Returns:
        --------
        uri : str
            URI of the device to open.
        """
        if device_type == SelectionManager.DeviceType.COM_DEVICE:
            # i.e. xi-com:\\.\COM1
            if platform.system() == "Windows":
                uri = r"xi-com:\\.\COM" + param
            else:
                uri = f"xi-com:/dev/tty.s{param}"

        elif device_type == SelectionManager.DeviceType.VIRT_DEVICE:
            if param:
                uri = f"xi-emu///{param}"
            else:
                uri = "xi-emu:///" + os.path.join(os.path.expanduser('~'), "virtual_controller.bin")

        elif device_type == SelectionManager.DeviceType.NETWORK_DEVICE:
            # i.e. xi-net://192.168.0.1
            return f"xi-net://{param}"

        else:
            raise RuntimeError(f"Wrong device type! Got {device_type}")

        return uri
        
    @staticmethod
    def get_devices_enumeration() -> List:
        # ******************************************** #
        #         Device searching and probing         #
        # ******************************************** #

        # Flags explanation:
        # ximc.EnumerateFlags.ENUMERATE_PROBE   -   Probing found devices for detailed info.
        # ximc.EnumerateFlags.ENUMERATE_NETWORK -   Check network devices.
        enum_flags = EnumerateFlags.ENUMERATE_PROBE | EnumerateFlags.ENUMERATE_NETWORK
        # Hint explanation:
        # "addr=" hint is used for broadcast network enumeration
        enum_hints = "addr="
        return ximc.enumerate_devices(enum_flags, enum_hints)
    
    @staticmethod
    def create_virtual_device():
        tempdir = os.path.join(os.path.expanduser('~'), "testdevice.bin")
        return "xi-emu:///" + tempdir