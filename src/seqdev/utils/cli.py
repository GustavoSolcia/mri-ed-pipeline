"""Argument parse functions."""

import argparse
import pathlib


def parse_experiment() -> dict[str]:
    """Argument parser for experiment script.

    Args:
        args (dict[str, pathlib.Path]): Arguments dictionary containing
            sequence type.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-e",
        "--experiment",
        type=str,
        help="Experiment type."
    )
    parser.add_argument(
        "-r",
        "--run",
        type=str,
        help="Target run."
    )
    parser.add_argument(
        "-b",
        "--backend",
        type=str,
        help="Simulation backend"
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        help="Number of threads to run simulation on"
    )

    args = vars(parser.parse_args())
    return args
