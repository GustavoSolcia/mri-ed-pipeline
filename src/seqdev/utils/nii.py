"""Neuroimaging Informatics Technology Initiative (NIfTI) utility functions."""

from pathlib import Path

import nibabel as nib
import numpy as np


def write_2d_nii(
    img: np.array,
    tag: str,
    path: Path
) -> None:
    """Writes NIfTI image from given image.

    Args:
        img (np.array): Desired image for saving
        tag (str): Image name tag.
        path (Path): Image save path.
    """

    header = nib.Nifti2Header()
    header.set_data_shape(img.shape)
    header.set_zooms((0.5, 0.5, 0.5))
    header.set_xyzt_units(2)  # millimeters
    affine = header.get_best_affine()
    nifti_img = nib.Nifti2Image(img, affine, header)
    nib.save(nifti_img, path / f"{tag}.nii.gz")
