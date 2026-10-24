"""2D Gradient Echo sequence."""

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


class GradientEcho2D(BaseSequence):
    """Gradient echo 2D (GRE-2D) sequence class."""

    def write(
        self,
        system_parameters: dict,
        sequence_parameters: dict,
        path: pathlib.Path
    ) -> None:
        """Writes GRE-2D sequence to file.

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

        rf, gz, gz_reph = make_sinc_pulse(
            flip_angle=sequence_parameters["flip_angle"]*pi/180,
            duration=sequence_parameters["rf_dur"],
            slice_thickness=sequence_parameters["slice_thickness"],
            apodization=0.5,
            time_bw_product=4,
            return_gz=True,
            use="excitation",
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
        gy_phase = make_trapezoid(
            channel="y",
            system=system,
            area=phase_areas[0],
            duration=sequence_parameters["ph_dur"]
        )

        gx_pre = make_trapezoid(
            channel="x",
            system=system,
            area=-gx.area / 2,
            duration=sequence_parameters["ph_dur"]
        )

        te_delay = (
            sequence_parameters["te"]
            - calc_duration(gz) / 2
            - calc_duration(gz_reph)
            - calc_duration(gy_phase)
            - calc_duration(gx_pre)
            - calc_duration(gx) / 2
        )
        te_delay = self._round_delay(te_delay, system.grad_raster_time)

        tr_delay = (
            sequence_parameters["tr"]
            - calc_duration(gz)
            - calc_duration(gz_reph)
            - calc_duration(gy_phase)
            - te_delay
            - calc_duration(gx_pre)
            - calc_duration(gx)
        )
        tr_delay = self._round_delay(tr_delay, system.grad_raster_time)

        for k in range(sequence_parameters["n_slices"]):
            rf.freq_offset = (
                gz.amplitude
                * sequence_parameters["slice_thickness"]
                * (k - (sequence_parameters["n_slices"] - 1) / 2)
            )

            for j in range(sequence_parameters["n_y"]):
                gy_phase = make_trapezoid(
                    channel="y",
                    system=system,
                    area=phase_areas[j],
                    duration=sequence_parameters["ph_dur"]
                )

                seq.add_block(rf, gz)
                seq.add_block(gz_reph)
                seq.add_block(gy_phase)
                seq.add_block(make_delay(te_delay))
                seq.add_block(gx_pre)
                seq.add_block(gx, adc)
                seq.add_block(make_delay(tr_delay))

        [ok, error_report] = seq.check_timing()

        if ok:
            logger.info('Timing check passed successfully')
        else:
            logger.info('Timing check failed! Error listing follows:')
            for error in error_report:
                logger.error(error)
        seq.set_definition(key="Name", value="2d_gre")
        seq.write(path / "gre_2d.seq")
        logger.info("Sequence saved in the data folder")
