#!/usr/bin/env python3

import numpy as np
import solid as sp

import cad, layout, utils

angle = 6.
split_offset = np.array([52., 0.])

switch_positions = layout.generate_switch_positions()

mounting_holes = np.array(
    [
        *utils.
        rotate(layout.generate_mounting_holes() + split_offset, degrees=angle),
        *utils.rotate(
            utils.mirror_in_x(layout.generate_mounting_holes()) - split_offset,
            degrees=-angle
        ),
    ]
)

board_outline = np.array(
    [
        *utils.rotate(
            layout.generate_partial_board_outline() + split_offset,
            degrees=angle
        ),
        *utils.rotate(
            utils.mirror_in_x(layout.generate_partial_board_outline()) -
            split_offset,
            degrees=-angle
        )[::-1],
    ]
)

u = cad.case_panel(board_outline, mounting_holes)
print(sp.scad_render(u))
