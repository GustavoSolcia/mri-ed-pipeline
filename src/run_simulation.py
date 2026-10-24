"""Simulation orchestration script."""

import os
import pathlib
from typing import Any

import numpy as np
import juliapkg
from juliacall import Main as jl
from scipy.io import savemat

from seqdev.reconstruction.data_processor import DataProcessor
from seqdev.sequences.pulse_sequence_writer import PulseSequenceWriter
from seqdev.utils.cli import parse_experiment
from seqdev.utils.config import load_config
from seqdev.utils.logging import logger

CUDA_UUID = "052768ef-5323-5732-b1bb-66c8b64840ba"


def main(
    config: dict[str, Any],
    results_path: pathlib.Path,
    phantom_path: pathlib.Path,
    backend: str,
    n_threads: int
) -> None:
    """Sequence writting, phantom creation, simulation, and post-processing.

    Args:
        config: Experiment configuration dictionary.
        results_path: Experiment results path.
        phantom_path: Phantom location path.
        backend: Backend to run simulation.
        n_threads: Number of threads to run simulation.
    """

    sequence_path = results_path / "sequence"
    sequence_path.mkdir(parents=True, exist_ok=True)
    
    figures_path = results_path / "figures"
    figures_path.mkdir(parents=True, exist_ok=True)

    writer = PulseSequenceWriter(config["sequence"]["type"])
    writer.write_sequence(config["scanner"], config["sequence"], sequence_path)

    script_path = pathlib.Path(__file__).parents[0]
    simulator_path = script_path / "julia_wrappers" / "simulator.jl"
    phantom_creator_path = script_path / "julia_wrappers" / "water_spheres.jl"
    phantom_file = ""

    jl.include(str(phantom_creator_path))
    if config["phantom"]["type"] != "brain":
        phantom_file = phantom_path / f"{config['phantom']['type']}.phantom"
        if not phantom_file.exists():
            phantom_path.mkdir(parents=True, exist_ok=True)
            jl.make_water_spheres(str(phantom_file))

    # Resolving CUDA backend mainly for first GPU runs.
    if backend == "gpu":
        try:
            # It will install the CUDA package on first run
            juliapkg.add("CUDA", CUDA_UUID, version="5, 6")
            juliapkg.resolve()
        except:
            logger.warning("Failed to add CUDA")

    os.environ["KOMA_BACKEND"] = backend

    # Loading the KomaMRI wrapper and calling the function responsible
    # to simulate with our experiment parameters
    jl.include(str(simulator_path))
    result = jl.run_koma(
        config["scanner"], config["sequence"], config["phantom"],
        str(sequence_path / f"{config['sequence']['type']}.seq"),
        str(phantom_file), backend, n_threads
    )

    simulation_path = results_path / "simulation"
    simulation_path.mkdir(parents=True, exist_ok=True)
    savemat(simulation_path / f"{config['sequence']['type']}.mat", result)

    processor = DataProcessor(config["sequence"]["type"])
    processor.process_signal(
        config["sequence"], config["phantom"]["type"], config["sequence"]["type"],
        results_path
    )

if __name__ == "__main__":

    args = parse_experiment()

    project_path = pathlib.Path(__file__).parents[1]

    experiment_config = load_config(
        project_path / "experiments" / args["experiment"] / f"{args['run']}.yml" 
    )

    experiment_results_path = project_path / "results" / args['experiment'] / args['run']
    experiment_results_path.mkdir(parents=True, exist_ok=True)

    experiment_phantom_path = project_path / "data" / "phantom"

    main(
        experiment_config, experiment_results_path, experiment_phantom_path,
        args["backend"], args["threads"]
    )
