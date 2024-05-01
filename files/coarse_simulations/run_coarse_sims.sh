#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
# #SBATCH --exclusive
#SBATCH --time=08:00:00
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --account=<account>

eval "$(/work/x01/x01/$USER/miniconda3/bin/conda shell.bash hook)"
conda activate boutsmartsim

module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20

ID_TRAJ=1
BASE_PATH=/scratch/space1/x01/data/my-scratch-data

executable=/work/x01/x01/$USER/my-hw/build/hasegawa-wakatani

for i in {0..1000}
do
  coarse_TRAJ_PATH=${BASE_PATH}/${i}/coarse
  coarse_TRAJ_SIM_PATH=${BASE_PATH}/${i}/coarse_sim
  mkdir -p $coarse_TRAJ_SIM_PATH
  cp ${coarse_TRAJ_PATH}/BOUT.restart.* $coarse_TRAJ_SIM_PATH
  cp coarse_BOUT.inp $coarse_TRAJ_SIM_PATH/BOUT.inp

  cd $coarse_TRAJ_SIM_PATH

  srun --nodes=1 --ntasks=1 --job-name=ss_job_0 --distribution=block:block \
    $executable -d . \
    restart=true append=false \
    solver:type=rk4 solver:adaptive=false solver:timestep=0.026 \
    nout=1 timestep=0.026 mesh:nx=260 mesh:nz=256 mesh:dx=0.1 mesh:dz=0.1 -d .
done
