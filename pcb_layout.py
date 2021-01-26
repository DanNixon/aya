#!/usr/bin/env python3

from collections import namedtuple
import numpy as np
import pcbnew
import sys

import layout, utils

component_references = namedtuple(
    "component_references",
    "switch_and_diode_start mcu i2c_header scl_pullup sda_pullup reset_sw"
)

lhs = component_references(
    switch_and_diode_start=36,
    mcu="B2",
    i2c_header="J2",
    scl_pullup="R3",
    sda_pullup="R4",
    reset_sw="SW72",
)

rhs = component_references(
    switch_and_diode_start=1,
    mcu="B1",
    i2c_header="J1",
    scl_pullup="R1",
    sda_pullup="R2",
    reset_sw="SW71",
)


def pcb_point(p):
    return pcbnew.wxPoint(*(p * np.array([1., -1.]) * 1e6))


def do_flip(part):
    if not part.IsFlipped():
        part.Flip(part.GetPosition())


def place_switch(board, ref_no, position, orientation):
    switch_centre_offset = np.array([2.56, 5.08])
    diode_switch_offset = np.array([4., -9.])

    switch_position = utils.rotate(
        position + switch_centre_offset, position, orientation
    )
    diode_position = utils.rotate(
        position + diode_switch_offset, position, orientation
    )

    switch = board.FindModuleByReference(f'SW{ref_no}')
    diode = board.FindModuleByReference(f'D{ref_no}')

    switch.SetPosition(pcb_point(switch_position))
    switch.SetOrientationDegrees(orientation)
    switch.Reference().SetVisible(False)

    diode.SetPosition(pcb_point(diode_position))
    diode.SetOrientationDegrees(180. + orientation)
    diode.Reference().SetVisible(False)


def place_electronics(board, ref, mcu_position):
    mcu = board.FindModuleByReference(ref.mcu)
    mcu.SetPosition(pcb_point(mcu_position))
    mcu.SetOrientationDegrees(0.)
    mcu.Reference().SetVisible(False)

    i2c_header = board.FindModuleByReference(ref.i2c_header)
    i2c_header.SetPosition(pcb_point(mcu_position + np.array([-4., 8.])))
    i2c_header.SetOrientationDegrees(90.)
    i2c_header.Reference().SetVisible(False)

    sda_pullup = board.FindModuleByReference(ref.scl_pullup)
    sda_pullup.SetPosition(pcb_point(mcu_position + np.array([1.75, -4.])))
    sda_pullup.SetOrientationDegrees(90.)
    sda_pullup.Reference().SetVisible(False)

    scl_pullup = board.FindModuleByReference(ref.sda_pullup)
    scl_pullup.SetPosition(pcb_point(mcu_position + np.array([-1.75, -4.])))
    scl_pullup.SetOrientationDegrees(90.)
    scl_pullup.Reference().SetVisible(False)

    reset_sw = board.FindModuleByReference(ref.reset_sw)
    reset_sw.SetPosition(pcb_point(mcu_position + np.array([0., 15.])))
    reset_sw.SetOrientationDegrees(0.)
    reset_sw.Reference().SetVisible(False)
    do_flip(reset_sw)


def place_switches(board, reg, positions, orientations):
    for a in range(0, layout.num_switches):
        col, row = divmod(a, layout.matrix_rows)
        place_switch(
            board, reg.switch_and_diode_start + a, positions[col, row],
            orientations[col, row]
        )


def remove_all_mounting_holes(board):
    for m in board.GetModules():
        if m.GetReference().startswith("HOLE"):
            board.Remove(m)


mounting_hole_counter = 1


def place_mounting_holes(board, positions):
    hole = pcbnew.FootprintLoad(
        "/usr/share/kicad/modules/MountingHole.pretty", "MountingHole_3.2mm_M3"
    )
    for pos in positions:
        global mounting_hole_counter
        h = pcbnew.MODULE(hole)
        h.SetReference("HOLE{}".format(mounting_hole_counter))
        h.SetPosition(pcb_point(pos))
        h.Reference().SetVisible(False)
        board.Add(h)
        mounting_hole_counter += 1


def place_right_hand_side(board):
    switch_positions = layout.generate_switch_positions() + layout.split_offset
    switch_orientations = layout.generate_switch_orientations()
    place_switches(board, rhs, switch_positions, switch_orientations)

    mcu_position = layout.generate_mcu_position() + layout.split_offset
    place_electronics(board, rhs, mcu_position)

    mounting_hole_positions = layout.generate_mounting_holes(
    ) + layout.split_offset
    place_mounting_holes(board, mounting_hole_positions)


def place_left_hand_side(board):
    switch_positions = utils.mirror_in_x(
        layout.generate_switch_positions()
    ) - layout.split_offset
    switch_orientations = layout.generate_switch_orientations() * -1
    place_switches(board, lhs, switch_positions, switch_orientations)

    mcu_position = utils.mirror_in_x(
        layout.generate_mcu_position() + layout.split_offset
    )
    place_electronics(board, lhs, mcu_position)

    mounting_hole_positions = utils.mirror_in_x(
        layout.generate_mounting_holes()
    ) - layout.split_offset
    place_mounting_holes(board, mounting_hole_positions)


filename = sys.argv[1]
board = pcbnew.LoadBoard(filename)
remove_all_mounting_holes(board)
place_right_hand_side(board)
place_left_hand_side(board)
board.Save(filename)
