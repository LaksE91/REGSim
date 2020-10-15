# -*- coding: utf-8 -*-
"""
Created on Mon May 27 16:32:25 2019

@author: Lakshmi

"""
#This script performs the Latin hyper cube sampling of input paramters for groundwater model

import pandas as pd
from pyDOE import lhs
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick

def rand(noi,nos,p,sy,r1,r11,r12,r21,r22,r23):
    
    lhs_samp = lhs(noi,samples=nos)
    pump                    = lhs_samp[:,0] * (p[1]-p[0]) + p[0]        # max pumping 
    spec_yield              = lhs_samp[:,1] * (sy[1]-sy[0]) + sy[0]     # specific yield
    rech                    = lhs_samp[:,2] * (r1[1]-r1[0]) + r1[0]     #  case1: recharge factor constant for all months
    rech_nonmon             = lhs_samp[:,3] * (r11[1]-r11[0]) + r11[0]  # case2: r1-recharge factor constant for Non-monsoon months
    rech_mon1               = lhs_samp[:,4] * (r12[1]-r12[0]) + r12[0]  # case2: r2-recharge factor constant for Monsoon months
    rech_win                = lhs_samp[:,5] * (r21[1]-r21[0]) + r21[0]  # case3: r1-recharge factor constant for Wet Non-monsoon months
    rech_sum                = lhs_samp[:,6] * (r22[1]-r22[0]) + r22[0]  # case3: r2-recharge factor constant for Hot Non-monsoon months
    rech_mon2               = lhs_samp[:,7] * (r23[1]-r23[0]) + r23[0]  # case3: r3-recharge factor constant for Monsoon months

    # save the variables in csv
    sample                = pd.DataFrame()
    sample["p"]           = pump
    sample["s"]           = spec_yield
    sample["r"]           = rech 
    sample["r11"]         = rech_nonmon
    sample["r12"]         = rech_mon1
    sample["r21"]         = rech_win
    sample["r22"]         = rech_sum
    sample["r23"]         = rech_mon2
    
    header = ["p","s", "r", "r11","r12","r21","r22","r23"]
    sample.to_csv("random_lhs.csv", index= False, columns = header)
    print ('Random distribution generation completed')
    
    #histogram to view the distribution of the input parameters 
    f, ((ax1,ax2,ax3,ax4),(ax5,ax6,ax7,ax8)) = plt.subplots(2, 4, figsize =(12,6))

    count1              = ax1.hist(spec_yield,color = 'blue', edgecolor = 'black', normed=True)
    count2              = ax2.hist(pump,color = 'blue', edgecolor = 'black', normed=True)
    count3              = ax3.hist(rech,color = 'blue', edgecolor = 'black', normed=True)
    count4              = ax4.hist(rech_nonmon,color = 'blue', edgecolor = 'black', normed=True)
    count5              = ax5.hist(rech_mon1,color = 'blue', edgecolor = 'black', normed=True)
    count6              = ax6.hist(rech_win,color = 'blue', edgecolor = 'black', normed=True)
    count7              = ax7.hist(rech_sum,color = 'blue', edgecolor = 'black', normed=True)
    count8              = ax8.hist(rech_mon2,color = 'blue', edgecolor = 'black', normed=True)
    
    ax1.set_xlabel('specific storage',fontsize =12)
    ax1.set_ylabel('count',fontsize =12)
    
    ax2.set_xlabel('Pumping',fontsize = 12)
    ax2.set_ylabel('count',fontsize =12)
    ax2.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True)) 
    ax2.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True)) 

    
    ax3.set_xlabel('r',fontsize = 12)
    ax3.set_ylabel('count',fontsize =12)
    
    ax4.set_xlabel('r11',fontsize = 12)
    ax4.set_ylabel('count',fontsize =12)
    
    ax5.set_xlabel('r12',fontsize = 12)
    ax5.set_ylabel('count',fontsize =12)
    
    ax6.set_xlabel('r21',fontsize = 12)
    ax6.set_ylabel('count',fontsize =12)
    
    ax7.set_xlabel('r22',fontsize = 12)
    ax7.set_ylabel('count',fontsize =12)
    
    ax8.set_xlabel('r23',fontsize = 12)
    ax8.set_ylabel('count',fontsize =12)
    
    plt.tight_layout()
    plt.show()
    
    print ('Histogram complete')
    return sample






