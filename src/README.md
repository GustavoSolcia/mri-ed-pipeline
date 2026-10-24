# Sequence and simulation info 

## Why PyPulseq?

[PyPulseq](https://github.com/imr-framework/pypulseq) is the Python version of
[Pulseq](https://github.com/imr-framework/pypulseq). Pulseq is a opensource 
project for magnetic resonance pulse sequence development with a open file format.
In our project we are going to use the sequences for simulations, but you could
also use the sequences in real scanners from multiple vendors with interpreters.
If you want to know more about this powerfull tool, please check their
 [Paper](https://doi.org/10.1002/mrm.26235) 

## Why KomaMRI?

Over the years, many MRI simulators were developed. [JEMRIS](https://www.jemris.org/)
is one of the most long lasting and widely used open-source software. 
However, JEMRIS lacks GPU support and has a slow learning curve. 
On the other hand, [KomaMRI](https://github.com/JuliaHealth/KomaMRI.jl) uses the 
Julia programming language, which is easy to install/learn, and supports 
both CPU and GPU parallelization. Last but not least, KomaMRI is a great example
of open science project. Please, take a look in the KomaMRI
 [Documentation](https://juliahealth.org/KomaMRI.jl/stable/) and 
[Paper](https://doi.org/10.1002/mrm.29635).

In this project KomaMRI is called from Python with juliacall. The Julia
dependencies are listed in `seqdev/juliapkg.json` and are installed
automatically on the first run, so you don't need to set up Julia by hand.
When running with `--backend gpu`, CUDA is added on the first run.
For AMDGPU support, please read the KomaMRI documentation.

## Writing sequences

We designed this code to facilitate the addition of new sequences to the pipeline.
Under the base/ directory you will be able to find base classes for sequence
and processing. The base sequence class is inherited by the sequences implemented
inside sequences/ directory. Inside sequences/ you will be able to find a pulse
sequence writer with a dictionary that is used as a sequence map.

Now let's suppose you have an idea for an amazing sequence. You have to create 
a file ```amazing_sequence.py```. Inside this file you will import everything
that you need to create you sequence and define the class and rewrite
the write class in the following way:

```
class AmazingSequence(BaseSequence):
    """Amazing sequence class.
    """
    def write(
        self,
        system_parameters: dict,
        sequence_parameters: dict,
        path: pathlib.Path
    ) -> None:
        """Writes an amazing sequence to file.
        
        Here you will write every important info to document
        your sequence and help others in the future.

        Parameters
        ----------
        system_parameters : dict
            Dictionary of system parameters.
        sequence_parameters : dict
            Dictionary of sequence parameters.
        path : pathlib.Path
            Path to save the sequence file.
        """
        system = Opts(
            max_grad=system_parameters["max_grad"], grad_unit="mT/m",
            max_slew=system_parameters["max_slew"], slew_unit="T/m/s",
            grad_raster_time=system_parameters["grad_raster_time"],
            rf_ringdown_time=system_parameters["rf_ringdown_time"],
            rf_dead_time=system_parameters["rf_dead_time"]
        )
        
        # Your code goes here
        ....
```

After writing your sequence, go to the sequence map dictionary inside the 
```pulse_sequence_writer.py``` and add the sequence you just created.

```
sequence_map = {
    "amazing_sequence": AmazingSequence(),
    "fid": FreeInductionDecay(),
    "se_1d": SpinEcho1D(),
    "se_2d": SpinEcho2D(),
    "se_ms": SpinEchoMS(),
    "se_ms_broken": SpinEchoMSB(),
    "gre_2d": GradientEcho2D()
}

```
Then, create an experiment configuration file, e.g.
```experiments/amazing_sequence/amazing_sequence_brain.yml```, with
`sequence.type` matching the key in the sequence map and all the parameters
your sequence needs:

```
scanner:
  field: 3
  max_grad: 32
  max_slew: 130
  grad_raster_time: 10.0e-6
  rf_ringdown_time: 20.0e-6
  rf_dead_time: 100.0e-6

sequence:
  type: amazing_sequence
  # Your sequence parameters go here

phantom:
  type: brain
  off_resonance: 0
```

After these steps you can run your experiment:

```
bash run_experiment.sh -e amazing_sequence -r amazing_sequence_brain
```

## Creating reconstructions

The procedure for creating new reconstructions is similar to what was described in the
sequences section. The main difference is that you will need to rewrite 
the load_signal and process methods to create the reconstruction for you
acquisition. But please, dont forget to add the same key of your desired sequence to the 
processing map.

```
processing_map = {
    "amazing_sequence": AmazingSequenceProcessing(),
    "fid": FreeInductionDecayProcessing(),
    "se_1d": SpinEcho1DProcessing(),
    "se_2d": SpinEcho2DProcessing(),
    "gre_2d": GradientEcho2DProcessing()
}
```
