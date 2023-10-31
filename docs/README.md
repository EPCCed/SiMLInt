SiMLInt is an [ExCALIBUR](https://excalibur.ac.uk/) project demonstrating how to integrate Machine Learning (ML) to physics simulations. It combines commonly used, open-source tools and few in-house Python scripts to execute ML-aided computational fluid dynamics simulations. This page explains how to set-up the workflow to apply the same techniques to other simulations, possibly using a different set of tools.

SiMLInt workflow is currently based on [Learned Correction](https://www.pnas.org/doi/full/10.1073/pnas.2101784118) (LC), where the system is simulated with a coarser-than-optimal resolution, and the error resulting from this under-resolution is frequently corrected using an convolutional neural network (CNN), which is trained to predict the difference between the coarse and the fully-resolved simulation. 

## Codes and Dependencies

Our example workflow uses the following tools:
* [BOUT++](https://boutproject.github.io), written in C++ and Python, as the fluid dynamics simulation code
* [TensorFlow](https://www.tensorflow.org/) (through [Keras](https://keras.io)) to develop, and train the ML model as well as for the ML inference
* [SmartSim](https://github.com/CrayLabs/SmartSim), using SmartRedis in-memory database, handles the communication between the simulation code and the ML model

In order to set up the workflow, you first need to install these tools in the [versions suitable for SmartSim](https://www.craylabs.org/docs/installation_instructions/basic.html#supported-versions). 
For this step, it is best to follow the tool's installing instructions; however, we provide an example step-by-step and expected outcomes at each stage for installing these on [Cirrus](https://www.cirrus.ac.uk).

[Example installation on Cirrus](./example-installation.md)

## Workflow

We demonstrate the workflow on the Hasegawa-Wakatani set of equations using a dummy ML-model which does not affect the simulation. This allows you to test that the set-up works and returns the expected results. 

*include conceptual description of the workflow*

[Detailed instructions](./workflow.md)

## Model training

*conceptual description*

[Implementation details](./ML_training.md)
