from typing import Dict, Union
from ctypes import c_uint, CDLL, WinDLL

from libximc.highlevel import Axis

def hl_settings(lib: Axis, data: Dict):
    """
    High-level interface user settings.

    Args:
        lib (Axis): Axis object.
        data (Dict): Dictionary with settings. This should be loaded from a yaml file.
    """
    import libximc.highlevel as hlximc
    for key, values in data.items():
        settings = getattr(hlximc, key + "_t")()
        for k, v in values.items():
            if isinstance(v, Union[int, float]):
                setattr(settings, k, v)

            elif isinstance(v, str):
                # since there are two flags in the yaml file, make an exception
                contains = ["name", "manufacturer", "partnumber"]
                if any((val in k.lower() for val in contains)):
                    setattr(settings, k, v)
                    continue

                if "control" in key.lower() and k.lower() == "flags":
                    class_name = getattr(hlximc, "Control" + k)
                else:
                    class_name = getattr(hlximc, k)

                if "," in v:
                    vals = v.split(",")
                    flag = getattr(class_name, vals[0].lstrip().rstrip())
                    for val in vals[1:]:
                        flag |= getattr(class_name, val.lstrip().rstrip())
                else:
                    flag = getattr(class_name, v)
                setattr(settings, k, flag)

            elif isinstance(v, list):
                contains = ["info", "units"]
                if any((val in k.lower() for val in contains)):
                    setattr(settings, k, bytes(v))
                else:
                    v = (c_uint * len(v))(*v)
                    setattr(settings, k, v)

            else:
                raise ValueError(f"Unknown type: {k}: {type(v)}")

        setting_func = getattr(lib, "set_" + key)
        setting_func(settings)


def ll_settings(lib: Union[CDLL, WinDLL], lib_id: int, data: Dict):
    """
    Low-level interface user settings.

    Args:
        lib (Axis): Axis object.
        lib_id (int): Axis ID.
        data (Dict): Dictionary with settings. This should be loaded from a yaml file.
    """
    import libximc.lowlevel as llximc
    import pyximc.settings.ll_flags
    for key, values in data.items():
        settings = getattr(llximc, key + "_t")()
        for k, v in values.items():
            if isinstance(v, Union[int, float]):
                setattr(settings, k, v)

            elif isinstance(v, str):
                # since there are two flags in the yaml file, make an exception
                if "control" in key.lower() and k.lower() == "flags":
                    class_name = getattr(pyximc.settings.ll_flags, "Control_" + k)
                else:
                    class_name = getattr(pyximc.settings.ll_flags, k)

                if "," in v:
                    flag = 0
                    for val in v.split(","):
                        flag |= getattr(class_name, val.lstrip().rstrip())
                else:
                    flag = getattr(class_name, v)
                setattr(settings, k, flag)

            elif isinstance(v, list):
                contains = [
                    "name", "manufacturer",
                    "partnumber", "info", "units"
                ]
                if any((val in k.lower() for val in contains)):
                    setattr(settings, k, bytes(v))
                else:
                    v = (c_uint * len(v))(*v)
                    setattr(settings, k, v)

            else:
                raise ValueError(f"Unknown type: {k}: {type(v)}")
        
        setting_func = getattr(lib, "set_" + key)
        setting_func(lib_id, settings)