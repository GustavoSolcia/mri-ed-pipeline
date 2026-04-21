"""Base processing strategy class definition."""

import pathlib
from abc import (
    ABC,
    abstractmethod
)


class BaseProcessing(ABC):
    """Base processing class."""

    @abstractmethod
    def load_signal(self, sequence: str, path: pathlib.Path) -> None:
        """Load signal from file.

        Args:
            sequence (str): Sequence type.
            path (pathlib.Path): Path to the signal file.
        """

        raise NotImplementedError

    @abstractmethod
    def process(
        self,
        parameters: dict,
        phantom: str,
        sequence: str,
        path: pathlib.Path
    ) -> None:
        """Process phantom signal according to sequence type.

        Args:
            parameters (dict): Sequence parameters.
            phantom (str): Phantom name.
            path (pathlib.Path): Parent path from raw data to save processed data.
        """

        raise NotImplementedError
