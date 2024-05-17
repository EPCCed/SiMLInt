#!/bin/bash

# Activate the Conda environment
_CONDA_DEFAULT_ENV="${CONDA_DEFAULT_ENV:-boutsmartsim}"

__conda_setup="$('/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
eval "$__conda_setup"
unset __conda_setup

# Restore our "indended" default env
conda activate "${_CONDA_DEFAULT_ENV}"

export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export PATH=/simlint-bin:$PATH

echo $@
