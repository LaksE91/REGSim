###########################################################################
### Simulation mode for the validation of groudnwater model (future)    ###
### Author : Lakshmi E                                                  ###
### Last Edit: 29-Jul-2021                                              ###
###########################################################################

import pandas as pd
import numpy as np
import sys
import os
dirpath = os.getcwd()
sys.path.insert(0, ".\Functions")
#import user defined functions
from simrun import simrun
from simfutplot import tsplot,multi_tsplot
import matplotlib.dates as mdates
#read the csv file  (input data)
filedir                 = 'C:\Users\Laks\Desktop\REGSim-main\REGSim module\Data'
filename                = 'sampledataforfuture.csv'
path                    = os.path.join(filedir,filename)
inputdata               = pd.read_csv(path,sep = ',',)

# read the parameter set
# Single parameter set
fn1                     = 'singlepara.csv'
path1                   = os.path.join(filedir,fn1)
spara                   = pd.read_csv(path1,sep = ',',)
# Multiple parameter set
fn2                     = 'behaviouralpara_case1_mv0.csv'
path2                   = os.path.join(filedir,fn2)
mpara                   = pd.read_csv(path2,sep = ',',)

################# Call user defined function
rech_case               = 1  # recharge case
pcase                   = 3  # pumping scenario
mv                      = 0  # model variant 0-> P ; 1-> (P-PE)
area                    = 5536407425 # area of the study area m2
intH                    = 12 # inital groundwater head 
hmax                    = 30 # maximum groudwater head 
nmon                    = len(inputdata)

# simulation  for single parameter set
gwpred_single           = simrun(rech_case, pcase, mv, inputdata, spara, area, intH, hmax)

# simulation for multiple parameter set
gwpred_multi            = simrun(rech_case, pcase, mv, inputdata, mpara, area, intH, hmax)
# estimating the lower, upper and median gwhead predication
lower                   = []
upper                   = []
med                     = []
for i in range(nmon):
    gwheadnew           = np.sort(gwpred_multi[i, :])
    lower.append(np.min(gwheadnew))
    upper.append(np.max(gwheadnew))
    med.append(np.median(gwheadnew))

bound = [lower, upper, med]


###########Plotting ##################################
tcount                  = inputdata.Time
gwhead_singlets         = tsplot(gwpred_single, tcount, rech_case, mv)
gwhead_multits          = multi_tsplot(bound, tcount, rech_case, mv)

# end of the script




