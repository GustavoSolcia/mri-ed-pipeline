"""This code contains the DataProcessor class.

Note: If you want to add a new post processing for your new/old sequence,
make shure to add it to the 'processing_map'.
"""

import pathlib

from seqdev.reconstruction.fid_processing import FreeInductionDecayProcessing
from seqdev.reconstruction.se_1d_processing import SpinEcho1DProcessing
from seqdev.reconstruction.se_2d_processing import SpinEcho2DProcessing
from seqdev.reconstruction.gre_2d_processing import GradientEcho2DProcessing


processing_map = {
    "fid": FreeInductionDecayProcessing(),
    "se_1d": SpinEcho1DProcessing(),
    "se_2d": SpinEcho2DProcessing(),
    "gre_2d": GradientEcho2DProcessing()
}


class DataProcessor:
    """Data processing class.

    It process the data according to the sequence utilized and
    saves with given phantom name.

    Args:
        sequence_name (str): Name of the pulse sequence from raw signal.
    """

    def __init__(self, sequence_name: str):
        if sequence_name not in processing_map:
            raise ValueError(f"Invalid sequence name: {sequence_name}")
        self.sequence_name = sequence_name
        self.processing = processing_map[self.sequence_name]

    def process_signal(
            self,
            sequence_parameters: dict,
            phantom_name: str,
            sequence_name: str,
            data_path: pathlib.Path
    ) -> None:
        """Process signal according to the sequence parameters.

        Args:
            sequence_parameters (dict): Sequence parameters for the specific
                sequence.
            phantom_name (str): Name of the phantom used in the experiment.
            sequence_name (str): Name of the sequence used in the experiment.
            data_path (pathlib.Path): Parent path where the raw data is stored
                and processed data will be saved.
     """

        self.processing.load_signal(self.sequence_name, data_path)
        self.processing.process(sequence_parameters, phantom_name, sequence_name, data_path)
