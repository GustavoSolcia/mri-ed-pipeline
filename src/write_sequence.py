"""Write sequence according to given arguments."""

import pathlib

from seqdev.sequences.pulse_sequence_writer import PulseSequenceWriter
from seqdev.utils.cli import parse_sequence
from seqdev.utils.config import load_config

if __name__ == "__main__":
    args = parse_sequence()

    SEQUENCE = args["sequence"]

    SCRIPT_PATH = script_path = pathlib.Path(__file__).resolve()
    PARENT_DIR = script_path.parents[1]
    BASE_CONFIG_PATH = PARENT_DIR / "config"
    DATA_PATH = PARENT_DIR / "data"

    scanner_config = load_config(BASE_CONFIG_PATH / "scanner.yml")
    sequence_config = load_config(BASE_CONFIG_PATH / f"{SEQUENCE}.yml")

    sequence_path = DATA_PATH / "sequence"
    # Making sure the data and sequence paths exists
    sequence_path.mkdir(parents=True, exist_ok=True)

    writer = PulseSequenceWriter(SEQUENCE)
    writer.write_sequence(scanner_config, sequence_config, sequence_path)
