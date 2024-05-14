#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --time=08:00:00
#SBATCH --partition=standard
#SBATCH --qos=standard

module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20

export WORK=${HOME/home/work}

for TRAJ_INDEX in {1..10}
do

  TRAJ_INDEX_BEFORE="$((TRAJ_INDEX-1))"

  mkdir -p $WORK/data/${TRAJ_INDEX}
  cd $WORK/data/${TRAJ_INDEX}

  cp ${WORK}/data/${TRAJ_INDEX_BEFORE}/BOUT.restart.* .
  cp ${WORK}/data/${TRAJ_INDEX_BEFORE}/BOUT.inp .

  srun --nodes=1 --ntasks=32 --job-name=bout-hw --distribution=block:block \
      $WORK/my-hw/build/hasegawa-wakatani \
      solver:type=rk4 solver:adaptive=false solver:timestep=0.008 \
      nout=1000 restart=true append=false -d . >> _log.txt 2>&1

done
