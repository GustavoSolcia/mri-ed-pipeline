"""1D Spin Echo (1D-SE) sequence."""

import pathlib
from math import (
    pi,
    floor
)

from pypulseq.opts import Opts
from pypulseq.Sequence.sequence import Sequence
from pypulseq.make_block_pulse import make_block_pulse
from pypulseq.make_adc import make_adc
from pypulseq.calc_duration import calc_duration
from pypulseq.make_delay import make_delay

from seqdev.base.base_sequence import BaseSequence
from seqdev.utils.logging import logger


class SpinEcho1D(BaseSequence):
    """Spin echo 1D (SE-1D) sequence class."""

    def write(
        self,
        system_parameters: dict,
        sequence_parameters: dict,
        path: pathlib.Path
    ) -> None:
        """Writes sequence to file.

        Note:
            System parameters are defined in the `system_parameters` dictionary.
                - max_grad: Maximum gradient amplitude (mT/m).
                - max_slew: Maximum slew rate (T/m/s).
                - grad_raster_time: Gradient raster time (s).
                - rf_ringdown_time: RF ring-down time (s).
                - rf_dead_time: RF dead time (s).
            Sequence parameters are defined in the `sequence_parameters` dictionary.
                - rf_dur: Duration of the 90-degree RF pulse (s).
                - adc_duration: ADC duration (s).

        Args:
            system_parameters (dict): Dictionary of system parameters.
            sequence_parameters (dict): Dictionary of sequence parameters.
            path (pathlib.Path): Path to save the sequence file.
        """

        system = Opts(
            max_grad=system_parameters["max_grad"], grad_unit="mT/m",
            max_slew=system_parameters["max_slew"], slew_unit="T/m/s",
            grad_raster_time=system_parameters["grad_raster_time"],
            rf_ringdown_time=system_parameters["rf_ringdown_time"],
            rf_dead_time=system_parameters["rf_dead_time"]
        )
        seq = Sequence(system)

        rf_90 = make_block_pulse(
            pi/2,
            duration=sequence_parameters["rf_dur"],
            system=system
        )
        rf_180 = make_block_pulse(
            pi,
            duration=sequence_parameters["rf_dur"],
            use='refocusing',
            system=system
        )

        # Time from the start of each RF block to the pulse centre, and from the
        # pulse centre to the end of the block
        rf90_tail = calc_duration(rf_90) - (rf_90.delay + rf_90.shape_dur / 2)
        rf180_center = rf_180.delay + rf_180.shape_dur / 2
        rf180_tail = calc_duration(rf_180) - rf180_center

        # 90 centre -> first 180 centre = TE/2; consecutive 180 centres = TE
        half_gap = self._round_delay(
            sequence_parameters["te"] / 2 - rf90_tail - rf180_center,
            system.grad_raster_time
        )
        echo_gap = self._round_delay(
            sequence_parameters["te"] - rf180_tail - rf180_center,
            system.grad_raster_time
        )
        if half_gap <= 0:
            raise ValueError("TE is too short for the RF pulses.")

        # Fill each gap with a readout: n_samples per echo window, and the same
        # dwell time for the FID window after the 90
        dead_time = system.adc_dead_time
        dwelltime = 1e-6 * floor(
            (echo_gap - 2 * dead_time) / sequence_parameters["n_samples"] / 1e-6
        )
        adc_echo = make_adc(
            num_samples=sequence_parameters["n_samples"],
            dwell=dwelltime,
            system=system
        )
        adc_fid = make_adc(
            num_samples=floor((half_gap - 2 * dead_time) / dwelltime),
            dwell=dwelltime,
            system=system
        )

        tr_delay = self._round_delay(
            sequence_parameters["tr"]
            - calc_duration(rf_90)
            - half_gap
            - sequence_parameters["n_echo"] * (calc_duration(rf_180) + echo_gap),
            system.grad_raster_time
        )
        if tr_delay < 0:
            raise ValueError("TR is too short for the echo train.")

        logger.info("Starting to build 1D SE sequence")
        for rep in range(sequence_parameters["n_rep"]):
            seq.add_block(rf_90)
            seq.add_block(make_delay(half_gap), adc_fid)       # FID, T2* decay
            for echo in range(sequence_parameters["n_echo"]):
                seq.add_block(rf_180)
                seq.add_block(make_delay(echo_gap), adc_echo)  # echo centred in window
            seq.add_block(make_delay(tr_delay))

        [ok, error_report] = seq.check_timing()

        if ok:
            logger.info('Timing check passed successfully')
        else:
            logger.info('Timing check failed! Error listing follows:')
            for error in error_report:
                logger.error(error)

        seq.set_definition(key="Name", value="1d_se")
        seq.write(path / "se_1d.seq")
        print("Sequence saved in the data folder")
