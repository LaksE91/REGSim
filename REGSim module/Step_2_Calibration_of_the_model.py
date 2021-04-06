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
from Utils import *
from mkdir import addpath
addpath()  # creates the new directory to store the results

############## inputs and data management #############################################

#read the csv file  (input data)

filedir                 = 'C:\Users\Laks\Desktop\REGSim modified\Data'
filename                = 'sampledata.csv'
path                    = os.path.join(filedir,filename)
#read the csv file  (input data)
## Column 1 -Time ## Column 2 groundwater head## Column 3 rainfall
## Column 4- Potential evapotranspiration ##Column5&6 Lateral inflow and outflow
data                    = pd.read_csv(path,sep = ',',)
# sort the data for the model 
input_data              = sortinput(data)
# sepearte the data for calibration and validation period 
# data_sep(dataset,totalmonth_calibrationmonth)
[input_calib,input_valid]       = data_sep(input_data,60,48)

###########################################################################################
#Calibration of the model using NSGA2 optimization method
def nsga2(rech_case,pcase,indata,area,mv,M=3,V=None,sy=None,Qp=None,r1=None,r11=None,r12=None,r21=None,r22=None,r23=None):
    
    def gw_model(input_para):
        return sim_mod(input_para,indata,area,rech_case,mv,pcase)
            
    # main program run - NSGA2, this code runs for unconstrained condition
    
    # define the no if decision variables and objective functions
    problem                 = Problem(V, M)
    
    # define the decision variable
    x1                      = Real(sy[0],sy[1])
    x2                      = Real(Qp[0],Qp[1]) 
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
    nsim                = 10000#input('no. of iterations:')
    
    algorithm.run(nsim)
    
    #stores the results of NSGA2
    result              = algorithm.result
    
    #store results in dataframe
    df_opt = pd.DataFrame()
    
    if rech_case==1:
        df_opt["Sy"]    = [s.variables[0] for s in result]
        df_opt["Qp"]    = [s.variables[1] for s in result]
        df_opt["r"]     = [s.variables[2] for s in result]
    if rech_case==2:
        df_opt["Sy"]    = [s.variables[0] for s in result]
        df_opt["Qp"]    = [s.variables[1] for s in result]
        df_opt["r11"]   = [s.variables[2] for s in result]
        df_opt["r12"]   = [s.variables[3] for s in result]
    if rech_case==3:
        df_opt["Sy"]    = [s.variables[0] for s in result]
        df_opt["Qp"]    = [s.variables[1] for s in result]
        df_opt["r21"]   = [s.variables[2] for s in result]
        df_opt["r22"]   = [s.variables[3] for s in result]
        df_opt["r23"]   = [s.variables[4] for s in result]
    
    df_opt["RMSE"]      = [s.objectives[0] for s in result]
    df_opt["MAE"]       = [s.objectives[1] for s in result]
    df_opt["NSE"]       = [s.objectives[2] for s in result]
    
    # save the output into csv file
    df_opt.to_csv(".\ Results\paretofront_case{}.txt".format(rech_case), 
                  sep='\t',index=False, header=True, encoding='utf-8')
    #
    # ploting pareto optimal front for each case
    par_plt             = paretoplot(df_opt,rech_case,mv)
    print ('Optimization completed')
    
    return df_opt

# run the nsga 2 algorithm
    
#nsga2(rech_case,indata,area,mv,M=3,V=None,sy=None,Qp=None,r1=None,r11=None,r12=None,r21=None,r22=None,r23=None):
'''
rech_case - recharge factor case 
indata -  total input dataset
area - area of the study [sq.m]
mv-  model variant condition  M-  objective function, V- decision variable (3-for case-1,4 for case-2, 5 for case-3)
Qp- max pumping rate[MCM]  sy- specfic yield [-], r1- constant recharge for case-1
r11 - recharge factor for nonmonsoon for case-2 r12- recharge factor for monsoon for case-2
r21- recharge factor for summer for case-3 r22- recharge factor for winter for case-3, r23- recharge factor for nonmonsoon for case-3
'''
df_opt = nsga2(2,4,input_calib,5536407425,mv=1,V=4,sy=[0.001,0.16],Qp=[50,100],r11=[0.0,1],r12=[0.1,1]) 
#############end of the script#################################
