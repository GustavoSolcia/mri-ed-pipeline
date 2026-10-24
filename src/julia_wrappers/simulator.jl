using KomaMRI

const BACKEND = get(ENV, "KOMA_BACKEND", "auto")

if BACKEND != "cpu"
    try
        @eval using CUDA
    catch err
        BACKEND == "gpu" && rethrow()
        @warn "CUDA unavailable; using CPU" exception = (err, catch_backtrace())
    end
end

function run_koma(
    scanner_config, sequence_config, phantom_config,
    sequence_path, phantom_path, backend, n_threads
)
    """
    Simulate with KomaMRI given configuration dictionaries.

    # Arguments
    - `scanner_config::Dict`: Scanner configuration dictionary.
    - `sequence_config::Dict`: Sequence configuration dictionary.
    - `phantom_config::Dict`: Phantom configuration dictionary.
    - `sequence_path::String`: Sequence path for loading into the simulator.
    - `backend::String': Simulation backend.
    """

    # Defining the system scanner
    sys = Scanner(
        B0=scanner_config["field"], # Other constants are equal to default
        Gmax=scanner_config["max_grad"] * 1e-3, 
        Smax=scanner_config["max_slew"] * 1e3,
        GR_Δt=scanner_config["grad_raster_time"],
        RF_ring_down_time=scanner_config["rf_ringdown_time"],
        RF_dead_time=scanner_config["rf_dead_time"]
    ) 

    # Reading the phantom
    if phantom_config["type"] == "brain"
        obj = brain_phantom3D()
        obj.Δw .= 0
    else
        obj = read_phantom(phantom_path)
        obj.Δw .+= 2π * phantom_config["off_resonance"]
    end


    # Reading the sequence
    seq = read_seq(sequence_path)

    # Simulator parameters
    sim_params = KomaMRICore.default_sim_params()
    if backend == "cpu"
        sim_params["gpu"] = false
        sim_params["Nthreads"] = n_threads
    else
        try
            @eval Main using CUDA
        catch err
            @warn "CUDA unavailable; using CPU" exception = err
        end
        sim_params["gpu"] = true
    end
    sim_params["sim_method"] = Bloch()
    sim_params["return_type"] = "mat"

    # Starting the simulation
    raw_mat = simulate(obj, seq, sys; sim_params)

    # Sampling times for future plots
    t = get_adc_sampling_times(seq)
    
    simulation_result = Dict(
        "raw" => raw_mat,
        "adc_sampling_times" => t
    )

    return simulation_result
end
