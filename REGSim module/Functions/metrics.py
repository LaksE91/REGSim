# -*- coding: utf-8 -*-
"""
Last edited on Tue May 28 17:11:19 2019

@author: Lakshmi
"""

### This  script is about the objective functions such as root mean squared error
import numpy as np

# Calculate Root Mean Squared Error
def rmse_metric(obs, sim):
    rmse = np.sqrt((np.mean((obs-sim)**2)))
    return rmse

# Calculate Mean Absolute Error
def mae_metric(obs, sim):
    mae = np.mean(np.abs((obs-sim)))
    return mae

# Calculate Nash Sutcliff Efficiency   
def nse_metric(obs,sim):
    nse = 1 - sum((sim-obs)**2)/sum((obs-np.mean(obs))**2)
    return nse

