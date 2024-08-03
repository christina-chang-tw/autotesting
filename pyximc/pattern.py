from typing import Callable

import numpy as np
from scipy import stats

def sampler(center: float, width: float, npts: int=25, std: float=0.2) -> np.ndarray:
    """
    Sampling the points with a normal distribution around the center.
    """
    dist = stats.norm(loc=0.5, scale=std)
    pp = np.linspace(*dist.cdf([0, 1]), num=npts)
    vals = dist.ppf(pp)
    vals = width*(vals - 1/2) + center

    return vals

def grid_search(x: float, y: float, func: Callable):
    """
    Perform a grid search to find the best position.

    Parameters
    ----------
    x : float
        The x position of the grating coupler.
    y : float
        The y position of the grating coupler.
    func : Callable
        The sampler function. This should be a partial function like this: partial(sampler, width=..., npts=..., std=...).
    """
    xs = func(center=x)
    ys = func(center=y)
    xs, ys = np.meshgrid(x, y)
    return xs, ys