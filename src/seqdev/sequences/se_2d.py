"""2D Spin Echo sequence."""

import pathlib
from math import pi

import numpy as np
from pypulseq.opts import Opts
from pypulseq.Sequence.sequence import Sequence
from pypulseq.make_sinc_pulse import make_sinc_pulse
from pypulseq.make_adc import make_adc
from pypulseq.calc_duration import calc_duration
from pypulseq.make_delay import make_delay
from pypulseq.make_trapezoid import make_trapezoid

from seqdev.base.base_sequence import BaseSequence
from seqdev.utils.logging import logger


class SpinEcho2D(BaseSequence):
    """Spin echo 2D (SE-2D) sequence class."""

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

        rf_90 = make_sinc_pulse(
            flip_angle=90*pi/180,
            duration=sequence_parameters["rf_dur"],
            apodization=0.5,
            time_bw_product=4,
            return_gz=False,
            system=system
        )

        rf_180 = make_sinc_pulse(
            flip_angle=pi,
            duration=sequence_parameters["rf_dur"],
            apodization=0.5,
            time_bw_product=4,
            return_gz=False,
            system=system
        )

        deltak = 1 / sequence_parameters["fov"]
        dwelltime_us = self._calculate_dwell_time(
                sequence_parameters["adc_dur"],
                sequence_parameters["n_x"],
                1e-6  # Scale in microseconds
        )
        gx_flat_time = dwelltime_us * sequence_parameters["n_x"]
        gx = make_trapezoid(
            channel="x",
            flat_area=sequence_parameters["n_x"]*deltak,
            flat_time=gx_flat_time,
            system=system
        )
        adc = make_adc(
            num_samples=sequence_parameters["n_x"],
            duration=gx.flat_time,
            delay=gx.rise_time
        )

        phase_areas = (
            np.arange(sequence_parameters["n_y"])
            - (sequence_parameters["n_y"] / 2)
        ) * deltak

        gx_pre = make_trapezoid(
            channel="x",
            system=system,
            area=gx.area / 2,
            duration=sequence_parameters["ph_dur"]
        )
        gy_phase_pre = make_trapezoid(
            channel="y",
            system=system,
            area=phase_areas[-1],
            duration=sequence_parameters["ph_dur"]
        )

        te_delay_1 = (
            sequence_parameters["te"] / 2
            - calc_duration(rf_90) / 2
            - calc_duration(gx_pre)
            - calc_duration(rf_180) / 2
        )
        te_delay_1 = self._round_delay(te_delay_1, system.grad_raster_time)

        te_delay_2 = (
            sequence_parameters["te"] / 2
            - calc_duration(rf_180) / 2
            - calc_duration(gx) / 2
        )
        te_delay_2 = self._round_delay(te_delay_2, system.grad_raster_time)

        tr_delay = (
            sequence_parameters["tr"]
            - calc_duration(rf_90)
            - calc_duration(gx_pre)
            - calc_duration(rf_180)
            - calc_duration(gx)
        )
        tr_delay = self._round_delay(tr_delay, system.grad_raster_time)

        for j in range(sequence_parameters["n_y"]):
            gy_phase_pre = make_trapezoid(
                channel="y",
                area=phase_areas[j],
                duration=sequence_parameters["ph_dur"],
                system=system
            )

            seq.add_block(rf_90)
            seq.add_block(gx_pre, gy_phase_pre)
            seq.add_block(make_delay(te_delay_1))
            seq.add_block(rf_180)
            seq.add_block(make_delay(te_delay_2))
            seq.add_block(adc, gx)
            seq.add_block(make_delay(tr_delay))

        [ok, error_report] = seq.check_timing()

        if ok:
            logger.info('Timing check passed successfully')
        else:
            logger.info('Timing check failed! Error listing follows:')
            for error in error_report:
                logger.error(error)

        seq.set_definition(key="Name", value="2d_se")
        seq.write(path / "se_2d.seq")
        logger.info("Sequence saved in the data folder")
