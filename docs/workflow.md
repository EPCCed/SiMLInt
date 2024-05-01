# SiMLInt Workflow

The system needs to have all the tools and packages (in suitable versions) installed. See the main page and the example of installation for help. 

The example workflow described here does not require a pre-trained ML model, we are using a placeholder model that alwyas returns zeroes to showcase the framework, and the script is provided here. Obviously, any other model can be exported in the desired format and used in the workflow.


<!-- 
## Export the ML model

Activate the conda environment with SmartSim (see Cirrus example to make sure it has all relevant packages)
```
conda activate myvenv
```

Export the (trained) ML model to a format suitable for SmartSim. For simplicity, you can simply generate a zero-model, that is, a model which returns a tensor of 0s regardless of the provided input. Data generation and training necessary to build an error-predicting model is decscribed [here](https://github.com/EPCCed/SiMLInt/tree/main/docs#model-training), and the resulting model can be used in place of the zero-model at all steps of the workflow below.

In the small test example, we are using a grid 128x256 with 4 guard cells in the x-dimension, hence our model expects a grid of size (132, 256). To demonstrate the workflow, we use a model that returns a tensor of zeroes, this allows the user to easily verify that the added ML-loop does not distort the simulation in any unexpected way. 

Create `zero_model-132-256.pb` in the current directory:
```
python write_zero_model.py 132 256 -f zero-model-132-256.pb
```

The `write_zero_model.py` uses the target CNN architecture with a modified final layer to force all-zeroes output while maintaining properties of the model, such as computational effort needed to add the ML inference to the workflow.
Note that the script requires also `padding.py`; this is our in-house implementation of periodic padding which is currently not implemented in TensorFlow.

You can now test the zero model:
```
python zero_model_test.py
```
This script launches a database and uploads the zero model. It generates a random tensor and uses it as input for the model inference, which should return a tensor of the same dimensions filled with zero. The output gets printed on screen so that one can easily verify the content of the returned tensor. -->

## Compile Hasegawa Wakatani with SmartRedis

Hasegawa-Wakatani system of equations is included among BOUT++ examples and gets downloaded to the system during BOUT++ installation.

With `myvenv` still active, load the following modules:
```
module load fftw/3.3.10-intel19-mpt225
module load netcdf-parallel/4.6.2-intel19-mpt225
module load cmake
```

Make a working copy of the hasegawa-wakatani example outside the BOUT-dev root directory
```
cp -r BOUT-dev/examples/hasegawa-wakatani my-bout-smartsim-hw
cd my-bout-smartsim-hw
```

Set the location of the BOUT++ build path for CMake
```
cmake . -B build -Dbout++_DIR=../BOUT-dev/build -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release
```

Compile your version of Hasegawa-Wakatani example. `my-bout-smartsim-hw` should contain (among others) `CMakeLists.txt` and `hw.cxx` which you need to modify --- The `CMakeLists.txt` needs to point to the path to the SmartRedis libraries as discussed in [the example installation](https://github.com/EPCCed/SiMLInt/blob/docs/docs/example-installation.md#build-smartredis-libraries), while the changes to `hw.cxx` implement the call onto the SmartRedis database and the CNN within, and receives and actions the correction to the simulation. You can see examples of the modified files in [files/modified_HW](https://github.com/EPCCed/SiMLInt/tree/docs/files/modified_HW).
```
cmake --build build --target hasegawa-wakatani
```

## Running the simulation using SmartRedis

You need to start the RedisAI database and upload the ML models, this can be done by calling a python script `start_db.py` with appropriate arguments specifying the port where the database will be available and path to the ML models (first the 'vort' model, then the 'n' model). 
This must be done before the simulation starts (or both added to an orchestrator).

To start the database eg at port 6899 with the zero model created earlier, run
```
python start_db.py 6899 /path/to/model-hw-20240427-164026-vort.pb /path/to/model-hw-20240427-210530-dens.pb
export SSDB=127.0.0.1:6899
```
Example models can be found in [files/models](https://github.com/EPCCed/SiMLInt/blob/docs/files/models). 

The environment variable SSDB points to the database entrypoint to which the simulation connects.

The simulation can be then started using the executable available in [files/HW-error-correction](https://github.com/EPCCed/SiMLInt/blob/docs/files/HW-error-correction).

Both of these commands are used by the SLURM submission script [files/6-simulation/submit-hw.sh](https://github.com/EPCCed/SiMLInt/blob/docs/files/6-simultaion/submit-hw.sh), which can be modified with you account and used on Cirrus.

[< Back](./)
