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
git clone https://github.com/GustavoSolcia/mri-simulation-dev.git
```

If you are not familiar with working on a terminal or git, we 
hightly suggest you to read the 
[Bash Reference Manual](https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html)
and the [Git Documentation](https://git-scm.com/docs/gittutorial).

### Setting up the environment

We recommend you to first install [miniforge](https://github.com/conda-forge/miniforge).
With environments you don't mix your personal python package configuration with our project 
requirements. After installing miniforge or any other package manager you can run the 
following commands:

```
mamba env create -f environment.yml
```

The installation can take a while, but everything will be ready for you to use 
pypulseq with our scripts. You just need to activate the environment first:

```
mamba activate mri_ed
```

To setup Julia dependencies, you can type ```julia``` and enter the package
manager mode by typing ```]```:

```
julia> ]
pkg> add KomaMRI
pkg> add Distributions
pkg> add CUDA
pkg> add MAT
pkg> add YAML
```

After typing ```]``` you will write ```add <package_name>``` and press enter.
This will install all Julia dependencies for our project. The packages KomaMRI
and CUDA will take a while to install.

After setting up the environment, just make sure you edit your local paths
in the config/local/paths.yml file.

### Running the scripts

With the environments and local paths all setup, you can run our experiment scripts
with the 'run_experiment.sh' script and pass the desired sequence and 
phantom as arguments:

```
bash run_experiment.sh --sequence fid --phantom water_spheres
```

It's also possible to run the script in a short way:

```
bash run_experiment.sh -s gre_2d -p brain
```

In case you are developing a new sequence or post processing, it's also
possible to run an individual python script:

```
python3 src/write_sequence -s se_1d
```

Same is valid with 'post_process.py' and 'simulate.jl'. You can always take
a look in the 'run_experiment.sh' file and check how to run these parts of
the pipeline individually.

## Project structure

```
mri-simulation-dev
├── config                  <- Configuration files (e.g. sequences and paths)
├── data                    <- Where data will be saved at the end of the runs
├── environment.yml
├── figures                 <- Where figures will be saved 
├── LICENSE
├── README.md
├── run_experiment.sh       <- Script to run experiments
└── src
    ├── base                <- Base classes (sequence and post-processing)
    ├── data_load           <- Data load code
    ├── phantom             <- Julia script to create phantom
    ├── plotting            <- Plotting code
    ├── post_process.py     <- Post-processing script
    ├── README.md
    ├── reconstruction      <- Reconstruction code
    ├── sequences           <- Sequences classes
    ├── simulate.jl         <- Simulation script
    ├── utils               <- Utilitary code
    └── write_sequence.py   <- Sequence writting script
```
