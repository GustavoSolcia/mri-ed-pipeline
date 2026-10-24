"""Code for reproducing the brain signal in function of TE"""

import pathlib

from seqdev.plotting.plots import plot_brain_decay


TR = 6000  # Fixed TR in the contrast exploration experiments
ECHO_TIMES = [20, 100, 400]  # Runs echo times for drawing vertical lines

def main(
    tr: float,
    echo_times: list[int],
    path: pathlib.Path
) -> None:
    """Plot function wrapper for reproducing brain signal figure.

    Args:
        tr: Sequence TR parameters.
        echo_times: List of echo times for figure drawing.
        path: Path for saving the figure.
    """

    plot_brain_decay(
        tr, echo_times, path
    )


if __name__ == "__main__":

    figure_path = pathlib.Path(__file__).parents[2] / "figures"
    figure_path.mkdir(parents=True, exist_ok=True)

    main(
        TR, ECHO_TIMES, figure_path
    )
