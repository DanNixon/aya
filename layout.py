import numpy as np

import utils

matrix_rows = 5
matrix_cols = 7
num_switches = matrix_rows * matrix_cols

thumb_cluster_switch_angle = 30.

switch_spacing = 19.5

mounting_hole_diameter = 3.5

split_offset = np.array([80., 0.])


def generate_switch_positions():
    positions = np.ndarray((matrix_cols, matrix_rows, 2), dtype=float)

    for x in range(matrix_cols):
        positions[x, :, 0] = switch_spacing * x
    for y in range(matrix_rows):
        positions[:, y, 1] = -switch_spacing * y

    positions[6, :4, 1] += -17.
    positions[5, :4, 1] += -17.
    positions[4, :4, 1] += -15.
    positions[3, :4, 1] += -1.
    positions[2, :4, 1] += 5.
    positions[1, :4, 1] += 0.
    positions[0, :4, 1] += -1.

    positions[0, 4] = positions[0, 2] + np.array([-switch_spacing, 0])

    positions[1:3, 4] += np.array([-switch_spacing / 2., -1.])

    d = positions[0, 3] - (switch_spacing * np.array([1.2, 0.3]))
    positions[3, 4] = d
    positions[4, 4] = utils.rotate(
        d + np.array([-switch_spacing, 0]), d, thumb_cluster_switch_angle
    )
    positions[5, 4] = utils.rotate(
        d + np.array([0, -switch_spacing]), d, thumb_cluster_switch_angle
    )
    positions[6, 4] = utils.rotate(
        d + np.array([-switch_spacing, -switch_spacing]), d, 30
    )

    return positions


def generate_switch_orientations():
    orientations = np.zeros(shape=(matrix_cols, matrix_rows), dtype=float)
    orientations[3:, 4] = thumb_cluster_switch_angle
    return orientations


def generate_board_outline():
    switch_positions = generate_switch_positions()

    return np.array(
        [
            switch_positions[0, 0] + np.array([-20., 0.]),
            switch_positions[4, 4],
            switch_positions[6, 4],
            switch_positions[6, 3],
            switch_positions[6, 0],
            switch_positions[2, 0],
        ]
    )


def generate_mounting_holes():
    switch_positions = generate_switch_positions()

    return np.array(
        [
            utils.midpoint(switch_positions[6, 0], switch_positions[6, 1]) +
            np.array([10., 0.]),
            utils.midpoint(switch_positions[6, 2], switch_positions[6, 3]) +
            np.array([10., 0.]),
            utils.midpoint(switch_positions[5, 0], switch_positions[4, 1]),
            utils.midpoint(switch_positions[5, 2], switch_positions[4, 3]),
            utils.midpoint(switch_positions[2, 0], switch_positions[3, 1]),
            utils.midpoint(switch_positions[2, 2], switch_positions[3, 3]),
            utils.midpoint(switch_positions[0, 0], switch_positions[1, 1]),
            utils.midpoint(switch_positions[0, 2], switch_positions[1, 3]),
            switch_positions[4, 0] + np.array([0., 15.]),
            switch_positions[3, 3] + np.array([0., -26.]),
            switch_positions[1, 0] + np.array([0., 12.]),
            switch_positions[1, 4] + np.array([-10., -17.]),
            switch_positions[0, 4] + np.array([-20., -10.]),
            utils.midpoint(switch_positions[4, 4], switch_positions[5, 4]),
        ]
    )


def generate_mcu_position():
    switch_positions = generate_switch_positions()
    return switch_positions[0, 0] + np.array([-22., -10.])
