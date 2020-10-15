# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 12:24:23 2020

@author: Laks
"""
# this script estimate the percentage of the observation values fall inside the uncertainty bound

import numpy as np

def obsv_inside(CI):
# assign the initial variable  
    log_bound =np.zeros(len(CI))
# iteration starts with the condition statement
    for i in range(len(CI)):
        if ((CI.lb[i] < CI.H[i]) and (CI.ub[i] > CI.H[i])):
            log_bound[i] = 1
        else:
            log_bound[i] = 0   
    #percentage of logical value
    inside_bound = np.count_nonzero(log_bound)/float(len(log_bound))*100
    #inside_bound = round(inside_bound)
    
    return inside_bound