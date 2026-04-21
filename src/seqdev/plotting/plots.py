"""Plot functions."""

import pathlib

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

CM = 1 / 2.54

SINGLE_COLUMN_SIZE = 8.67 * CM
ONE_HALF_COLUMN_SIZE = 13.06 * CM
DOUBLE_COLUMN_SIZE = 17.56 * CM


def plot_fid_decay(
    t: np.array,
    mag: np.array,
    real: np.array,
    imag: np.array,
    path: pathlib.Path
) -> plt.Figure:
    """Plot FID decay with magnitude, real, and imaginary signal.

    Args:
        t (np.array): Time array from ADC sampling times.
        mag (np.array): Magnitude from the signal.
        real (np.array): Real part from the signal.
        imag (np.array): Imaginary part from the signal.
        path (pathlib.Path): Figure saving path.

    Returns:
        fig (plt.Figure): Figure output for logging purposes.
    """

    figsize = (SINGLE_COLUMN_SIZE, SINGLE_COLUMN_SIZE)

    fig, ax = plt.subplots(1, figsize=figsize, dpi=300)
    sns.set_theme(context="paper", style="ticks")

    plt.plot(t, real, color="#8cc5e3", label="Real")
    plt.plot(t, imag, color="#f0b077", label="Imaginary")
    plt.plot(t, mag, color="k", label="Magnitude")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (a.u.)")

    plt.legend()
    plt.tight_layout()
    plt.savefig(path / "svg" / "fid_decay.svg")
    plt.savefig(path / "pdf" / "fid_decay.pdf")

    return fig


def plot_se_decay(
    t: np.array,
    mag: np.array,
    path: pathlib.Path
) -> plt.Figure:
    """Plot SE decay with magnitude, real, and imaginary signal.

    Args:
        t (np.array): Time array from ADC sampling times.
        mag (np.array): Magnitude from the signal.
        path (pathlib.Path): Figure saving path.

    Returns:
        fig (plt.Figure): Figure output for logging purposes.
    """
    water_T2 = 2
    inom_freq = 50
    water_T2_star = 1 / ((1 / water_T2) + inom_freq)

    decay_T2 = np.exp(-t/water_T2)
    decay_T2_star = np.exp(-t/water_T2_star)

    figsize = (SINGLE_COLUMN_SIZE, SINGLE_COLUMN_SIZE)

    fig, ax = plt.subplots(1, figsize=figsize, dpi=300)
    sns.set_theme(context="paper", style="ticks")

    plt.plot(t, mag, color='k', label='Magnitude')
    plt.plot(t, decay_T2, color='#99c6cc', label="$T_2$ decay")
    plt.plot(t, decay_T2_star, color='#ff5a5e', label="$T_2^*$ decay")
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (a.u.)')

    plt.legend()
    plt.tight_layout()
    plt.savefig(path / "svg" / "1d_se_decay.svg")
    plt.savefig(path / "pdf" / "1d_se_decay.pdf")
    return fig
