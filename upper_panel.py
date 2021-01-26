#!/usr/bin/env python3

import numpy as np
import solid as sp

import cad, layout, utils


def place_right_hand_side():
    switch_positions = layout.generate_switch_positions() + layout.split_offset
    switch_orientations = layout.generate_switch_orientations()
    board_outline = layout.generate_board_outline() + layout.split_offset
    mounting_holes = layout.generate_mounting_holes() + layout.split_offset
    return sp.difference()(
        cad.case_panel(board_outline, mounting_holes),
        list(cad.switch_cutouts(switch_positions, switch_orientations)),
        cad.mcu_header_cutouts(
            layout.generate_mcu_position() + layout.split_offset
        ),
    )


def place_left_hand_side():
    switch_positions = utils.mirror_in_x(
        layout.generate_switch_positions()
    ) - layout.split_offset
    switch_orientations = layout.generate_switch_orientations() * -1
    board_outline = utils.mirror_in_x(
        layout.generate_board_outline()
    ) - layout.split_offset
    mounting_holes = utils.mirror_in_x(
        layout.generate_mounting_holes()
    ) - layout.split_offset
    return sp.difference()(
        cad.case_panel(board_outline, mounting_holes),
        list(cad.switch_cutouts(switch_positions, switch_orientations)),
        cad.mcu_header_cutouts(
            utils.
            mirror_in_x(layout.generate_mcu_position() + layout.split_offset)
        ),
    )


u = sp.union()(place_right_hand_side(), place_left_hand_side())
print(sp.scad_render(u))
