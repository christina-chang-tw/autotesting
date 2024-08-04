"""
chip_manager.py

Chip configuration manager.
"""
from dataclasses import dataclass

@dataclass
class ChipConfig:
    x: float = 0 # x origin reference point
    y: float = 0 # y origin reference point
    width: float = None # from cross to cross
    height: float = None
    angle: float = None


def find_chip_crossing() -> ChipConfig:
    """
    Using image recognition to locate the exact position of the crosses.
    """
    pass
