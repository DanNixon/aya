import numpy as np
import solid as sp

import layout, utils


def place_switch(position, orientation):
    return sp.translate(position)(
        sp.rotate((0, 0, orientation))(sp.square([14, 14], center=True))
    )


def switch_cutouts(positions, orientations):
    for a in range(0, layout.num_switches):
        col, row = divmod(a, layout.matrix_rows)
        yield place_switch(positions[col, row], orientations[col, row])


def mcu_header_cutouts(mcu_position):
    return sp.translate(mcu_position)(
        [
            sp.translate([x, -1.2])(sp.square([4.5, 33], center=True))
            for x in [-7.6, 7.6]
        ],
    )


def case_outline(outline):
    return sp.minkowski()(
        sp.polygon(points=outline),
        sp.circle(r=15.),
    )


def case_panel(outline, mounting_holes):
    return sp.difference()(
        case_outline(outline),
        [
            sp.translate(p)(
                sp.circle(d=layout.mounting_hole_diameter, segments=32)
            ) for p in mounting_holes
        ],
    )
