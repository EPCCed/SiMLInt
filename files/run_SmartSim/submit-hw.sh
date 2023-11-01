#!/bin/bash

#SBATCH --job-name=boutsmartsim
#SBATCH --time=0:20:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1

#SBATCH --account=x01
#SBATCH --partition=standard
#SBATCH --qos=standard

# Setup the job environment (this module needs to be loaded before any other modules)
module load mpt
module load intel-compilers-19
module load fftw/3.3.10-intel19-mpt225
module load netcdf-parallel/4.6.2-intel19-mpt225

# Set the number of threads to 1
#   This prevents any threaded system libraries from automatically
#   using threading.
export OMP_NUM_THREADS=1

# activate conda environment for SmartSim and SmartRedis Python packages
conda activate myvenv

# Start the orchestrator and a new experiment which launches RedisAI for communication
# Load the model from the given file
# Remember to adjust the path to the start_db.py script!
python start_db.py 6899 /work/x01/x01/auser/zero-model-256-double.pb

export SSDB=127.0.0.1:6899
cd my-bout-smartsim-hw
srun -n 1 --distribution=block:block --hint=nomultithread ./hasegawa-wakatani
