###########################################################################
### Calibration of the conceptual groundwater model using NSGA-II       ###
### Author : Lakshmi E                                                  ###
### Last Edit: 07 Jul 2020                                              ###
###########################################################################

from platypus import NSGAII, Problem, Real
import pandas as pd
import os, sys

dirpath = os.getcwd()
sys.path.insert(0, ".\Functions")

#import the user defined functions
from modelcalb_nsga2 import *
from visualplot import *
from data_divide import data_sep
from mkdir import addpath
addpath()  # creates the new directory to store the results

############## inputs and data management #####################################################

#read the csv file  (input data)
input_data                      = pd.read_csv(".\Data\sampledata.csv")

[input_calib,input_valid]       = data_sep(input_data)

# assign the range of input parameters
rech_case               = input('Test case: ')                  # call the testcase index
p                       = input('maximum pumping range [min,max]:' ) # units Million Cubic meters
sy                      = input('specific yield range [min,max]:' ) #unit percentage 

if rech_case==1:
    r1                  = input('recharge case-1 range [min,max]:' ) #unit percentage 
if rech_case==2:
    r11                 = input('recharge non-monsoon case-2 [min,max]:' ) #unit percentage
    r12                 = input('recharge monsoon case-2 [min,max]:' ) #unit percentage
if rech_case==3:
    r21                 = input('recharge winter case-3 [min,max]:' ) #unit percentage
    r22                 = input('recharge summer case-3 [min,max]:' ) #unit percentage
    r23                 = input('recharge monsoon case-3 [min,max]:' ) #unit percentage

area                    = input('area of the study area boundary in m2 :' ) # area in m2, eg. 5536407425  

###########################################################################################
#Calibration of the model using NSGA2 optimization method

def gw_model(input_para):
    return sim_mod(input_para,input_calib,area,rech_case)
        
# main program run - NSGA2, this code runs for unconstrained condition
V                       = input('no of decision variables: ')   # no of decision variables
M                       = input('no of objective functions: ')  #no of objective functio

# define the no if decision variables and objective functions
problem                 = Problem(V, M)


# define the decision variable
x1                      = Real(sy[0],sy[1])
x2                      = Real(p[0],p[1]) 
if rech_case==1:   
    x3                  = Real(r1[0],r1[1])
    input_para          = [x1,x2,x3]
if rech_case==2:
    x3                  = Real(r11[0],r11[1])
    x4                  = Real(r12[0],r12[1])
    input_para          = [x1,x2,x3,x4]
if rech_case==3:
    x3                  = Real(r21[0],r21[1]) 
    x4                  = Real(r22[0],r22[1]) 
    x5                  = Real(r23[0],r23[1])
    input_para          = [x1,x2,x3,x4,x5]

# define the problem definition
problem.types[:]    = input_para
problem.function    = gw_model

# instantiate the optimization algorithm
algorithm           = NSGAII(problem)#, population_size=500)

# optimize the problem using function evaluations
nsim                = input('no. of iterations:')
algorithm.run(nsim)

#stores the results of NSGA2
result              = algorithm.result

feasible_solutions  = [s for s in algorithm.result if s.feasible]

for solution in algorithm.result:
    print solution.variables
   
#store results in dataframe
df_opt = pd.DataFrame()

if rech_case==1:
    df_opt["Sy"]    = [s.variables[0] for s in algorithm.result]
    df_opt["Qp"]    = [s.variables[1] for s in algorithm.result]
    df_opt["r"]     = [s.variables[2] for s in algorithm.result]
if rech_case==2:
    df_opt["Sy"]    = [s.variables[0] for s in algorithm.result]
    df_opt["Qp"]    = [s.variables[1] for s in algorithm.result]
    df_opt["r11"]   = [s.variables[2] for s in algorithm.result]
    df_opt["r12"]   = [s.variables[3] for s in algorithm.result]
if rech_case==3:
    df_opt["Sy"]    = [s.variables[0] for s in algorithm.result]
    df_opt["Qp"]    = [s.variables[1] for s in algorithm.result]
    df_opt["r21"]   = [s.variables[2] for s in algorithm.result]
    df_opt["r22"]   = [s.variables[3] for s in algorithm.result]
    df_opt["r23"]   = [s.variables[4] for s in algorithm.result]

df_opt["RMSE"]      = [s.objectives[0] for s in algorithm.result]
df_opt["MAE"]       = [s.objectives[1] for s in algorithm.result]
df_opt["NSE"]       = [s.objectives[2] for s in algorithm.result]

# save the output into csv file
df_opt.to_csv(".\ Results\paretofront_case{}.txt".format(rech_case), 
              sep='\t',index=False, header=True, encoding='utf-8')

# ploting pareto optimal front for each case
par_plt             = paretoplot(df_opt,rech_case)

print ('Optimization completed')
##############################end of the script#################################
