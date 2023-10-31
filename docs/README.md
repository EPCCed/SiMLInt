SiMLInt is an [ExCALIBUR](https://excalibur.ac.uk/) project demonstrating how to integrate Machine Learning (ML) to physics simulations. It combines commonly used, open-source tools and few in-house Python scripts to execute ML-aided computational fluid dynamics simulations. This page explains how to set-up the workflow to apply the same techniques to other simulations, possibly using a different set of tools.

SiMLInt workflow is currently based on [Learned Correction](https://www.pnas.org/doi/full/10.1073/pnas.2101784118) (LC), where the system is simulated with a coarser-than-optimal resolution, and the error resulting from this under-resolution is frequently corrected using an convolutional neural network (CNN), which is trained to predict the difference between the coarse and the fully-resolved simulation. 

Our example workflow uses the following tools:
* [BOUT++](https://boutproject.github.io), written in C++ and Python, as the fluid dynamics simulation code
* [TensorFlow](https://www.tensorflow.org/) (through [Keras](https://keras.io)) to develop, and train the ML model as well as for the ML inference
* [SmartSim](https://github.com/CrayLabs/SmartSim), using SmartRedis in-memory database, handles the communication between the simulation code and the ML model

## Codes and Dependencies

In order to set up the workflow, you need to install a ...
*
*
...

To get these installed to your system, we suggest you follow the developers' instructions, however,we provide an example step-by-step instructions and expected outcomes for installing these on [Cirrus](https://www.cirrus.ac.uk).

> [Example installation on Cirrus](./example-installation)

## Workflow

...










