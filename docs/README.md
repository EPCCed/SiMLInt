SiMLInt is an [ExCALIBUR](https://excalibur.ac.uk/) project demonstrating how to integrate Machine Learning (ML) to physics simulations. It combines commonly used, open-source tools and few in-house Python scripts to execute ML-aided computational fluid dynamics simulations. This page explains how to set-up the workflow to apply the same techniques to other simulations, possibly using a different set of tools.

SiMLInt workflow is currently based on [Learned Correction](https://www.pnas.org/doi/full/10.1073/pnas.2101784118) (LC), where the system is simulated with a coarser-than-optimal resolution, and the error resulting from this under-resolution is frequently corrected using an convolutional neural network (CNN), which is trained to predict the difference between the coarse and the fully-resolved simulation. 

## Codes and Dependencies

Our example workflow uses the following tools:
* [BOUT++](https://boutproject.github.io), written in C++ and Python, as the fluid dynamics simulation code
* [TensorFlow](https://www.tensorflow.org/) (through [Keras](https://keras.io)) to develop, and train the ML model as well as for the ML inference
* [SmartSim](https://github.com/CrayLabs/SmartSim), using SmartRedis in-memory database, handles the communication between the simulation code and the ML model

In order to set up the workflow, you first need to install these tools in the version suitable for SmartSim. For this step, it is best to follow the developers' instructions; however, we provide an example step-by-step and expected outcomes at each stage for installing these on [Cirrus](https://www.cirrus.ac.uk).

[Example installation on Cirrus](./example-installation.md)

## Workflow

We demonstrate the workflow on the Hasegawa-Wakatani set of equations using a dummy ML-model which does not affect the simulation. This allows you to test that the set-up works and returns the expected results. 


### Export zero model

Activate the conda environment with SmartSim (see Cirrus example to make sure it has all relevant packages)
```
conda activate myvenv
```

Export the (trained) ML model in a format suitable for SmartSim. 

In our example we are using a grid 128x256 with 4 guard cells in the x dimension, hence our model expects a grid of size (132, 256). Here we use a model that returns all zeros to ..., so we create
`zero_model-132-256.pb` in the current directory:
```
python write_zero_model.py 132 256 -f zero-model-132-256.pb
```

The `write_zero_model.py` defines a simple CNN which returns all zeros... 
Note that the script requires also `padding.py`, which is our in-house implementation of periodic padding, which is not currently implemented in TensorFlow.

You can now test the zero model:
```
python zero_model_test.py
```
This launches a database, uploads the zero model and inputs a random tensor, returning a tensor of the same size, containing only zeroes. The output gets printed on screen.

### Compile Hasegawa Wakatani with SmartRedis

Load modules
```
module load mpt
module load intel-compilers-19
module load fftw/3.3.10-intel19-mpt225
module load netcdf-parallel/4.6.2-intel19-mpt225
module load cmake
```

Modify `CMakeLists.txt` and `hw.cxx`.

Outside the BOUT-dev root directory you can set the location of the BOUT++ build path for CMake:
```
cmake . -B build -Dbout++_DIR=/PATH/TO/BOUT-dev/build -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release
```

Compile:
```
cmake --build build --target hasegawa-wakatani
```

### Python script to start database and upload zero model

The python script `start_db.py` starts the RedisAI database and uploads the zero model.
This script must be run before the simulation starts (or both added to an orchestrator).

Change the model path in line 18.

To start the database at port 6899:
```
python start_db.py 6899 /path/to/zero-model-132-256.pb
```

### Run with SmartRedis database

The slurm job file starts the SmartSim orchestrator (in Python) with a Redis database and RedisAI communication layer.
The environment variable SSDB points to the database entrypoint to which the simulation connects.
In this example, the Redis DB runs on the same node since the simulation only runs in one process.








