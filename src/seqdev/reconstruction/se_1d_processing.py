"""Spin echo 1D (SE-1D) post-processing."""

import pathlib

from seqdev.base.base_processing import BaseProcessing
from seqdev.data_load.load_signal import load_signal_mat
from seqdev.plotting.plots import plot_se_decay


class SpinEcho1DProcessing(BaseProcessing):
    """Spin echo 1D (SE-1D) processing class."""

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

        plot_se_decay(
            self.signal["t"],
            self.signal["mag"],
            path.parent / "figures"
        )
