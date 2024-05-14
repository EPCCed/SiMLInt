#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=02:00:00
#SBATCH --partition=standard
#SBATCH --qos=standard

module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20

export WORK=${HOME/home/work}
mkdir -p $WORK/data/0
cp ${WORK}/SiMLInt/files/1-data-generation/BOUT.inp ${WORK}/data/0
cd ${WORK}/data/0

srun --nodes=1 --ntasks=32 --job-name=bout-hw --distribution=block:block \
    ${WORK}/my-hw/build/hasegawa-wakatani \
    nout=4800 -d . >> _log.txt 2>&1