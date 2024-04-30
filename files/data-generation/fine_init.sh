#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=32
# #SBATCH --exclusive
#SBATCH --time=05:00:00
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=<account>

module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20

cd /scratch/space1/x01/data/my-scratch-data/initial/

srun --nodes=1 --ntasks=32 --job-name=bout-hw --distribution=block:block \
    /work/x01/x01/$USER/BOUT-dev/build/examples/hasegawa-wakatani/hasegawa-wakatani \
    nout=4800 -d . >> _log.txt 2>&1
