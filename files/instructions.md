# hands-on: Simulation and Machine Learning Integration 
**(ExCALIBUR workshop: Data Driven Algorithms)**

## 1. Cirrus

Log in to Cirrus:

`$ ssh username@login.cirrus.ac.uk`

or, if you used any non-default name or location for your private SSH key, `$ ssh username@login.cirrus.ac.uk -i /home/user/.ssh/id_rsa_cirrus` .

Feel free to have a look around.


### File systems

There are two file systems we will concern ourselves with, `/home` and `/work`. On logging in you will find yourself in your home directory at
`/home/tc057/tc057/username`. The `/home` file system is not particularly large but can be used to store some important files. Importantly, it is not mounted on the compute nodes. Jobs will instead be run from within the `/work` file system. 

You will have your own work directory at `/work/tc057/tc057/username`. Disc space is shared between all members of the project (i.e. all attendees and demonstrators at this event). Please keep this for the exercises only, and clean up if you accidentally produce any huge files.

Your home and work directories are kept private to you alone. If you want to share files with anyone else, or if the demonstrators want to share files with you, the shared directories can be used. These exist on both file systems in two hierarchies. To share with other users in this project (who are also members of the tc057 Unix group), use
`/work/tc057/tc057/shared`, and to share with anyone on any other project you can use `/work/tc057/shared`

You may still need to set read permissions on anything you copy into these directories. For example, to recursively set group read and execute permissions on a directory, allowing other tc057 project members to read it and its contents:
`$ chmod -R g+rX /work/tc057/tc057/shared/mydirectory`.


### Modules

Environment modules are available. You can use the commands you are probably used to
```
$ module list
$ module avail
$ module load <modulename>
```
to list the currently loaded modules, see what other modules are available, and then to load a module. 


### Running jobs

Jobs are run via the Slurm batch system. The job scripts you will use will be covered in the training material. You will be able to run jobs via the normal QoS if you like, but we have also set up reservations on Cirrus to allow our group exclusive access to several compute nodes, ensuring quick job throughput.

In a Slurm job script the account (budget to charge), partition (group or type of nodes to run on) and QoS (type of job, determining the limits that apply) will be specified by options to the sbatch command used to submit the job. To use a given reservation, you must also provide its code. All in all, you should provide the following options in your scripts:
```
#SBATCH --account=tc057
#SBATCH --partition=standard
#SBATCH --qos=reservation
#SBATCH --reservation=tc057_1141276
```

### Further reading

If you would like to read more about using Cirrus, the documentation is available online at https://docs.cirrus.ac.uk .


## 2. Build the individual components



First, set up `.bashrc` and `.bash_login`: login to Cirrus, then enter the following:
```
echo "source /work/tc057/tc057/$USER/.bashrc" > .bash_login
echo "export WORK=/work${HOME#/home}" > /work/tc057/tc057/$USER/.bashrc
echo "export HOME=$WORK" >> /work/tc057/tc057/$USER/.bashrc
echo "cd $WORK" >> /work/tc057/tc057/$USER/.bashrc
```
`exit` and log in again to complete this setup. Do `pwd` to check you are in `/work/tc057/tc057/$USER` .

### BOUT++

Load required modules:
```
module load mpt
module load intel-compilers-19
module load fftw/3.3.10-intel19-mpt225
module load netcdf-parallel/4.6.2-intel19-mpt225
module load cmake
```

BOUT++ installation requires a Python environment. We'll use miniconda3:
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
~/miniconda3/bin/conda init bash
```

Now `exit` and login to Cirrus again to complete the miniconda3 setup.

Create and activate a conda environment:
```
conda create -y --name boutsmartsim python=3.10
conda activate boutsmartsim
```

Build BOUT++:
```
module load mpt
module load intel-compilers-19
module load fftw/3.3.10-intel19-mpt225
module load netcdf-parallel/4.6.2-intel19-mpt225
module load cmake

git clone https://github.com/boutproject/BOUT-dev.git
cd /work/tc057/tc057/$USER/BOUT-dev

MPICXX_CXX=icpc MPICC_CC=icc MPICXX=icpc cmake . -B build -DBOUT_DOWNLOAD_NETCDF_CXX4=ON -DBOUT_USE_LAPACK=off -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release

export PYTHONPATH=~/BOUT-dev/build/tools/pylib:~/BOUT-dev/tools/pylib:$PYTHONPATH

cmake --build build -j 6

cd ~
```

#### Example: Hasegawa-Wakatani
This will build a *pure* BOUT++ version of the Hasegawa-Wakatani example. A build with SmartSim connection capability is described later.

In `/work/tc057/tc057/$USER/BOUT-dev/`:
```
MPICXX_CXX=icpc MPICXX=mpicxx cmake .  --build build -DBOUT_BUILD_EXAMPLES=on

