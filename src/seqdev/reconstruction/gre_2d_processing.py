"""Gradient echo 2D (GRE-2D) post-processing."""

import pathlib

import numpy as np

from seqdev.base.base_processing import BaseProcessing
from seqdev.data_load.load_signal import load_signal_mat
from seqdev.reconstruction.kspace import build_2d_kspace
from seqdev.reconstruction.recon import fft_2d
from seqdev.utils.nii import write_2d_nii


class GradientEcho2DProcessing(BaseProcessing):
    """Gradient echo 2D (GRE-2D) processing class."""

    def load_signal(
        self,
        sequence: str,
        path: pathlib.Path
    ) -> None:
        """Load signal from file

        Args:
            sequence (str): Sequence type.
            path (pathlib.Path): Path to the signal file
        """

        self.signal = load_signal_mat(path / "simulation", sequence)
        return self

    def process(
        self,
        parameters: dict,
        phantom: str,
        sequence: str,
        path: pathlib.Path
    ) -> None:
        """Process phantom signal according to sequence type.

        Args:
            parameters (dict): Sequence parameters.
            phantom (str): Phantom name.
            path (pathlib.Path): Parent path from raw data to save processed
                data.
        """

        kspace = build_2d_kspace(
            self.signal["real"],
            self.signal["imag"],
            parameters["n_x"],
            parameters["n_y"],
            parameters["n_slices"]
        )

        img = fft_2d(kspace)

        write_2d_nii(
            np.abs(np.flip(kspace, axis=1)),
            f"{phantom}_{sequence}_kspace",
            path / "nii"
        )
        write_2d_nii(
            np.abs(np.flip(img, axis=1)),
            f"{phantom}_{sequence}_mag",
            path / "nii"
        )
