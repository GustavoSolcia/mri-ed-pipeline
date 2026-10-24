# PyPulseq and KomaMRI pipeline for MRI education

This project covers the basics of MRI using a current open source
MRI simulation framework. We are trying to make this repository as open and 
friendly as possible. The pipeline will consist on doing sequence development 
with pypulseq and simulating the MRI signal with KomaMRI. Then, you should 
expect to find both Julia and Python languages, but you should not feel 
overwhelmed by it. Everything will be available as an environment with 
install instructions. For advanced implementation instructions, please
read the README file inside src/.

**The content of this project is written mainly for education purposes.**

## Getting started

### Cloning the repository

To clone the repository you can run the following command 
line in your terminal:

```
git clone https://github.com/GustavoSolcia/mri-ed-pipeline.git
```

If you are not familiar with working on a terminal or git, we 
hightly suggest you to read the 
[Bash Reference Manual](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html)
and the [Git Documentation](https://git-scm.com/docs/gittutorial).

### Setting up the environment

We recommend you to first install
[micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html).
With environments you don't mix your personal python package configuration with our project 
requirements. After installing miniforge or any other package manager you can run the 
following commands:

```
micromamba env create -f environment.yml
```

The installation can take a while, but everything will be ready for you to use 
pypulseq with our scripts.
You just need to activate the environment first:

```
micromamba activate mri_ed
```
You don't need to install Julia by yourself. We call KomaMRI from Python
with [juliacall](https://github.com/JuliaPy/PythonCall.jl), and on the
first run it will download Julia and the packages listed in `src/seqdev/juliapkg.json`.
The first run will take a while because of this installation.
If you run the simulation on a GPU, the CUDA package will also be installed on the
first GPU run.


### Running the scripts

Every simulation is described by an experiment configuration file located at
`experiments/<experiment>/<run>.yml`. Each file has three blocks: `scanner`
(system limits), `sequence` (sequence type and parameters) and `phantom`
(`brain` or `water_spheres`). You run an experiment with the
'run_experiment.sh' script by passing the experiment folder and the run name:

```
bash run_experiment.sh --experiment fid --run fid_signal
```

It's also possible to run the script in a short way and choose the simulation
backend (`cpu` or `gpu`, default `cpu`) and the number of threads (default is
the number of available cores):

```
bash run_experiment.sh -e gre_2d -r gre_2d_brain -b gpu -t 8
```

Results are saved in `results/<experiment>/<run>/`

The water spheres phantom is created on the first run and cached in
`data/phantom/`.

## Project structure

```
mri-ed-pipeline
├── data
│   └── phantom             <- Cached phantom files
├── environment.yml
├── experiments             <- Experiment configuration files (<experiment>/<run>.yml)
├── figures                 <- Where standalone figures will be saved
├── LICENSE
├── paper                   <- Manuscript files
├── presentation
├── pyproject.toml          <- seqdev package definition
├── README.md
├── requirements.txt
├── results                 <- Where results will be saved (<experiment>/<run>/)
├── run_experiment.sh       <- Script to run experiments
├── src
│   ├── README.md
│   ├── julia_wrappers      <- Julia code for KomaMRI simulation and phantom creation
│   ├── run_simulation.py   <- Sequence, simulation, and post-processing script
│   └── seqdev              <- Sequence development package
│       ├── base                <- Base classes (sequence and post-processing)
│       ├── data_load           <- Data load code
│       ├── plotting            <- Plotting code
│       ├── reconstruction      <- Reconstruction code
│       ├── sequences           <- Sequences classes
│       ├── utils               <- Utilitary code (CLI, config, logging, NIfTI)
│       └── juliapkg.json       <- Julia dependencies
└── tests                   <- Tests for implemented sequences
```
