###########################################################################
### Uncertainty analysis using GLUE method                              ###
### Author : Lakshmi E                                                  ###
### Last Edit: 13-April-2020                                            ###
###########################################################################

import pandas as pd
import sys,os

#path    = os.chdir(input("give the current directory:"))#r"G:\CE15RESCH11013_LAKSHMI\Code\GWM\Code_process_instruct")
dirpath = os.getcwd()
sys.path.insert(0, ".\Functions")

from data_divide import data_sep
from LHS_sample import rand
from Gluerun import sim_glue, uncertain
from glueplot import myglueplot
from percent_available import obsv_inside

#Uncertanity analysis GLUE and plotting the prediction interval

#read the csv file  (input data)
input_data                  = pd.read_csv(".\Data\sampledata.csv", header=0)

[input_calib,input_vald]    = data_sep(input_data)

# assign the range of input parameters

p                           = input('maximum pumping range [min,max]:' ) # units Million Cubic meters
sy                          = input('specific yield range [min,max]:' ) #unit percentage 
r1                          = input('recharge case-1 range [min,max]:' ) #unit percentage   
r11                         = input('recharge non-monsoon case-2 [min,max]:' ) #unit percentage
r12                         = input('recharge monsoon case-2 [min,max]:' ) #unit percentage
r21                         = input('recharge winter case-3 [min,max]:' ) #unit percentage
r22                         = input('recharge summer case-3 [min,max]:' ) #unit percentage
r23                         = input('recharge monsoon case-3 [min,max]:' ) #unit percentage
area                        = input(' area of the study area boundary in m2 :' )#5536407425 

#assign the input parameter ranges
#noi                         = input('no of input to generate random sampling:' )
rech_case                   = input('Test case: ')    # call the testcase index
noi                         = 8
nos                         = input('no of sample:' )

# simulation of uniform LHS sample set
samp_set                    = rand(noi,nos,p,sy,r1,r11,r12,r21,r22,r23)   

lb                          = input('lower Confidence interval:' )
ub                          = input('upper Confidence interval:' )
cutoff                      = input('assign percentage of acceptable threshold:' )
h_max                       = input('possible maximum depth to water table(m):')

# call the glue function to estimate the lower and upper prediction interval
[lowerbound, upperbound]    = uncertain(rech_case,input_data,input_calib,samp_set,
                                        area,lb,ub,cutoff,h_max,1)
# call the glue function to estimate prediction interval for total sample set
# cutoff we are considering the total sample set
[lower_total, upper_total]  = uncertain(rech_case,input_data,input_calib,samp_set, 
                                        area,0,1,1,h_max,1)

### displaying the results by plotting
# input variables for plotting
CI_bounds                   = pd.DataFrame()
CI_bounds ["lb"]            = lowerbound
CI_bounds ["ub"]            = upperbound
CI_bounds ["lf"]            = lower_total
CI_bounds ["uf"]            = upper_total
CI_bounds ["H"]             = input_data.H

sim_plt                     = myglueplot(CI_bounds,rech_case)

percent_value               = round(obsv_inside(CI_bounds))

print ('Percentage of observation within the confidence interval:'
       + str(percent_value) + '%')

##########################end of  the script ##########################################################
