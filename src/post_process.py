"""Post-processing according to sequence type."""

import pathlib

import matplotlib.pyplot as plt
import numpy as np

from seqdev.reconstruction.data_processor import DataProcessor
from seqdev.utils.cli import parse_sequence
from seqdev.utils.config import load_config


if __name__ == "__main__":
    args = parse_sequence()

    SEQUENCE = args["sequence"]
    PHANTOM = args["phantom"]

    SCRIPT_PATH = script_path = pathlib.Path(__file__).resolve()
    PARENT_DIR = script_path.parents[1]
    BASE_CONFIG_PATH = PARENT_DIR / "config"
    DATA_PATH = PARENT_DIR / "data"

    scanner_config = load_config(BASE_CONFIG_PATH / "scanner.yml")
    sequence_config = load_config(BASE_CONFIG_PATH / f"{SEQUENCE}.yml")

    processor = DataProcessor(SEQUENCE)
    processor.process_signal(sequence_config, PHANTOM, SEQUENCE, DATA_PATH)
