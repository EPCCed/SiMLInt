# ML Model Training

Following on from the [data generation phase](data-generation.md) of our implementation for the Hasegawa-Wakatani example, this page describes how we train our ML models.


We are at the stage of having fine-grained simulation trajectories, and from those, extracted data for each timestep, coarsened that data, and run single-timestep coarse-grained simulations. We have then converted that data to NetCDF files that contain data at timestep 0 (gt_traj_{traj}.nc), the ground-truth data resulting from coarsening of the fine-grained simulation for trajectory {traj}, and at timestep 1 (sim_traj_{traj}.nc), the coarse-grained simulation output following a single time step.

The files in [files/5-training](https://github.com/EPCCed/SiMLInt/tree/main/files/5-training) take this data and perform: (1) error calculation; (2) ML model training and (3) freezing the models for use in LC simulations.

1. Error calculation.

    The error between these is calculated on-the-fly in [files/5-training/data_read.py](https://github.com/EPCCed/SiMLInt/tree/main/files/5-training/data_read.py). This script loads all available gt_traj_{traj}.nc and sim_traj_{traj}.nc files, and generates raw coarse-grained and error data for two BOUT++ variables: 'vort' (the vorticity) and 'n' (the density).

2. Model.

    [files/5-training/model.py](https://github.com/EPCCed/SiMLInt/tree/main/files/5-training/model.py) describes a convolutional neural network (CNN) that with 6 hidden layers that, given the coarse-grained data, aims to predict the error.

3. Training.

    Running [files/5-training/training.py](https://github.com/EPCCed/SiMLInt/tree/main/files/5-training/training.py) via `sbatch submit-training.sh` submits the training script to a GPU node on Cirrus. It trains two models (one to correct vorticity and one to correct density) which it then freezes to file. Examples of these can be found in [files/models](https://github.com/EPCCed/SiMLInt/tree/main/files/models). These will be loaded into the SmartRedis database for use during LC simulations.

The [next step](inference.md) is to run a LC simulation using SmartSim, BOUT++ and TensorFlow, with inference from the newly trained model.