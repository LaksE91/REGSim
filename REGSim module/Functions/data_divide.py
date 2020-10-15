# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 14:13:03 2020

@author: Lakshmi
"""
import numpy as np
  
def data_sep(dt):

###################dataset for model#################################################
    # divide the data into calibration and validation period. 
    # the example dataset considered for 5 years, monthly data which contains rainfall,
    # groundwater head,lateral inflow and outflow. Hence we divide the data into 4 years 
    # or calibration and one year for validation for furture analysis
    
    ty_nom              =  input('total number of months considered:')
    ty_nomc             =  input('number of months considered for calibration:')
    
    try: 
        nom             = int(ty_nom)
        nomc            = int(ty_nomc)
    except:
        print("Please enter the number")
        
    cal_dat             = np.arange(nomc,nom,1)
    val_dat             = np.arange(0,nomc,1)
    
    indexes_to_keep     = set(range(dt.shape[0])) - set(cal_dat)
    calb                = dt.take(list(indexes_to_keep))
    
    indexes_to_keep1    = set(range(dt.shape[0])) - set(val_dat)
    vald                = dt.take(list(indexes_to_keep1))
    
    calib               = calb.reset_index(drop=True)
    
    vald                = vald.reset_index(drop=True)
    
    size = len(dt.columns)
    
    if size==2:
        val             = vald
    else:
        val             = vald.drop(['Qin','Qout'],axis =1)
    
    return calib, val

