###########################################################################
### Uncertainty analysis using GLUE method                              ###
### Author : Lakshmi E                                                  ###
### Last Edit: 25 March 2021                                            ###
###########################################################################

import pandas as pd
import numpy as np
import sys
import os
dirpath = os.getcwd()
sys.path.insert(0, ".\Functions")
from Utils import sortinput
from data_divide import data_sep
from LHS_sample import rand
from Gluerun import sim_glue, uncertain
from glueplot import myglueplot
from percent_available import obsv_inside

#Uncertanity analysis GLUE and plotting the prediction interval
############# inputs and data management #############################################

filedir                 = 'C:\Users\Laks\Desktop\REGSim-main\REGSim module\Data' # enter the user directory
filename                = 'sampledata.csv' # enter the filename of the input file 
path                    = os.path.join(filedir,filename)
#read the csv file  (input data)
data                    = pd.read_csv(path,sep = ',',)
## Column 1 -Time ## Column 2 groundwater head## Column 3 rainfall
## Column 4- Potential evapotranspiration ##Column5&6 Lateral inflow and outflow
input_data              = sortinput(data)
# sepearte the data for calibration and validation period 
# data_sep(dataset,totalmonth_calibrationmonth)
[input_calib,input_valid] = data_sep(input_data,60,48)

# assign the range of input parameters
#rand(p,sy,r1,r11,r12,r21,r22,r23,nos,noi=8)
'''
p   - maximum pumping range [min,max] # units Million Cubic meters
sy  - specific yield range [min,max] #unit percentage 
r1  - recharge case-1 range [min,max] #unit percentage   
r11 - recharge non-monsoon case-2 [min,max] #unit percentage
r12 - recharge monsoon case-2 [min,max] #unit percentage
r21 - recharge winter case-3 [min,max] #unit percentage
r22 - recharge summer case-3 [min,max] #unit percentage
r23 -  recharge monsoon case-3 [min,max] #unit percentage
area  - area of the study area boundary in m2 #5536407425 
#assign the input parameter ranges
#noi           = no of input to generate random sampling
rech_case      =    # call the testcase index
noi            = 8
nos            = no of sample
'''
# simulation of uniform LHS sample set
samp_set                    = rand([50,350],[0.001,0.05],[0.1,0.6],[0,1],[0,1],[0,1],[0,1],[0,1],1000)   
#########input parameters to the model
lb                          = 0.05#input('lower Confidence interval:' )
ub                          = 0.95#input('upper Confidence interval:' )
cutoff                      = 0.1#input('assign percentage of acceptable threshold:' )
h_max                       = 30#input('possible maximum depth to water table(m):')
area                        = 5536407425 # sq.m
mv                          = 0 # model variant (P and P-PE)
pcase                       = 3
rech_case                   = 1 # recharge factor scenario
# call the glue function to estimate the lower and upper prediction interval
[lowerbound, upperbound,behavpara] = sim_glue(rech_case,pcase,input_data,input_calib,samp_set,area,lb,ub,cutoff,h_max,mv,1)
# call the glue function to estimate prediction interval for total sample set
# cutoff we are considering the total sample set
[lower_total, upper_total] = uncertain(rech_case,pcase,input_data,input_calib,samp_set,area,0,1,1,h_max,mv,1)

### displaying the results by plotting
# input variables for plotting
CI_bounds                   = pd.DataFrame()
CI_bounds ["lb"]            = lowerbound
CI_bounds ["ub"]            = upperbound
CI_bounds ["lf"]            = lower_total
CI_bounds ["uf"]            = upper_total
CI_bounds ["H"]             = input_data.H

# save the behavourial parameter set in csv
behavpara.to_csv('behaviouralpara_case{}_mv{}.csv'.format(rech_case,mv))
########################################Ploting##########################

month                       = ['01/2004','06/2004','01/2005','06/2005','12/2005','05/2006',
                               '11/2006','06/2007','12/2007','05/2008','12/2008']#,'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
tcount                      = np.arange(1,61,1) # total time period considered for simulation
sim_plt                     = myglueplot(CI_bounds,rech_case,mv,month,tcount)

percent_value               = round(obsv_inside(CI_bounds))

print ('Percentage of observation within the confidence interval:'
       + str(percent_value) + '%')

##########################end of  the script ##########################################################
