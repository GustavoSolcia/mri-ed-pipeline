"""Base sequence strategy class definition."""

import pathlib
from abc import (
    ABC,
    abstractmethod
)


class BaseSequence(ABC):
    """Base sequence class."""

    @abstractmethod
    def write(
        self,
        system_parameters: dict,
        sequence_parameters: dict,
        path: pathlib.Path
    ) -> None:
        """Writes sequence to file.

        Args:
            system_parameters (dict): Parameters for the system.
            sequence_parameters (dict): Parameters for the sequence.
            path (pathlib.Path): Path to the output file.
        """

        raise NotImplementedError

    def _calculate_dwell_time(
        self,
        adc_dur: float,
        n: int,
        scale: float
    ) -> float:
        """Calculates dwell time from sequence parameters.

        Args:
            adc_dur (float): ADC duration from sequence parameters.
            n (int): Number of points in the readout.
            scale (float): Time scale for rounding (e.g. 1e-6 for microseconds).

        Returns:
            dwelltime (float): Rounded dwelltime in given time scale.
        """

        dwelltime = scale * round(int((adc_dur / n) / scale), 5)
        return dwelltime

    def _round_delay(self, delay: float, grad_raster_time: float) -> float:
        """Round delay value according to gradient raster time.

        Args:
            delay (float): Sequence time delay.
            grad_raster_time (float): System gradient raster time.

        Returns:
        delay_round (float): Rounded delay value according to gradient raster time.
        """

        delay_round = round(delay / grad_raster_time) * grad_raster_time
        return delay_round