cmake --build build --target hasegawa-wakatani
```

### SmartSim and it's ML wrapper


#### Python/conda environment

Add the following packages to install SmartSim ML wrapper:
```
conda install -y git-lfs
git lfs install
pip install smartsim[ml]
```

Build:
```
module load intel-compilers-19
module load cmake
smart build --device cpu 
```

#### Build SmartRedis libraries

Clone the git repo and the required version and build:
```
git clone https://github.com/CrayLabs/SmartRedis.git --branch v0.5.0
cd SmartRedis/
make lib
```

The install path is then available in `SmartRedis/install`.

### ML-models

Activate the conda environment with SmartSim
```
conda activate boutsmartsim
```

In this example, we are using a grid 256x256 with 4 guard cells in the x-dimension, hence our model expects a grid of size (260, 256). These dimensions need to match on the resolution specified in the simulation's input file, `/work/tc057/tc057/shared/simulation/run_SmartSim/BOUT.inp`.

To demonstrate the workflow, we use a model that returns a tensor of 0s, this allows us to easily verify that the added ML-loop does not distort the simulation in any unexpected way. All python scripts used in this section are available in `/work/tc057/tc057/shared/ML_model/`.

First, we export the ML model to a format suitable for SmartSim -- `zero_model-260-256.pb`, using the `write_zero_model.py` script in your main directory:
```
cd /work/tc057/tc057/$USER

python /work/tc057/tc057/shared/simulation/ML_model/write_zero_model.py 260 256 -f zero-model-260-256.pb
```

The `write_zero_model.py` uses the target CNN architecture with a modified final layer to force all-0s output while maintaining properties of the model, such as computational effort needed to add the ML inference to the workflow.

Note that the script requires also `padding.py`; this is our in-house implementation of periodic padding which is currently not implemented in TensorFlow, and you need to have a copy of it in the directory you are running `write_zero_model.py` from.

You can now test the zero model:
```
cp /work/tc057/tc057/shared/simulation/ML_model/zero_model_test.py ~
```

Modify the "zero_model_test.py` to have the correct model_path (line 13) and tensor shape (line 24).
```
python zero_model_test.py
```
This script launches a database and uploads the zero model. It generates a random tensor and uses it as input for the model inference, which should return a tensor of the same dimensions filled with zero. The output gets printed on screen so that one can easily verify the content of the returned tensor.

> **Try this:** Clone and modify the python scripts to generate an arbitrary "bad" model, and repeat the steps above to test that this new model returns a "bad" tensor. 
>
> What makes a model "bad"?


## 4. Simulation

### Compile the example (modified Hasegawa-Wakatani)

Hasegawa-Wakatani system of equations is included among BOUT++ examples and is part of the installation scripts in /shared/BOUT-dev. We will, however, need to make few modifications to make it run using SmartRedis. 

With `boutsmartsim` still active, load the following modules:
```
module load mpt
module load intel-compilers-19
module load fftw/3.3.10-intel19-mpt225
module load netcdf-parallel/4.6.2-intel19-mpt225
module load cmake
```

Make a working copy of the hasegawa-wakatani example outside the BOUT-dev root directory
```
cp -r BOUT-dev/examples/hasegawa-wakatani my-bout-smartsim-hw
cd my-bout-smartsim-hw
```

Compile your version of Hasegawa-Wakatani example. 

Modify the Hasegawa-Wakatani example: `my-bout-smartsim-hw` should contain (among others) `CMakeLists.txt` and `hw.cxx`. Replace these files with their modified version available in `/work/tc057/tc057/shared/simulation/modified_HW/`. 
- The changes to `hw.cxx` implement the call onto the SmartRedis database and the CNN within, and receives and actions the correction to the simulation. 
- You will need to further update this version of `CMakeLists.txt` so that it points to the path to the SmartRedis libraries - edit line 5 `set(SMARTREDIS_INSTALL_PATH /path/to/SmartRedis/install)`.

Set the location of the BOUT++ build path for CMake
```
cmake . -B build -Dbout++_DIR=../BOUT-dev/build -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release
cmake --build build --target hasegawa-wakatani
```


### Run mHW with ML-model

Create a run folder and copy over a BOUT input file:
```
mkdir ~/run
cp /work/tc057/tc057/shared/simulation/run_SmartSim/BOUT.inp ~/run
```

You can see an example job-submission script in `/work/tc057/tc057/shared/simulation/run_SmartSim/submit-hw.sh`. This slurm job file starts the SmartSim orchestrator (in Python) with a Redis database and RedisAI communication layer. In this example, the Redis DB runs on the same node since the simulation only runs in one process. The script sets up the environment as needed, in particular, it 

1. starts the RedisAI database and uploads the ML model using a python script `/work/tc057/tc057/shared/simulation/run_SmartSim/start_db.py` with appropriate arguments specifying the port where the database will be available and path to the ML model. This must be done before the simulation starts (or both added to an orchestrator):  
    the line `python start_db.py 6899 /work/tc057/tc057/$USER/zero-model-260-256.pb`
    needs to be modified so that it points to your instance of the ML model (i.e., `/work/tc057/tc057/$USER/zero-model-260-256.p`) 
    and a suitable `start_db.pb`  --- either in `/shared`, or feel free to make and use your local copy where you are launching the script from.


2. Sets the environment variable SSDB to points to the database entrypoint to which the simulation connects.
    Our example uses 6899, but this can be arbitrarily changed in case a conflict occurs.

For additional runs, copy this to your `/work` folder, create a new folder for the outputs, e.g. `hw-run-1`, and edit line 36 to match the new folder (`RUN_FOLDER=~/hw-run-1`). 

Note: this scripts expects `zero-model-260-256.pb` to be in your /work folder. Edit line 32 if you have created it elsewhere.

This slurm job file starts the SmartSim orchestrator (in Python) with a Redis database and RedisAI communication layer.  In this example, the Redis DB runs on the same node since the simulation only runs in one process.

> **Try this:** Run mHW with the "bad" ML-model.




