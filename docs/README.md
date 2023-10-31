# SiMLInt GitHub Page

(Based on [minimal theme](https://github.com/pages-themes/minimal/blob/master/index.md))

View the GitHub page at [https://epcced.github.io/SiMLInt/](https://epcced.github.io/SiMLInt/)

SiMLInt is an [ExCALIBUR](https://excalibur.ac.uk/) project demonstrating how to integrate Machine Learning (ML) to physics simulations. It uses BOUT++, SmartSim, TensorFlow and in-house Python code to execute machine-learning-aided computational fluid dynamics simulations. 

SiMLInt workflow is currently based on [Learned Correction](https://www.pnas.org/doi/full/10.1073/pnas.2101784118) (LC), where the system is simulated with a coarser-than-optimal resolution, and the error resulting from this under-resolution is frequently corrected using an convolutional neural network (CNN), which is trained to predict the difference between the coarse and the fully-resolved simulation. 

Our example workflow uses the following tools:
* [BOUT++](https://boutproject.github.io), written in C++ and Python, is used as the fluid dynamics simulation code
* The CNN is developed and trained in [TensorFlow](https://www.tensorflow.org/) through [Keras](https://keras.io)
* The communication between the simulation code and the ML steps is handled by [SmartSim](https://github.com/CrayLabs/SmartSim) using SmartRedis in-memory database







