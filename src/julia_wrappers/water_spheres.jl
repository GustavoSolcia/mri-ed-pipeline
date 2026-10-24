using KomaMRI
using Distributions

function make_water_spheres(phantom_file)
    """
    Generates water spheres phantom with KomaMRI.

    # Arguments
    - `phantom_file::String`: Phantom file save location.
    """
    N_mesh = 20 # Minimum mesh size
    radius = 2.5*1e-2 # Spheres radius
    x1 = -2.5*1e-2
    x2 = 2.5*1e-2
    z1 = -2.5*1e-2
    z2 = 2.5*1e-2

    water_T1 = 4 # Relaxation in seconds
    water_T2 = 2
    inom_freq = 50 # rad/s
    water_T2_star = 1 /((1 /water_T2) + inom_freq)

    # Mesh bounding box
    x_lim = collect(range(-5*1e-2, 5*1e-2, length=2*N_mesh))
    y_lim = collect(range(-2.5*1e-2, 2.5*1e-2, length=N_mesh))
    z_lim = collect(range(-5*1e-2, 5*1e-2, length=2*N_mesh))

    N_iso = 100 # Number of isochromats
    omega_0 = 0 
    off_resonance_dist = Truncated(Cauchy(omega_0, inom_freq),omega_0-1000, omega_0+1000)
    ones_iso = ones(N_iso)
    
    obj = nothing
    first_spin_identifier = true # Just to start the phantom object inside the loop 
    position_counter = 0
    for z in z_lim # Iterate over the mesh limits
        for y in y_lim
            for x in x_lim 
                # Spheres radius condition
                if ((x-x1)^2+y^2+(z-z1)^2<= radius^2) || ((x-x2)^2+y^2+(z-z2)^2 <= radius^2)
                    # New off resonance distribution samples for each new position
                    off_resonance_samples = rand(off_resonance_dist, N_iso)
                    if first_spin_identifier
                        obj = Phantom{Float64}(
                            x = x .* ones_iso,
                            y = y .* ones_iso,
                            z = z .* ones_iso,
                            ρ = 1. .* ones_iso,
                            T1 = water_T1 .* ones_iso,
                            T2 = water_T2 .* ones_iso,
                            Δw = off_resonance_samples
                        )
                        first_spin_identifier = false
                        position_counter += 1
                    else
                        obj_tmp = Phantom{Float64}(
                            x = x .* ones_iso,
                            y = y .* ones_iso,
                            z = z .* ones_iso,
                            ρ = 1. .* ones_iso,
                            T1 = water_T1 .* ones_iso,
                            T2 = water_T2 .* ones_iso,
                            Δw = off_resonance_samples
                        )
                        obj += obj_tmp
                        position_counter += 1
                    end
                end
            end
        end
    end

    # Normalizing the proton density
    obj.ρ .= 1.0 / (position_counter * N_iso)

    # Saving the phantom
    write_phantom(obj, phantom_file)
end
