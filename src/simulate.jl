using CUDA
using MAT
using KomaMRI
import YAML

scanner_config = YAML.load_file("config/scanner.yml")

phantom_path = ARGS[1]
seq_path = ARGS[2]
data_path = ARGS[3]

seq_type = ARGS[4]
phantom_type = ARGS[5]

seq_config = YAML.load_file("config/$(seq_type).yml")

# Defining the system scanner
sys = Scanner(
    B0=scanner_config["field"], # Other constants are equal to default
    Gmax=scanner_config["max_grad"] * 1e-3, 
    Smax=scanner_config["max_slew"] * 1e3,
    GR_Δt=scanner_config["grad_raster_time"],
    RF_ring_down_T=scanner_config["rf_ringdown_time"],
    RF_dead_time_T=scanner_config["rf_dead_time"]
) 

# Reading the phantom
if phantom_type == "brain"
    obj = brain_phantom3D()
    obj.Δw .= 0
else
    obj = read_phantom(phantom_path)
end

# Reading the sequence
seq = read_seq(seq_path)

# Simulator parameters
sim_params = KomaMRICore.default_sim_params()
if (seq_type == "fid" || seq_type == "se_1d")
    sim_params["gpu"] = false
    sim_params["Nthreads"] = 4
else
    sim_params["gpu"] = true
end
sim_params["sim_method"] = Bloch()
sim_params["return_type"] = "mat"

# Starting the simulation
raw_mat = simulate(obj, seq, sys; sim_params)

# Sampling times for future plots
t = get_adc_sampling_times(seq)

# Writing output file
mat_file = matopen(data_path, "w")
write(mat_file, "raw", raw_mat)
write(mat_file, "adc_sampling_times", t)
close(mat_file)
