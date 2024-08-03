from pathlib import Path
import numpy as np
from functools import partial

import libximc.highlevel as ximc

from pyximc.manager import SelectionManager, GeneralManager, ChipConfig
from pyximc.pattern import sampler, grid_search

def main():
    ### Please change this part ################################
    file = Path(r"coord.csv")

    uri_larm_x = SelectionManager().get_uri(SelectionManager.DeviceType.VIRT_DEVICE)
    uri_larm_y = SelectionManager().get_uri(SelectionManager.DeviceType.VIRT_DEVICE)
    uri_rarm_x = SelectionManager().get_uri(SelectionManager.DeviceType.VIRT_DEVICE)
    uri_rarm_y = SelectionManager().get_uri(SelectionManager.DeviceType.VIRT_DEVICE)
    
    ############################################################
    coord = np.loadtxt(file)
    chip_config = ChipConfig(x=0, y=0, width=10, height=20, angle=0)

    axis_larm_x, axis_larm_y = ximc.Axis(uri_larm_x), ximc.Axis(uri_larm_y)
    axis_rarm_x, axis_rarm_y = ximc.Axis(uri_rarm_x), ximc.Axis(uri_rarm_y)

    gm_larm = GeneralManager(xaxis=axis_larm_x, yaxis=axis_larm_y, chip_config=chip_config)
    gm_rarm = GeneralManager(xaxis=axis_rarm_x, yaxis=axis_rarm_y, chip_config=chip_config)

    sam = partial(sampler, width=10, npts=15, std=0.2)
    search_algor = partial(grid_search, func=sam)

    for x0, y0, x1, y1 in coord:
        # move to the specified position, currently only move the x direction...
        gm_larm.move(x0, y0)
        gm_rarm.move(x1, y1)

        gm_larm.wait_for_stop_ms(1)
        gm_rarm.wait_for_stop_ms(1)
        
        gm_larm.align_to_max_pos(x0, y0, search_algor)
        gm_rarm.align_to_max_pos(x1, y1, search_algor)

if __name__ == "__main__":
    main()

