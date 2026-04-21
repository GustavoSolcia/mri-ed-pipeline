"""Tests for 2D Gradient Echo (2D-GRE) sequence."""

import os
import unittest
from pathlib import Path

from constants import (
    GRE_2D_SEQUENCE_PARAMETERS,
    SYSTEM_PARAMETERS
)
from seqdev.sequences.gre_2d import GradientEcho2D


class TestGradientEcho2D(unittest.TestCase):
    """Test suite for 2D-GRE."""

    def setUp(self):
        """Set up path and parameters for testing the sequence."""

        # Sequence will be created and deleted in the project path
        self.current_path = Path.cwd()
        self.test_filename = self.current_path / "gre_2d.seq"

        self.system_parameters = SYSTEM_PARAMETERS
        self.sequence_parameters = GRE_2D_SEQUENCE_PARAMETERS

        # Making sure the sequence does not exist before testing
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self):
        """Removing the sequence file after the test is finished."""

        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_write(self):
        """Test if sequence is writting properly."""

        sequence = GradientEcho2D()
        sequence.write(
            self.system_parameters, self.sequence_parameters, self.current_path
        )
        self.assertTrue(os.path.exists(self.test_filename))


if __name__ == "__main__":
    unittest.main()
