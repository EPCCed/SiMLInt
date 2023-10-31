**SiMLInt is an [ExCALIBUR](https://excalibur.ac.uk/) project demonstrating how to integrate Machine Learning (ML) to physics simulations. It combines commonly used, open-source tools with in-house Python scripts to execute ML-aided computational fluid dynamics simulations.** 
This page explains how to set-up the workflow to apply the same techniques to other simulations.


## Codes and Dependencies

Our example workflow uses the following tools:
* [BOUT++](https://boutproject.github.io), written in C++ and Python, as the fluid dynamics simulation code
* [TensorFlow](https://www.tensorflow.org/) (through [Keras](https://keras.io)) to develop, and train the ML model as well as for the ML inference
* [SmartSim](https://github.com/CrayLabs/SmartSim), using SmartRedis in-memory database, handles the communication between the simulation code and the ML model

In order to set up the workflow, you first need to install these tools in the [versions suitable for SmartSim](https://www.craylabs.org/docs/installation_instructions/basic.html#supported-versions). 
For this step, it is best to follow the tool's installing instructions; however, we provide an example step-by-step and expected outcomes at each stage for installing these on [Cirrus](https://www.cirrus.ac.uk).

[Example installation on Cirrus](./example-installation.md)

## Workflow

SiMLInt workflow is currently based on [Learned Correction](https://www.pnas.org/doi/full/10.1073/pnas.2101784118) (LC). 

The numerical solver is used to simulate a system, with adapted parameters so that the system is under-resolved due to the domain being decomposed to a coarser level than would be optimal. Beyond this, the execution of the simulation remains unchanged and can be parallelised as usual.

The coarse granularity of the domain decomposition means the simulation would diverge from the real evolution of the system. To prevent this, the workflow uses a pretraind ML model to adjust the grid at every step of the simulation, keeping the system on the right track.

The ML model is often based on a convolutional neural network (CNN), and is trained to predict the difference between the coarse simulation step and a fully-resolved state, coarsened to match the grid dimensions. Notably, the workflow can be used in a parallelised scenario, where the the correction inference is performed in each parallel process separately, using the partial domain as the ML model's input, and using the model's prediction to correct only that slice.


The diagram below visualises the workflow. The numerical simulation, run in BOUT++, is represented by the black squares and grids, while the Learned Correction loop is realised in SmartSim by calling a TensorFlow model, which returns the correction (orange grid).
 
![SiMLInt workflow](./assets/SiMLInt_workflow.pdf)


We demonstrate the workflow on the Hasegawa-Wakatani set of equations using a dummy ML-model which does not affect the simulation. This allows the users to test that the set-up works and returns the expected results. 

[Detailed instructions](./workflow.md)

## Model training

The example workflow uses a model that returns always 0s for the correction, maintaining the simulation on the same trajectory it would follow without any ML adjustments. The idea of Learned Correction however requires a model that is trained to predict the difference between the fully resolved trajectory that runs over a sufficiently fine resolution of the domain and a trajectory that uses coarser domain decomposition (and coarser time steps). To obtain a suitable ML model, we need to generate training data and use it to train the model.

The data generation schema below outlines the kind of data we need to collect for the model training --- we need to:
1. run a fully resolved simulation (denoted F)
2. coarsen some points on the fine trajectory (denoted C) -- these are *inputs* for the training process
3. make a coarse simulation step from C (denoted by the arrow labelled ∆t_c)
4. calculate the difference between the fully resolved, coarsened grid and the coarse grid (denoted Ĉ at the equivalent simulation step -- this is the *target* to train the model for

![Data Generation](./assets/data_generation_schema.pdf)

The dataset we have created for the Hasegawa-Wakatani example, based on 32,000 fully resolved points and, in the coarsened state prepared for the ML training, taking XXX GB, is available on request.

[Implementation details](./ML_training.md)
