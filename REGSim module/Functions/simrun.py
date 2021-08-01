# -*- coding: utf-8 -*-
"""
Created on Wed 28 Jul 2021

@author: Lakshmi
"""
import numpy as np
import numpy.matlib
import pandas as pd
from pumpfunc import *

def simrun(test_case,pcase,mv,data,Psets,A,int_H,hmax):
    
    #input variables and parameter sets
    pdata               = data.P
    pedata              = data.PE
    # Check the lateral flow inclusion
    try:
        qin             = np.array(data.Qin) # Lateral inflow
        qout            = np.array(data.Qin) # lateral outflow
    except:
        qin             = np.zeros(len(data.P))
        qout             = np.zeros(len(data.P)) 
        
    #get the number of months of avialable data
    nsims               = len(Psets)
    month               = 12
    nmon                = len(data)
    nyrs                = nmon/month

    ### Choice of model variant P or P-PE
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
    
########################### recharge and pumping condition######################
    # Recharge Scenario
    if test_case==3:
    # repeat the data for the respective years
        #case3
        r1                          = Psets.r21
        r2                          = Psets.r22
        r3                          = Psets.r23
        rechargeratio1              = np.array([r1,r1,r2,r2,r2,r2,r3,r3,r3,r3,r1,r1]) 
    if test_case==2:
        #case2
        r1                          = Psets.r11
        r2                          = Psets.r12
        rechargeratio1              = np.array([r1,r1,r1,r1,r1,r1,r2,r2,r2,r2,r1,r1])
    if test_case==1:
        #case1
        r                           = Psets.r
        rechargeratio1              = np.array([r,r,r,r,r,r,r,r,r,r,r,r])
    
    rtimes                          = np.zeros((nmon,nsims))
    for i in range(nsims):
        rtimes[:,i]                 = np.matlib.repmat(rechargeratio1[:,i],1,nyrs) 

    # Assign pumping parameter set
    Qpmax                           = Psets.p
    pumping                         = np.zeros((month,nsims))
    for i in range(nsims):
        
        if pcase ==1:
            tm                      = (np.arange(1,13,1)) # monthly data
            Qp                      = np.array(sinefunc(tm,Qpmax[i],0.5*Qpmax[i]))  # sine function
            pumping[:,i]            = Qp*10**6
        if pcase==2:
            tm                      = (np.arange(1,13,1))
            Qp                      = np.array(linearfunc(tm,Qpmax[i],0.5*Qpmax[i])) #linear function
            pumping[:,i]            = Qp*10**6
        if pcase ==3:
            tm                      = (np.arange(1,13,1))
            Qp                      = np.array(stepfunc(tm,Qpmax[i],0.5*Qpmax[i])) #binary function
            pumping[:,i]            = Qp*10**6
        if pcase==4:
            tm                      = (np.arange(1,13,1))
            Qp                      = np.array(trapzfunc(tm,Qpmax[i])) #trapezoidal function 
            pumping[:,i]            = Qp*10**6

    # repeat the data for the respective years
    ptimes                          = np.zeros((nmon,nsims))
    for i in range(nsims):
        ptimes[:,i]                 = np.matlib.repmat(pumping[:,i],1,nyrs) 
##############################################################################
    
    # Simulation of the groundwater model
    gwhead_pred                     = np.zeros((nmon,nsims))
    gwhead_pred[0,:]                = int_H      # initial head
    effrech                         = model_variant(mv)   # effective water available 
    # iteration starts
    for ii in range(nsims):
        for jj in range(nmon-1):
            rh1                     = (effrech[jj+1]*rtimes[jj+1,ii])/(Psets.s[ii])
            ph1                     = (ptimes[jj+1,ii])/(Psets.s[ii]*A)
            #lh                      = ((qin[jj+1]-qin[jj+1])/(Psets.s[ii]*A))
            head_1                  = (gwhead_pred[jj,ii] - (rh1-ph1))#+lh))
            if head_1 > hmax:
                gwhead_pred[jj+1,ii] =hmax
            elif head_1 < 0:
                gwhead_pred[jj+1,ii] = 0
            else:
                gwhead_pred[jj+1,ii] = head_1    
    
    return gwhead_pred
