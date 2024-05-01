#!/bin/bash

#SBATCH --job-name=boutsmartsim
#SBATCH --time=0:20:00
#SBATCH --nodes=1
#SBATCH --tasks-per-node=4
#SBATCH --cpus-per-task=1

#SBATCH --account=x01
#SBATCH --partition=standard
#SBATCH --qos=standard

# Setup the job environment
module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20

# Set the number of threads to 1
#   This prevents any threaded system libraries from automatically
#   using threading.
export OMP_NUM_THREADS=1

# activate conda environment for SmartSim and SmartRedis Python packages
conda activate boutsmartsim

cd /path/to/run/

# Start the orchestrator and a new experiment which launches RedisAI for communication
# Load the vorticity and density models from their files
model_vort=/scratch/space1/d175/amy/full_stack/data-model/cnn/model-hw-20240427-164026-vort.pb
model_n=/scratch/space1/d175/amy/full_stack/data-model/cnn/model-hw-20240427-210530-dens.pb
python start_db.py 6899 $model_vort $model_n
echo "Started Redis"

export SSDB=127.0.0.1:6899
executable=/path/to/build/hasegawa-wakatani

# Run the simulation
srun -n 1 --distribution=block:block --hint=nomultithread $executable \
    restart=true append=false \
    solver:type=rk4 solver:adaptive=false solver:timestep=0.026 \
    nout=10 timestep=0.026 mesh:nx=260 mesh:nz=256 mesh:dx=0.1 mesh:dz=0.1
