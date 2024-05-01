# Data Generation

Following the structure given in the [general data generation](ML_training.md) case, this page describes our implementation for the Hasegawa-Wakatani example.

1. Fine- and coarse-grained resolutions. We chose:
 - 1024x1024 for fine-grained simulations; and
 - 256x256 for coarse-grained simulations.

    For BOUT++ our implementation, we performed 2-d simulations, with guard cells in the x-dimension (1028 or 260 x values), 1 y value, and a periodic z-dimension (1024 or 256 values). Therefore the shapes of the variables used by BOUT++ are (1028x1x1024) for the fine-grained simulations and (260x1x256) for the coarse-grained simultions.

2. Generate a "fully resolved" simulation

    The first step is to create a modified version of the Hasegawa-Wakatani example from BOUT++, which we'll copy to `/work/x01/x01/$USER/my-hw`.

    ```shell
    # For full compatibility with the test simulations run during the SiMLInt project, the diffusive function is modified.
    cp -r $WORK/BOUT-dev/examples/hasegawa-wakatani $WORK/my-hw
    cd $WORK/my-hw
    sed -i 's/-Dn \* Delp4(n);/+Dn \* Delp2(n);/g' hw.cxx
    sed -i 's/-Dvort \* Delp4(vort);/+Dvort \* Delp2(vort);/g' hw.cxx

    # recompile
    module load intel-20.4/mpi
    module load intel-20.4/compilers
    module load fftw/3.3.10-intel20.4-impi20.4
    module load netcdf-parallel/4.9.2-intel20-impi20
    module load cmake

    cmake . -B build -Dbout++_DIR=../BOUT-dev/build -DCMAKE_CXX_FLAGS=-std=c++17 -DCMAKE_BUILD_TYPE=Release
    cmake --build build --target hasegawa-wakatani
    ```
    
    Before simulating the training data, a burn-in run must be conducted at the desired resolution. For an example of this, see [fine_init.sh](../files/data-generation/fine_init.sh). Edit `<account>` on line 9 and `x01` in lines containing paths to match your `$WORK` and desired `/scratch` locations and submit via `sbatch fine_init.sh`.

    Following that, we run a number of sequentially trajectories to generate fine-grained ground-truth data. See [fine_trajectories.sh](../files/data-generation/fine_trajectories.sh)

    The initial simulation produces "restart files", `/scratch/space1/x01/data/my-scratch-data/initial/data/BOUT.restart.*.nc` from which a simulation can be continued. Those, as well as the input file (`/scratch/space1/x01/data/my-scratch-data/initial/data/BOUT.inp` should be placed in `/scratch/space1/x01/data/my-scratch-data/0`.

    Edit line 17 (`for TRAJ_INDEX in {1..10}`) to give the desired number of trajectories. Edit `<account>` on line 9 and `x01` in lines containing paths for your project and submit via `sbatch fine_trajectories.sh`.

3. Coarsen selected simulation snapshots.

    Fine-grained data must be coarsened to match the desired coarse-grained resolution. This can be done via interpolation for a general solution. Files in [files/coarsening](../files/coarsening) perform this task. Submit `submit-resize.sh` via `sbatch submit-resize.sh`.

    _Note: this operates on one trajectory at a time and will therefore need to be repeated for each trajectory run in step 2.

4. Single-timestep coarse simulations.

    With the previous step having extracted fine-grained data for each time step (and each trajectory for which it was repeated), we now need to run a single-timestep coarse-grained simulation. To do this, see [files/coarse_simulations](../files/coarse_simulations/). Submitting [run_coarse_sims.sh](../files/coarse_simulations/run_coarse_sims.sh) will run a single step simulation for each coarsened timestep created in the previous step.

Subsequent steps: calculating the error; reformatting data for ingestion into TensorFlow; and model training are covered in [ML model training implementation](training_implementation.md).


