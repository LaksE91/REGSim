# -*- coding: utf-8 -*-
"""
Last edited on Tue May 28 15:38:37 2019

@author: Lakshmi
"""
import numpy as np
import numpy.matlib
import pandas as pd
from metrics import *

# defining class to create object with attributes lower and upper bound
class ChoiceData():
    def __init__(self,lb,ub):
        # you can put here some validation logic
        self.lower = lb
        self.upper = ub

# function defintion for GLUE simulation       
def sim_glue(test_case,data,calib,Psets,A,lb,ub,c,h_max,tb):
    
    #######################################################################################
    #create a dataframe for metrics
    inf_liklhd                      = pd.DataFrame()
    inf_liklhd["nse"]               = np.zeros_like(Psets.p)
    
    #Initalize inputs to the model
    ns                              = len(Psets)        # no of simulation
    nm                              = len(calib)        # no of months
    numyears                        = nm/12             # no of years
    h_int                           = np.zeros((nm,ns)) #Gw head 
    h_int[0,:]                      = calib.H[0]        # initial head
    effectiveer                     = calib.P/1000      # unit of rainfall mm to m
    
    if test_case==1:
        #case1 recharge rate is constant 
        r                           = Psets.r
        rechargeratio               = np.array([r,r,r,r,r,r,r,r,r,r,r,r]) #[0,0,0,0,0,1,1,1,1,1,0,0]

    if test_case==2:
        #case2 two recharge set, monsoon and non monsoon 
        r1                          = Psets.r11
        r2                          = Psets.r12
        rechargeratio               = np.array([r1,r1,r1,r1,r1,r1,r2,r2,r2,r2,r1,r1])

    if  test_case==3:
        #case3 three recharge set winter , summer and monsoon season
        r1                          = Psets.r21
        r2                          = Psets.r22
        r3                          = Psets.r23
        rechargeratio               = np.array([r1,r1,r2,r2,r2,r2,r3,r3,r3,r3,r1,r1])  
        
    # we assume max pumping with 50% less in monsoon and 100% in nonmonsoon season (unit MCM)
    pumping                         = np.array([1,1,1,1,1,1,0.5,0.5,0.5,0.5,1,1]) 
                 
    # repeat the data for the respective years
    pumptimes                       = numpy.matlib.repmat(pumping,1,numyears)
    pumptimes                       = pumptimes.reshape(nm)
    
    rechargetimes                   = np.zeros((nm,ns))
    for i in range(ns):
        rechargetimes[:,i]          = numpy.matlib.repmat(rechargeratio[:,i],1,numyears)
    
    ##### Calibration phase: identify behavioural parameter sets #####
    for i in range(ns):
        for j in range(nm-1):
            rh                      = (effectiveer[j+1]*rechargetimes[j+1,i])/(Psets.s[i])
            ph                      = (pumptimes[j+1]*Psets.p[i])/(Psets.s[i]*A)
            #lh                     = ((qin[m]-qout[m])/(Sy*A))
            h_int[j+1,i]            = (h_int[j,i] - (rh-ph))
    # calculate the metrics
        inf_liklhd.nse[i]           = nse_metric(calib.H,h_int[:,i])        

    # behavioural set
    cutoff                          = c   # assigning % ratio to identify the behavioural sets
    numBehav                        = cutoff*len(Psets)  

    if tb ==1:
        metrics                     = inf_liklhd.sort_values('nse', ascending=False)
        index                       = metrics.index.values 
        # defining the likelihood
        #index is the reference of the sorted of nse
        behav_index                 = index[0:int(numBehav)] 
        behav_rank                  = np.arange(numBehav,0,-1)
        behav_rank                  = behav_rank/1.0
        posterior                   = behav_rank / sum(behav_rank)  
        #here posterior = likelihood(nse) as it is uniform distirubution
        
    if tb ==2:
        numnonBehav                 = cutoff*len(Psets)  
        metrics                     = inf_liklhd.sort_values('nse', ascending=True)
        index                       = metrics.index.values 
        # defining the likelihood
        behav_index                 = index[0:int(numnonBehav)] #index is the reference of the sorted of nse
        nbehav_rank                 = np.arange(numnonBehav,0,-1)
        posterior                   = nbehav_rank / sum(nbehav_rank)

    if test_case==1:
        df_case1                    = pd.DataFrame()
        df_case1 ["p"]              = list(Psets.p[behav_index])
        df_case1 ["s"]              = list(Psets.s[behav_index])
        df_case1 ["r"]              = list(Psets.r[behav_index])
        db                          = df_case1 
    if test_case==2:
        df_case2                    = pd.DataFrame()
        df_case2["p"]               = list(Psets.p[behav_index])
        df_case2["s"]               = list(Psets.s[behav_index])
        df_case2["r1"]              = list(Psets.r11[behav_index])
        df_case2["r2"]              = list(Psets.r12[behav_index])
        db                          = df_case2
    if test_case==3:
        df_case3                    = pd.DataFrame()
        df_case3["p"]               = list(Psets.p[behav_index])
        df_case3["s"]               = list(Psets.s[behav_index])
        df_case3["r1"]              = list(Psets.r21[behav_index])
        df_case3["r2"]              = list(Psets.r22[behav_index])
        df_case3["r3"]              = list(Psets.r23[behav_index])
        db                          = df_case3
        
