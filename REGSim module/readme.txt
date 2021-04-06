###########################################################
#  REGSim -Open source tool in python used to simulate 	  #
#  groundwater head and identify the uncertainty of the	  #
#  parameter in the model				  #
#							  #
#  Author:Lakshmi Elangovan				  #
#  Version: V.0.2 					  #
#  Date: 3 April 2021					  #
###########################################################

##########################################################
1. Step_2_Calibration_of_the_model.py

#enter the directory of the input dataset (.csv)
filedir - enter the directory
filename - enter the filename of the dataset

# format for the dataset columns
## Column 1 -Time ## Column 2 groundwater head ## Column 3 rainfall
## Column 4- Potential evapotranspiration ##Column5&6 Lateral inflow and outflow
input_data- sortinput(data)

# sepearte the data for calibration and validation period 
# data_sep(dataset,totalmonth_calibrationmonth)

# function to call nsga2
# nsga2(rech_case,indata,area,mv,M=3,V=None,sy=None,Qp=None,r1=None,r11=None,r12=None,r21=None,r22=None,r23=None)

rech_case - recharge factor case 
indata -  total input dataset
area - area of the study [sq.m]
mv-  model variant condition  
M-  objective function, 
V- decision variable (3-for case-1,4 for case-2, 5 for case-3)
Qp- max pumping rate[MCM]  
sy- specfic yield [-], 
r1- constant recharge for case-1
r11 - recharge factor for nonmonsoon for case-2
r12- recharge factor for monsoon for case-2
r21- recharge factor for summer for case-3 
r22- recharge factor for winter for case-3, 
r23- recharge factor for nonmonsoon for case-3

#paretoplot(df_opt,rech_case,mv) - plot the pareto optimal front

############################################################################
Step_3_Validation_of_the_model.py

#input same as step_2

# function to call
valsim(rech_case,indat,area,mv,sy,Qp,r=None,r11=None,r12=None,r21=None,r22=None,r23=None)

# valplot(obsv_head,gwhead,tcount,months,1)- plot the validation GW head vs observed head
##########################################################################

Step_4a_Uncertanity_analysis.py

# dataset same as Step-2:

#LHS sample
rand(p,sy,r1,r11,r12,r21,r22,r23,nos,noi=8)
p   - maximum pumping range [min,max] # units Million Cubic meters
sy  - specific yield range [min,max] #unit percentage 
r1  - recharge case-1 range [min,max] #unit percentage   
r11 - recharge non-monsoon case-2 [min,max] #unit percentage
r12 - recharge monsoon case-2 [min,max] #unit percentage
r21 - recharge winter case-3 [min,max] #unit percentage
r22 - recharge summer case-3 [min,max] #unit percentage
r23 -  recharge monsoon case-3 [min,max] #unit percentage
area  - area of the study area boundary in m2 
#assign the input parameter ranges
noi         -no of input to generate random sampling
rech_case   - call the testcase index
noi         - number of paramters
nos         - no of sample
lb          - lower Confidence interval
ub          - upper Confidence interval
cutoff      - assign percentage of acceptable threshold
h_max       - possible maximum depth to water table(m)
mv 	    - model variant (0- P and 1 for P-PE)
Psets       - ransom sampled parameter set

# call the GLUE function to perform uncertainty analysis
#uncertain(rech_case,data,calib,Psets,area,lb,ub,c,h_max,mv,tb)

#############################################################################333
Step_4b_Sensitivity_analysis.py

# inputs are same as Step_4a
sim_glue(rech_case,data,calib,Psets,area,lb,ub,c,h_max,mv,tb)
# function to estimate the CDF
ecdf(sample)
# function to plot CDF
eplt(evar_p,evar_q,rech_case,mv)