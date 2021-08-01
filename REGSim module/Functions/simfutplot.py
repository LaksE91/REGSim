# -*- coding: utf-8 -*-
"""
Created on Wed Jul 28 16:07:29 2021

@author: Laks
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

def multi_tsplot(df,time_axis,test_case,mv):
    
    f,ax                    = plt.subplots()
    
    # plot the pareto-front of the objective functions
    ###############################################################################
    lb1              = ax.plot(time_axis, df[0],'--',c='k',linewidth=2, label ='min-max bound')
    ub1              = ax.plot(time_axis, df[1],'--',c='k',linewidth=2)
    md1              = ax.plot(time_axis, df[2],'-',c='b',linewidth=2,label= 'Median')

    ax.margins(x=0)
    ax.invert_yaxis()
    ax.set_xticks(time_axis)
    ax.set_ylabel('GW head[m]',fontsize =20)
    ax.locator_params(tight=True, nbins=10)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=15,rotation='vertical')
    
    if test_case ==1:
        title = ' (a) Case {}: constant recharge factor'.format(test_case)
    if test_case ==2:
        title = ' (b) Case {}: two seasonal recharge factor'.format(test_case)
    if test_case ==3:
        title = ' (c) Case {}: three seasonal recharge factor'.format(test_case)

    ax.set_title(title,  fontsize=15)
    
    ax.legend(loc='best', numpoints=1, fontsize=12)  

    plt.tight_layout()
    plt.savefig(".\ Results\simheadmultifuture_case{}_modvar{}.png".format(test_case,mv),dpi=300,bbox_inches='tight')

    plt.show()

def tsplot(gwhead,xaxis,test_case,mv):
    
    fig,ax            = plt.subplots()#figsize=(9,6))
    ax.plot(xaxis, gwhead,'--*',c='r',markersize=10,markerfacecolor="None",label='Simulated head')

    #ax.margins(x=0)
    plt.gca().invert_yaxis()
    
    if test_case ==1:
        title = ' (a) Case {}: constant recharge factor'.format(test_case)
    if test_case ==2:
        title = ' (b) Case {}: two seasonal recharge factor'.format(test_case)
    if test_case ==3:
        title = ' (c) Case {}: three seasonal recharge factor'.format(test_case)
        
    ax.set_title(title, fontsize=15)
    ax.set_xticks(xaxis)
    ax.set_ylabel('GW head[m]',fontsize =20)
    plt.yticks(fontsize=15)
    ax.xaxis.set_major_locator(plt.MaxNLocator(12))
    ax.yaxis.set_major_locator(plt.MaxNLocator(7))
    plt.xticks(fontsize=15,rotation='vertical')
    #plt.gcf().autofmt_xdate()
    plt.legend(loc='best', numpoints=1, ncol =2,fontsize=12)
    plt.tight_layout()
    plt.savefig(".\ Results\simheadsinglefuture_case{}_mv{}.png".format(test_case,mv),dpi=600,bbox_inches='tight')
    plt.show()
    