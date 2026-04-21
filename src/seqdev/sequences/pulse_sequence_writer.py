"""This code contains the PulseSequenceWriter class.

Note: If you want to add a new pulse sequence, make sure to add it to the
'sequence_map'.
"""

import pathlib

from seqdev.sequences.fid import FreeInductionDecay
from seqdev.sequences.gre_2d import GradientEcho2D
from seqdev.sequences.se_1d import SpinEcho1D
from seqdev.sequences.se_2d import SpinEcho2D

# Map of sequence names to their corresponding classes.
# If you add a new sequence, simply add an entry to this
# map with the sequence name as the key and the class as the value.
sequence_map = {
    "fid": FreeInductionDecay(),
    "se_1d": SpinEcho1D(),
    "se_2d": SpinEcho2D(),
    "gre_2d": GradientEcho2D()
}


class PulseSequenceWriter:
    """Pulse sequence writer class

    Args:
        sequence_name (str): Name of the pulse sequence to be written.
    """

    def __init__(self, sequence_name: str):
        if sequence_name not in sequence_map:
            raise ValueError(f"Invalid sequence name: {sequence_name}")
        self.sequence_name = sequence_name
        self.sequence = sequence_map[self.sequence_name]

    def write_sequence(
        self,
        system_parameters: dict,
        sequence_parameters: dict,
        path: pathlib.Path
    ) -> None:
        """Writes the pulse sequence to a file.

        Args:
            system_parameters (dict): Dictionary of system parameters.
            sequence_parameters (dict): Dictionary of parameters for the pulse
                sequence.
            path (pathlib.Path): Path to the sequence.
        """
        self.sequence.write(system_parameters, sequence_parameters, path)
