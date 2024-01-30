#!/bin/bash

#SBATCH --job-name=boutsmartsim
#SBATCH --time=0:20:00
#SBATCH --exclusive
#SBATCH --nodes=1
#SBATCH --tasks-per-node=36
#SBATCH --cpus-per-task=1

#SBATCH --account=tc057
#SBATCH --partition=standard
#SBATCH --qos=standard

source /work/tc057/tc057/$USER/.bashrc

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
conda activate boutsmartsim

# run folder
RUN_FOLDER=~/run
cd $RUN_FOLDER
mkdir $RUN_FOLDER/data
cp /work/tc057/tc057/shared/simulation/run_SmartSim/BOUT.inp $RUN_FOLDER/data
cp /work/tc057/tc057/shared/simulation/run_SmartSim/start_db.py $RUN_FOLDER

# Start the orchestrator and a new experiment which launches RedisAI for communication
# Load the model from the given file
# Remember to adjust the path to the start_db.py script!
python start_db.py 6899 /work/tc057/tc057/$USER/zero-model-260-256.pb

export SSDB=127.0.0.1:6899

srun -n 1 --distribution=block:block --hint=nomultithread ~/my-bout-smartsim-hw/build/hasegawa-wakatani
