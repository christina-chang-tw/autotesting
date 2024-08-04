"""
fitting.py

This module contains the fitting algorithms used to find the maximum position of the 2D plane.
"""
from typing import Tuple

import numpy as np
from scipy.interpolate import RectBivariateSpline

def find_max_pos(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Tuple[float, float]:
    # 2D plane fitting
    fit_func = RectBivariateSpline(x, y, z.T)
    xnew = np.linspace(min(x), max(x), len(x)*5)
    ynew = np.linspace(min(y), max(y), len(y)*5)
    znew = fit_func(xnew, ynew)

    xidx, yidx = np.unravel_index(np.argmax(znew), znew.shape)

    return xnew[xidx], ynew[yidx]
