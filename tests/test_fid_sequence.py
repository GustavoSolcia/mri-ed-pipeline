"""Tests for Free Induction Decay (FID) sequence."""

import os
import unittest
from pathlib import Path

from constants import (
    FID_SEQUENCE_PARAMETERS,
    SYSTEM_PARAMETERS
)
from seqdev.sequences.fid import FreeInductionDecay


class TestFreeInductionDecay(unittest.TestCase):
    """Test suite for FID."""

    def setUp(self):
        """Set up path and parameters for testing the sequence."""

        # Sequence will be created and deleted in the project path
        self.current_path = Path.cwd()
        self.test_filename = self.current_path / "fid.seq"

        self.system_parameters = SYSTEM_PARAMETERS
        self.sequence_parameters = FID_SEQUENCE_PARAMETERS

        # Making sure the sequence does not exist before testing
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self):
        """Removing the sequence file after the test is finished."""

        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_write(self):
        """Test if sequence is writting properly."""

        sequence = FreeInductionDecay()
        sequence.write(
            self.system_parameters, self.sequence_parameters, self.current_path
        )
        self.assertTrue(os.path.exists(self.test_filename))


if __name__ == "__main__":
    unittest.main()
