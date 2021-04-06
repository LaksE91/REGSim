# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 10:50:15 2021

@author: Laks
"""

import pandas as pd
import numpy as np


## Column 1:  Time period ## Column 2: Groundwater head ## Column 3: Rainfall
## Column 4: Evapotranspiration ## Column 5: Lateral inflow ## Column 6: Lateral outflow
class invar:
    def __init__(self,var):
        self.Time = var.iloc[:,0].values 
        self.H = var.iloc[:,1].values
        self.P = var.iloc[:,2].values
        self.PE = var.iloc[:,3].values
        if len(var.columns)>4:
            self.Qin = var.iloc[:,4].values
            self.Qout = var.iloc[:,5].values
            self.all = [self.Time,self.H,self.P,self.PE,self.Qin,self.Qout]
        else:
            self.all = [self.Time,self.H,self.P,self.PE]
    
    def availvar(self):
        indat = self.all
        return indat
######################################################################### 
def sortinput(data):    
    callinput = invar(data)
    finp = callinput.availvar()
    
    inputdata = pd.DataFrame()
    
    inputdata['Date']   = pd.to_datetime(finp[0], format = '%d-%m-%Y')
    inputdata['H']      = finp[1]
    inputdata['P']      = finp[2]
    inputdata['PE']     = finp[3]
    try: 
        inputdata['Qin']    = finp[4]
        inputdata['Qout']   = finp[5]
    except:
        print (' Lateral flow is the not the input variable')
        
    inputdata['day'] = inputdata['Date'].dt.day
    inputdata['month'] = inputdata['Date'].dt.month
    inputdata['year'] = inputdata['Date'].dt.year  
    
    return inputdata

#### fill the rechagre factor for respective time scale
def fillrech(test_case,calibd,Pset,summer=None, winter=None, monsoon=None):
    numdat = len(calibd)
    r = []
    for i in range(0,numdat):
        if (test_case==1):
            r.append(float(Pset[2]))
        if (test_case==2):
            r.append(float(Pset[2]) if (calibd.month[i] <= summer and calibd.month[i]>=winter) else float(Pset[3]))
        if (test_case == 3):
            r[i] = float(Pset[2]) if (calibd.month[i] <= summer) else float(Pset[3]) if(calibd.month[i]>=winter) else float(Pset[4])
    return r
