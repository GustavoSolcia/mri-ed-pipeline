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
    plt.savefig(path / "svg" / "fid_signal.svg")
    plt.savefig(path / "pdf" / "fid_signal.pdf")

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
    plt.savefig(path / "svg" / "1d_se_signal.svg")
    plt.savefig(path / "pdf" / "1d_se_signal.pdf")

    return fig


def plot_brain_decay(
    tr: float,
    echo_times: list[int],
    path: pathlib.Path
) -> plt.Figure:
    """Plot brain tissues in function of TE.

    Args:
        tr: Sequence TR parameter
        echo_times: List of echo times for figure drawing.
        path: Path for saving the figure.

    Returns:
        fig (plt.Figure): Figure output for logging purposes.
    """

    TISSUES = {
        "CSF": {
            "rho": 1.00,
            "t1": 2569.0,
            "t2": 329.0
        },
        "GM": {
            "rho": 0.86,
            "t1": 833.0,
            "t2": 83.0
        },
        "WM": {
            "rho": 0.77,
            "t1": 500.0,
            "t2": 70.0
        },
    }

    # x-axis limits
    MIN_TE = 0
    MAX_TE = 450
    N_TE = 500

    #y-axis limits
    MIN_RHO = 0
    MAX_RHO = 1

    te = np.linspace(MIN_TE, MAX_TE, N_TE)

    signal_csf = _compute_signal(
        te, tr, **TISSUES["CSF"]
    )
    signal_wm = _compute_signal(
        te, tr, **TISSUES["WM"]
    )
    signal_gm = _compute_signal(
        te, tr, **TISSUES["GM"]
    )

    figsize = (SINGLE_COLUMN_SIZE, SINGLE_COLUMN_SIZE)

    fig, ax = plt.subplots(1, figsize=figsize, dpi=300)
    sns.set_theme(context="paper", style="ticks")

    plt.plot(te, signal_csf, color='k', label='CSF')
    plt.plot(te, signal_wm, color='#99c6cc', label="WM")
    plt.plot(te, signal_gm, color='#ff5a5e', label="GM")
    plt.vlines(
        echo_times, ymin=MIN_RHO, ymax=MAX_RHO, colors="k", linestyles="dashed"
    )
    plt.xlabel('TE (ms)')
    plt.ylabel(r"$\rho\,(1-e^{-TR/T_1})\,e^{-TE/T_2}$")

    plt.xlim([MIN_TE, MAX_TE])
    plt.ylim([MIN_RHO, MAX_RHO])

    plt.legend()
    plt.tight_layout()
    plt.savefig(path / "svg" / "brain_decay.svg")
    plt.savefig(path / "pdf" / "brain_decay.pdf")

    return fig


def _compute_signal(
    te: np.array,
    tr: float,
    rho: float,
    t1: float,
    t2: float
) -> np.array:
    """Helper function to compute signal according to parameters.

    Args:
        te: Echo time array in milliseconds.
        tr: Sequence TR parameter.
        rho: Proton density parameter.
        t1: Tissue T1 parameter.
        t2: Tissue T2 parameter.

    Returns:
        signal: Signal in function of TE.
    """

    signal = rho * (1 - np.exp(-tr / t1)) * np.exp(-te / t2)

    return signal
