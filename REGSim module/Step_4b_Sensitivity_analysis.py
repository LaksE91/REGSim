###########################################################################
### Sensitivity analaysis using Cumulative distribution function        ###
### Author : Lakshmi E                                                  ###
### Last Edit: 25-March-2021                                            ###
###########################################################################

import os
import numpy as np
import pandas as pd

# working current directory 
dirpath = os.getcwd()
import sys
sys.path.insert(0, ".\Functions")

#import the user defined functions 
from data_divide import data_sep
from Gluerun import sim_glue, uncertain
from ecdfplot import eplt
from Utils import *


###################dataset for model#################################################
#read the csv file  (input data)

df_Psets                    = pd.read_csv("random_lhs.csv", header = 0) 
filedir                     = 'C:\Users\Laks\Desktop\REGSim-main2\REGSim module\Data' # update wiith user directory
filename                    = 'sampledata.csv' # user's input dataset filname
path                        = os.path.join(filedir,filename)
#read the csv file  (input data)
data                        = pd.read_csv(path,sep = ',',)
## Column 1 -Time ## Column 2 groundwater head## Column 3 rainfall
## Column 4- Potential evapotranspiration ##Column5&6 Lateral inflow and outflow
input_data                  = sortinput(data)
# sepearte the data for calibration and validation period 
# data_sep(dataset,totalmonth_calibrationmonth)
[input_calib,input_valid]   = data_sep(input_data,60,48)

###########################Simulation of the model##############################
rech_case                 = 1                # call the testcase index
lb                        = 0.05            #= input('lower Confidence interval:' )
ub                        = 0.95            # = input('upper Confidence interval:' )
cutoff1                   = 0.1             #input('assign percentage of acceptable threshold:' )
cutoff2                   = 1- cutoff1      #input('assign percentage of unacceptable threshold:' )
h_max                     = 30              #input('possible maximum depth to water table(m):')
area                      = 5536407425       # input(' area of the study area boundary in m2 :' )#5536407425 
mv                        = 1  # model variant
####### behavioural set######
[lb,ub,df_behav]                 = sim_glue(rech_case,data,input_calib,df_Psets,area,lb,ub,cutoff1,h_max,1,1)
######## non-behavioural set#####
[lb,ub,df_nbehav]                = sim_glue(rech_case,data,input_calib,df_Psets,area,lb,ub,cutoff2,h_max,1,2)

###########################plotting##################################################

def ecdf(sample):

    # convert sample to a numpy array, if it isn't already
    sample = np.atleast_1d(sample)

    # find the unique values and their corresponding counts
    quantiles, counts = np.unique(sample, return_counts=True)

    # take the cumulative sum of the counts and divide by the sample size to
    # get the cumulative probabilities between 0 and 1
    cumprob = np.cumsum(counts).astype(np.double) / sample.size

    return quantiles, cumprob

# compute the ECDF of the samples

p1 = df_Psets.p
p2 = df_behav.p
p3 = df_nbehav.p

s1 = df_Psets.s
s2 = df_behav.s
s3 = df_nbehav.s

qep1, pep1 = ecdf(p1) 
qep2, pep2 = ecdf(p2) 
qep3, pep3 = ecdf(p3)

qes1, pes1 = ecdf(s1) 
qes2, pes2 = ecdf(s2) 
qes3, pes3 = ecdf(s3)

if rech_case ==1: 
    r1 = df_Psets.r
    r2 = df_behav.r
    r3 = df_nbehav.r
    
    qer1, per1 = ecdf(r1) 
    qer2, per2 = ecdf(r2) 
    qer3, per3 = ecdf(r3)

    evar_q = [qep1,qep2,qep3,qes1,qes2,qes3,qer1,qer2,qer3]
    evar_p = [pep1,pep2,pep3,pes1,pes2,pes3,per1,per2,per3]
    
if rech_case ==2:
    r1_11 = df_Psets.r11
    r2_11 = df_behav.r1
    r3_11 = df_nbehav.r1

    qer1_11, per1_11 = ecdf(r1_11) 
    qer2_11, per2_11 = ecdf(r2_11) 
    qer3_11, per3_11 = ecdf(r3_11)
    
    r1_12 = df_Psets.r12
    r2_12 = df_behav.r2
    r3_12 = df_nbehav.r2
    
    qer1_12, per1_12 = ecdf(r1_12) 
    qer2_12, per2_12 = ecdf(r2_12) 
    qer3_12, per3_12 = ecdf(r3_12)
    
    evar_q = [qep1,qep2,qep3,qes1,qes2,qes3,qer1_11,qer2_11,qer3_11,qer1_12,qer2_12,qer3_12]
    evar_p = [pep1,pep2,pep3,pes1,pes2,pes3,per1_11,per2_11,per3_11,per1_12,per2_12,per3_12]
    
if rech_case==3:
    r1_21 = df_Psets.r21
    r2_21 = df_behav.r1
    r3_21 = df_nbehav.r1
    
    qer1_21, per1_21 = ecdf(r1_21) 
    qer2_21, per2_21 = ecdf(r2_21) 
    qer3_21, per3_21 = ecdf(r3_21)

    r1_22 = df_Psets.r22
    r2_22 = df_behav.r2
    r3_22 = df_nbehav.r2

    qer1_22, per1_22 = ecdf(r1_22) 
    qer2_22, per2_22 = ecdf(r2_22) 
    qer3_22, per3_22 = ecdf(r3_22)
    
    r1_23 = df_Psets.r23
    r2_23 = df_behav.r3
    r3_23 = df_nbehav.r3
    
    qer1_23, per1_23 = ecdf(r1_23) 
    qer2_23, per2_23 = ecdf(r2_23) 
    qer3_23, per3_23 = ecdf(r3_23)
    
    evar_q = [qep1,qep2,qep3,qes1,qes2,qes3,qer1_21,qer2_21,qer3_21,qer1_22,qer2_22,qer3_22,qer1_23,qer2_23,qer3_23]
    evar_p = [pep1,pep2,pep3,pes1,pes2,pes3,per1_21,per2_21,per3_21,per1_22,per2_22,per3_22,per1_23,per2_23,per3_23]

senplot = eplt(evar_p,evar_q,rech_case,mv)

print ('CDF plot are generated')
# end of the script
