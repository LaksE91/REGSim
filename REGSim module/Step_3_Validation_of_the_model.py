###########################################################################
### Validation of the conceptual groundwater model                      ###
### Author : Lakshmi E                                                  ###
### Last Edit: 25-March-2021                                            ###
###########################################################################

import pandas as pd
import numpy as np

import sys,os
dirpath = os.getcwd()
sys.path.insert(0, ".\Functions")

#import user defined functions
from modelcalb_nsga2 import *
from visualplot import *
from Utils import *

############## inputs and data management #####################################################

#read the csv file  (input data)

filedir                 = 'C:\Users\Laks\Desktop\REGSim modified\Data'
filename                = 'sampledata.csv'
path                    = os.path.join(filedir,filename)
#read the csv file  (input data)
data                    = pd.read_csv(path,sep = ',',)
## Column 1 -Time ## Column 2 groundwater head## Column 3 rainfall
## Column 4- Potential evapotranspiration ##Column5&6 Lateral inflow and outflow
input_data              = sortinput(data)

#Validation of the model based on the pareto front and comparing with the observed GWhead

def valsim(rech_case,pcase,indat,area,mv,sy,Qp,r=None,r11=None,r12=None,r21=None,r22=None,r23=None):
    
    #simulated data with observed groundwater head
    if rech_case==1:
        optimal_set             = [sy,Qp,r]
        [rmse,mae,nse,gwhead]   = modelrun(optimal_set,indat,area,rech_case,mv,pcase)
        
    if rech_case==2:
        optimal_set             = [sy,Qp,r11,r12]
        [rmse,mae,nse,gwhead]   = modelrun(optimal_set,input_data,area,rech_case,mv,pcase)
    
    if rech_case==3:
        optimal_set             = [sy,Qp,r21,r22,r23]
        [rmse,mae,nse,gwhead]   = modelrun(optimal_set,input_data,area,rech_case,mv,pcase)
    
       
    return rmse,mae,-nse,gwhead

# call validation function 
#valsim(rech_case,indat,area,mv,sy,Qp,r=None,r11=None,r12=None,r21=None,r22=None,r23=None):
'''
rech_case - recharge factor case 
indata -  total input dataset
area - area of the study [sq.m]
mv-  model variant condition  M-  objective function, V- decision variable (3-for case-1,4 for case-2, 5 for case-3)
Qp- max pumping rate[MCM]  sy- specfic yield [-], r1- constant recharge for case-1
r11 - recharge factor for nonmonsoon for case-2 r12- recharge factor for monsoon for case-2
r21- recharge factor for summer for case-3 r22- recharge factor for winter for case-3, r23- recharge factor for nonmonsoon for case-3
'''  
# user update  this example for sample dataset
[rmse,mae,nse,gwhead] = valsim(2,4,input_data,5536407425,1,0.02,83,r11=0.25,r12=0.34)
################ Plotting#####################################################
obsv_head                   = input_data.H  
months                      = ['01/2004','06/2004','01/2005','06/2005','12/2005',
                               '05/2006','11/2006','06/2007','12/2007','05/2008',
                               '12/2008']

tcount                      = np.arange(1,61,1) # number of months to plot
rech_case                   = 2 # recharge factor  case
mv                          = 0 # model variant P or P-PE
val_plt                     = valplot(obsv_head,gwhead,tcount,months,rech_case,mv)

##########################################################################
