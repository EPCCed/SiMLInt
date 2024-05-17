# Running SiMLInt LC Simulation (Inference)

Running a simulation with LC using the SiMLInt framework requires SmartSim, BOUT++ (with modified [hw.cxx](https://github.com/EPCCed/SiMLInt/tree/main/files/HW-error-correction/hw.cxx)) and TensorFlow. To install these, follow the [example installation](example-installation.md). Now the SmartRedis Client is included to send/receive data from the SmartRedis database, request ML model runs and add the inferred error correction to BOUT++ internal variables for vorticity and density.

```shell
module load intel-20.4/mpi
module load intel-20.4/compilers
module load fftw/3.3.10-intel20.4-impi20.4
module load netcdf-parallel/4.9.2-intel20-impi20
module load cmake

cd $SIMLINT_HOME/HW-error-correction

cmake . -B build -Dbout++_DIR=$WORK/BOUT-dev/build -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release
cmake --build build --target hasegawa-wakatani
```

Modify the job submission file [submit-hw.sh](https://github.com/EPCCed/SiMLInt/tree/main/files/5-simulation/submit-hw.sh) to reference the model files produced in the model training phase (step 5), for example:

```shell
model_vort=${WORK}/models/model-hw-20240427-164026-vort.pb
model_n=${WORK}/models/model-hw-20240427-210530-dens.pb
```

The file name includes the timestamp when the model was trained and will be different in your example run.

To run a simulation:

```shell
cd $SIMLINT_HOME/6-simulation
sbatch submit-hw.sh --account $ACCOUNT
```

The output should differ slightly from a "pure" BOUT++ Hasegawa-Wakatani in that information about the SmartRedis database is given, and extra lines are produced during simulation to give timing information on communication with the database.

To visualise the result of this, or any other BOUT++ simulations, see the Jupyter Notebook, [Visualise.ipynb](https://github.com/EPCCed/SiMLInt/tree/main/files/7-visualisation/Visualise.ipynb). See [Cirrus Docs](https://docs.cirrus.ac.uk/user-guide/python/#using-jupyterlab-on-cirrus) for notes on running Jupyter Lab on Cirrus.

[< Back](./)
