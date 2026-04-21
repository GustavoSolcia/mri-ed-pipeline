"""Reconstruction functions."""

import numpy as np


def fft_2d(kspace: np.array) -> np.array:
    """Apply 2d fft for each slice in the kspace.

    Args:
        kspace (np.array): K-space with a fez slices in the z direction.

    Returns:
        img (np.array): Fourier transformed image.
    """

    img = []
    for k_slice in kspace:
        img.append(np.fft.fftshift(np.fft.fft2(k_slice)))
    img = np.permute_dims(np.array(img), axes=[2, 1, 0])

    return img
