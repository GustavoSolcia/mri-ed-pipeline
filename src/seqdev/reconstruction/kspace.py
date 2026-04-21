"""K-space processing functions."""

import numpy as np


def build_2d_kspace(
    real_signal: np.array,
    imag_signal: np.array,
    N_x: int,
    N_y: int,
    N_slices: int
) -> np.array:
    """Builds a 2D Kspace from provided signal and parameters.

    Args:
        real_signal (np.array): Real raw signal acquired.
        imag_signal (np.array): Imaginary raw signal acquired.
        N_x (int): Number of voxels in the x dimension.
        N_y (int): Number of voxels in the y dimension.
        N_slices (int): Number of slices in the z dimension.

    Returns:
        kspace (np.array): K-space with N_slices, of N_x X N_y size.
    """

    real_signal_reshaped = real_signal.reshape(N_slices, N_y, N_x)
    imag_signal_reshaped = imag_signal.reshape(N_slices, N_y, N_x)

    kspace = real_signal_reshaped + 1j * imag_signal_reshaped

    return kspace
