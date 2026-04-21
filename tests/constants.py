
SYSTEM_PARAMETERS = {
    "field": 3,
    "max_grad": 32,
    "max_slew": 130,
    "grad_raster_time": 10.0e-6,
    "rf_ringdown_time": 20.0e-6,
    "rf_dead_time": 100.0e-6
}

FID_SEQUENCE_PARAMETERS = { 
    "n_rep": 1,
    "n_samples": 1024,
    "adc_dur": 200.0e-3,
    "rf_dur": 500.0e-6,
    "tr": 12,
    "t": 10.0e-3
}

SE_1D_SEQUENCE_PARAMETERS = {
    "n_rep": 1,
    "n_echo": 10,
    "n_samples": 1024,
    "adc_dur": 200.0e-3,
    "rf_dur": 50.0e-6,
    "tr": 12,
    "te": 10.0e-3
}

SE_2D_SEQUENCE_PARAMETERS = {
    "n_x": 128,
    "n_y": 128,
    "fov": 256.0e-3,
    "adc_dur": 5.12e-3,
    "rf_dur": 1.0e-3,
    "rf_offset": 0.0,
    "ph_dur": 440.0e-6,
    "tr": 6000.0e-3,
    "te": 200.0e-3
}

GRE_2D_SEQUENCE_PARAMETERS = {
    "n_x": 128,
    "n_y": 128,
    "n_slices": 3,
    "fov": 256.0e-3,
    "slice_thickness": 5.0e-3,
    "adc_dur": 5.12e-3,
    "rf_dur": 1.0e-3,
    "ph_dur": 440.0e-6,
    "flip_angle": 10,
    "tr": 6000.0e-3,
    "te": 200.0e-3
}
