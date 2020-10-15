###########################################################################
### Validation of the conceptual groundwater model                      ###
### Author : Lakshmi E                                                  ###
### Last Edit: 13-April-2020                                            ###
###########################################################################

import pandas as pd
import numpy as np

import sys,os
dirpath = os.getcwd()
sys.path.insert(0, ".\Functions")

#import user defined functions
from modelcalb_nsga2 import *
from visualplot import *

#read the csv file  (input data)
input_data                  = pd.read_csv(".\Data\sampledata.csv", header=0)
area                        = input(' area of the study area boundary in m2 :' )  

#Validation of the model based on the pareto front and comparing the 
rech_case                   = input('Test case: ')  # recharge factor case 1 or2 or 3

#simulated data with observed groundwater head
if rech_case==1:
    x1                      = input('Optimal specific yield :' )
    x2                      = input('Optimal pumping rate :' )
    x3                      = input('Optimal recharge rate :' )
    optimal_set             = [x1,x2,x3]
    [rmse,mae,nse,gwhead]   = modelrun(optimal_set,input_data,area,rech_case)
    
if rech_case==2:
    x1                      = input('Optimal specific yield :' )
    x2                      = input('Optimal pumping rate :' )
    x3                      = input('Optimal recharge rate nonmonsoon :' )
    x4                      = input('Optimal recharge rate monsoon :' )
    optimal_set             = [x1,x2,x3,x4]
    [rmse,mae,nse,gwhead]   = modelrun(optimal_set,input_data,area,rech_case)

if rech_case==3:
    x1                      = input('Optimal specific yield :' )
    x2                      = input('Optimal pumping rate :' )
    x3                      = input('Optimal recharge rate winter :' )
    x4                      = input('Optimal recharge rate summer :' )
    x5                      = input('Optimal recharge rate monsoon :' )
    optimal_set             = [x1,x2,x3,x4,x5]
    [rmse,mae,nse,gwhead]   = modelrun(optimal_set,input_data,area,rech_case)

################ Plotting#####################################################
obsv_head                   = input_data.H  
months                      = ['01/2004','06/2004','01/2005','06/2005','12/2005',
                               '05/2006','11/2006','06/2007','12/2007','05/2008',
                               '12/2008']

tcount                      = np.arange(1,61,1)

val_plt                     = valplot(obsv_head,gwhead,tcount,months,rech_case)

################################################################################