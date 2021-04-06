# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:20:00 2018

@author: Lakshmi
"""
import numpy as np
import numpy.matlib
from metrics import *
from Utils import fillrech
from pumpfunc import *

## choice of selecting the return output
class choicedata():
    def __init__(self, rmse,mae,nse,gwhead):
        # you can put here some validation logic
        self.rmse   = rmse
        self.mae    = mae
        self.nse    = nse
        self.gwhead = gwhead

#function to define the model
def modelrun(Pset,var,area,test_case,mv,pcase):    
    
# assign the input to the variable    
    pdata                  = np.array(var.P)  # rainfall
    gwdata                 = np.array(var.H)  # groundwater head
    pedata                 = np.array(var.PE) # potential evapotranspiration
 
# choose model variant (0: Recharge as the function of P; 1: Recharge as the function of P and PE)    
    def precp():
        er = pdata/1000
        return er

    def pevap():
        er                    = (pdata-pedata)/1000
        sort_er           = [i if i>0 else 0 for i in er]
        return sort_er
    
    switcher ={
            0: precp,
            1: pevap,
            } 
    
# Switch case function to select the model variant condition  
    def model_variant(argument): 
        # Get the function from switcher dictionary
        func = switcher.get(argument)
        if func is None:
            raise ValueError("test case not found")
        # Execute the function
        return func()
   
# Check the lateral flow inclusion
    try:
        qin                = np.array(var.Qin) # Lateral inflow
        qout               = np.array(var.Qin) # lateral outflow
    except:
        qin                = np.zeros(len(gwdata))
        qout               = np.zeros(len(gwdata))
        
# Parameterization         
    Sy                     = float(Pset[0]) #specific yield
    Qpmax                  = float(Pset[1]) # pumping discharge

#get the number of months of avialable data
    nummonths              = len(gwdata)
    numyears               = nummonths/12

# func call to generate the recharge factor    
    rechargetimes= fillrech(test_case,var,Pset,summer=6, winter=10, monsoon=None)
# max pumping with 50% less in monsoon and 100% in nonmonsoon season
    if pcase ==1:
        tm                      = (np.arange(1,13,1)) # monthly data
        Qp                      = np.array(sinefunc(tm,Qpmax,0.5*Qpmax))  # sine function
        #Qp                     = np.array([1,1,1,1,1,1,0.5,0.5,0.5,0.5,1,1])
        pumping                 = Qp*10**6  #*p
    if pcase==2:
        tm                      = (np.arange(1,13,1))
        Qp                      = np.array(linearfunc(tm,Qpmax,0.5*Qpmax)) 
        pumping                 = Qp*10**6  #*p
    if pcase ==3:
        tm                      = (np.arange(1,13,1))
        Qp                      = np.array(stepfunc(tm,Qpmax,0.5*Qpmax)) 
        pumping                 = Qp*10**6  #*p
    if pcase==4:
        tm                      = (np.arange(1,13,1))
        Qp                      = np.array(trapzfunc(tm,Qpmax)) 
        pumping                 = Qp*10**6  #*p
    
# repeat the data for the respective years
    pumptimes              = numpy.matlib.repmat(pumping,1,numyears)
    pumptimes              = pumptimes.reshape(nummonths)

#assign Constant and initial variables as an input to the model
    gwhead                 = np.zeros(nummonths) 
    gwhead[0]              = gwdata[0]            # initial head
    effectiveer            = model_variant(mv)    # converting millimeter to meter

# iteration of the model starts
    for m in range(1,nummonths):
        rh                 = (effectiveer[m]*rechargetimes[m])/Sy 
        ph                 = (pumptimes[m]/(Sy*area))
        lh                 = ((qin[m]-qout[m])/(Sy*area))
        gwhead[m]          = (gwhead[m-1] - rh + ph -lh)

# calculate the metrics
    rmse                   = rmse_metric(gwdata,gwhead) # minimize
    mae                    = mae_metric(gwdata,gwhead)  # minimize
    nse                    = -nse_metric(gwdata,gwhead) # maximize   
    return rmse,mae,nse,gwhead

# Calbration process for the model
def sim_mod(Pset,var,area,test_case,mv,pcase):
    choice_data= modelrun(Pset,var,area,test_case,mv,pcase)
    return choice_data[0], choice_data[1],choice_data[2]

