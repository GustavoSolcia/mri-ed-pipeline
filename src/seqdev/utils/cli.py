"""Argument parse functions."""

import argparse
import pathlib


def parse_sequence() -> dict[str]:
    """Argument parser for sequence writing function.

    Args:
        args (dict[str, pathlib.Path]): Arguments dictionary containing
            sequence type.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sequence",
        type=str,
        help="Desired sequence."
    )
    parser.add_argument(
        "-p",
        "--phantom",
        type=str,
        help="Desired phantom."
    )

    args = vars(parser.parse_args())
    return args
