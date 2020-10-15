# REGSim

Recharge Estimation and Groundwater Simulation is a flexbile tool designed to estimate the recharge and simulate the groundwater levels by using a parsimonious groundwater model. This tool incorporates the two-step process: 
1.	Simulation and optimization method
2.	Uncertainty and sensitivity analysis


It includes the estimation of lateral groundwater fluxes using Darcy’s law, calibration of the groundwater model by Non-dominated Sorting Genetic Algorithm (NSGA-II) and predicting the uncertainty bounds of groundwater head using Generalized Likelihood Uncertainty Estimation (GLUE) method.


# Content 
The entire set up was developed using six python modules which include:
1.	Step_1a_Estimation_of_slope.py – estimate the gradient of the aquifer boundary
2.	Step_1b_Estimation_of_lateralflow.py – estimate the average lateral flow 
3.	Step_2_Calibration_of_the_model.py - calibrate the parameters using multi-objective optimization
4.	Step_3_Validation_of_the_model.py – validate the model using the optimal parameter set
5.	Step_4a_Uncertainty_check.py – uncertainty using GLUE method.
6.	Step_4b_Sensitivity.py – sensitivity analysis of the parameters using the cumulative distribution function

# Example 
This framework includes sample data (‘Data/sampledata.csv’) to demonstrate the function of REGSim. User documentation is included for further details. 

# Citation 

DOI : https://zenodo.org/badge/latestdoi/304316690

## License & copyright

© Lakshmi Elangovan , IIT Hyderabad

REGSim is licensed under the under [MIT License](LICENSE) 
