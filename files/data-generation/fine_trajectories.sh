#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=32
# #SBATCH --exclusive
#SBATCH --time=08:00:00
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=<account>

module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20


for TRAJ_INDEX in {1..10}
do

  TRAJ_INDEX_BEFORE="$((TRAJ_INDEX-1))"

  mkdir /scratch/space1/x01/data/my-scratch-data/${TRAJ_INDEX}
  cd /scratch/space1/x01/data/my-scratch-data/${TRAJ_INDEX}

  cp /scratch/space1/x01/data/my-scratch-data/${TRAJ_INDEX_BEFORE}/BOUT.restart.* .
  cp /scratch/space1/x01/data/my-scratch-data/${TRAJ_INDEX_BEFORE}/BOUT.inp .

  srun --nodes=1 --ntasks=32 --job-name=bout-hw --distribution=block:block \
      /work/x01/x01/$USER/my-hw/build/hasegawa-wakatani \
      solver:type=rk4 solver:adaptive=false solver:timestep=0.008 \
      nout=1000 restart=true append=false -d . >> _log.txt 2>&1

done
