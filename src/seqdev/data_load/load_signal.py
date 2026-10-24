"""One dimensional signal load functions."""

import pathlib

import numpy as np
from scipy.io import loadmat


def load_signal_mat(
    path: pathlib.Path,
    sequence: str
) -> dict:
    """Loads one dimensional signal from mat file.

    It considers that the times where stored as 'adc_sampling_times' and
    the signal data was stored as 'raw'.

    Args:
        path (pathlib.Path): Simulation result data path.
        sequence (str): Sequence name as stored in data.

    Returns:
        signal (dict): Signal dictionary containing time, real, imaginary,
            and magnitude data.
    """

    signal_mat = loadmat(path / f"{sequence}.mat")

    t = signal_mat["adc_sampling_times"]

    signal_complex = signal_mat["raw"][:, 0, 0]

    signal = {
        "t": t.flatten(),
        "real": np.real(signal_complex),
        "imag": np.imag(signal_complex),
        "mag": np.abs(signal_complex)
    }

    return signal
