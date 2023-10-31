# files
You can find files useful for running the ML-aided workflows here.

## ML_model
This folder contains files related to the ML model --- its architecture and conversion to format used in the workflow. 

## modified_HW
The simulation software, BOUT++, comes with a set of examples, including the Hasegawa-Wakatani set of equations. We are using this example to demonstrate the whole workflow, but several files need to be modified in order to gain access to SmartRedis and the ML model. The modified files are included here.

## run_SmartSim
Scripts to start the in-memory database and to submit a job running the workflow.