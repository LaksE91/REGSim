# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:20:00 2018

@author: Lakshmi
"""
import numpy as np
import numpy.matlib
from metrics import *

## choice of selecting the return output
class choicedata():
    def __init__(self, rmse,mae,nse,gwhead):
        # you can put here some validation logic
        self.rmse = rmse
        self.mae = mae
        self.nse = nse
        self.gwhead = gwhead

#function to define the model
def modelrun(Pset,var,area,test_case):    
    
# assign the input to the variable    
    pdata                  = np.array(var.P)  # rainfall
    gwdata                 = np.array(var.H)  # groundwater head
    
    try:
        qin                = np.array(var.Qin) # Lateral inflow
        qout               = np.array(var.Qin) # lateral outflow
    except:
        qin                = np.zeros(len(gwdata))
        qout               = np.zeros(len(gwdata))
        
    Sy                     = float(Pset[0]) #specific yield
    p                      = float(Pset[1]) # pumping discharge

#get the number of months of avialable data
    nummonths              = len(gwdata)
    numyears               = nummonths/12

#assign input to the model
    if test_case ==1:
        rr                 = np.array([1,1,1,1,1,1,1,1,1,1,1,1])
        rechargeratio      = (rr)*float(Pset[2])
    if test_case==2:
        r1                 = float(Pset[2])
        r2                 = float(Pset[3])
        rechargeratio      = [r1,r1,r1,r1,r1,r1,r2,r2,r2,r2,r1,r1]
    if test_case ==3:
        r1                 = float(Pset[2])
        r2                 = float(Pset[3])
        r3                 = float(Pset[4])
        rechargeratio      = [r1,r1,r2,r2,r2,r2,r3,r3,r3,r3,r1,r1] 

# max pumping with 50% less in monsoon and 100% in nonmonsoon season
    Qp                     = np.array([1,1,1,1,1,1,0.5,0.5,0.5,0.5,1,1])
    pumping                = p*Qp   

# repeat the data for the respective years
    rechargetimes          = numpy.matlib.repmat(rechargeratio,1,numyears)
    pumptimes              = numpy.matlib.repmat(pumping,1,numyears)
    rechargetimes          = rechargetimes.reshape(nummonths)
    pumptimes              = pumptimes.reshape(nummonths)

#assign Constant and initial variables as an input to the model
    gwhead                 = np.zeros(nummonths) 
    gwhead[0]              = gwdata[0]     # initial head
    effectiveer            = pdata/1000    # converting millimeter to meter

# iteration of the model starts
    for m in range(1,nummonths):
        rh                 = (effectiveer[m]*rechargetimes[m])/Sy 
        ph                 = (pumptimes[m]/(Sy*area))
        lh                 = ((qin[m]-qout[m])/(Sy*area))
        gwhead[m]          = (gwhead[m-1] - (rh-ph +lh))

# calculate the metrics
    rmse                   = rmse_metric(gwdata,gwhead) # minimize
    mae                    = mae_metric(gwdata,gwhead)  # minimize
    nse                    = -nse_metric(gwdata,gwhead) # maximize   
    return rmse,mae,nse,gwhead

# Calbration process for the model
def sim_mod(Pset,var,area,test_case):
    choice_data= modelrun(Pset,var,area,test_case)
    return choice_data[0], choice_data[1],choice_data[2]