########## Validation phase: simulate model and get prediction limits ###############
    
    nsims                           = int(numBehav)  # no of simulation 
    nmon                            = len(data)       # no of months
    nyrs                            = nmon/12        # no of years
    gwhead_pred                     = np.zeros((nmon,nsims))
    gwhead_pred[0,:]                = data.H[0]       # initial head
    effrech                         = data.P/1000     # unit of rainfall from mm to m
    nse_val                         = np.zeros(nsims)
    
    # repeat the data for the respective years
    if test_case==1:
    #case1
        r                           = db.r
        rechargeratio1              = np.array([r,r,r,r,r,r,r,r,r,r,r,r])
    if test_case==2:
    #case2
        r1                          = db.r1
        r2                          = db.r2
        rechargeratio1              = np.array([r1,r1,r1,r1,r1,r1,r2,r2,r2,r2,r1,r1]) 
    if test_case==3:
     #case3
        r1                          = db.r1
        r2                          = db.r2
        r3                          = db.r3
        rechargeratio1              = np.array([r1,r1,r2,r2,r2,r2,r3,r3,r3,r3,r1,r1]) 
    
    rtimes                          = np.zeros((nmon,nsims))
    for i in range(nsims):
        rtimes[:,i]                 = np.matlib.repmat(rechargeratio1[:,i],1,nyrs)
    
    ptimes                          = np.matlib.repmat(pumping,1,nyrs)
    ptimes                          = ptimes.reshape(nmon)
      
    for ii in range(nsims):
        for jj in range(nmon-1):
            rh1                     = (effrech[jj+1]*rtimes[jj+1,ii])/(db.s[ii])
            ph1                     = (ptimes[jj+1]*db.p[ii])/(db.s[ii]*A)
            head_1                  = (gwhead_pred[jj,ii] - (rh1-ph1))
            if head_1 > h_max:
                gwhead_pred[jj+1,ii] = h_max
            elif head_1 < 0:
                gwhead_pred[jj+1,ii] = 0
            else:
                gwhead_pred[jj+1,ii] = head_1

    # calculate the metrics
        nse_val[ii]                 = nse_metric(data.H,gwhead_pred[:,ii])    
    
    lower = []
    upper = []

    # updating the likelihood at every time step
    for k in range(nmon):
        newgwhead                   = np.sort(gwhead_pred[k,:])
        indx                        = np.argsort(newgwhead)
        newpost                     = np.cumsum(posterior[indx])
    
        lower.append(np.interp(lb,newpost,newgwhead))
        upper.append(np.interp(ub,newpost,newgwhead))
    
    # creating the dataframe for behavioural dataset
    return lower,upper,db

def uncertain(test_case,data,calib,Psets,A,lb,ub,c,h_max,tb):
   Choice_data=sim_glue(test_case,data,calib,Psets,A,lb,ub,c,h_max,tb)
   return Choice_data[0], Choice_data[1]
