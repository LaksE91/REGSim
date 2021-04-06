# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 16:35:06 2019

@author: Lakshmi
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.dates as dates
import numpy as np


## Function for the optimal pareto front for each recharge scenario.
def paretoplot(df,test_case,mv,s=100):
        
    fig = plt.figure()
    ax  = fig.add_subplot(111, projection='3d')

    # plot the pareto-front of the objective functions
    ax.scatter(-df.NSE,df.MAE,df.RMSE,s=s,edgecolors='r',marker = '*',facecolors ='none')

    if test_case ==1:
        title = ' (a) Case {}: constant recharge factor'.format(test_case)
    if test_case ==2:
        title = ' (b) Case {}: two seasonal recharge factor'.format(test_case)
    if test_case ==3:
        title = ' (c) Case {}: three seasonal recharge factor'.format(test_case)

    ax.set_title(title,  fontsize=20)
    ax.set_xticklabels(-df.NSE,fontsize=15)
    ax.set_yticklabels(df.MAE,fontsize=15)
    ax.set_zticklabels(df.RMSE,fontsize=15)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.set_xlabel("NSE", fontsize =12,labelpad=10)
    ax.set_zlabel("RMSE", fontsize =12,labelpad=5,rotation=90)
    ax.set_ylabel("MAE", fontsize =12,labelpad=10)
    ax.locator_params(tight=True, nbins=3)

    plt.tight_layout()
    plt.savefig(".\ Results\paretoplot_case{}_modvar{}.png".format(test_case,mv),dpi=600,bbox_inches='tight')
    plt.show()


#function for validation plot between observed and simulated head
def valplot(gwdata,gwhead,xaxis,months,test_case,mv):
    
    fig,ax            = plt.subplots(figsize=(9,6))
    line1             = ax.plot(xaxis, gwhead,'--*',c='r',markersize=10,markerfacecolor="None",label='Simulated head')
    line2             = ax.plot(xaxis, gwdata,'o',markersize=8,markerfacecolor='k',markeredgecolor='none',label='Observed head')
    plt.axis([0, 60, 0.7*np.min(gwdata), 1.1*np.max(gwdata)])
    plt.axvline(x=48,linestyle='--',alpha= 0.4,c ='k')
    plt.text(24,7,'Calibration',fontsize =12)
    plt.text(50,7,'Validation',fontsize=12)
    ax.annotate('', xy=(1,7.1), xytext=(46,7.1),
            arrowprops={'arrowstyle': '<->'}, va='center')
    ax.annotate('', xy=(49,7.1), xytext=(60,7.1),
            arrowprops={'arrowstyle': '<->'}, va='center')  
    ax.margins(x=0)
    plt.gca().invert_yaxis()
    
    if test_case ==1:
        title = ' (a) Case {}: constant recharge factor'.format(test_case)
    if test_case ==2:
        title = ' (b) Case {}: two seasonal recharge factor'.format(test_case)
    if test_case ==3:
        title = ' (c) Case {}: three seasonal recharge factor'.format(test_case)
    
    
    ax.set_title(title, fontsize=20)
    ax.set_xticks(xaxis)
    ax.set_xticklabels(xaxis,fontsize=15)
    ax.set_xticklabels(months, rotation='vertical', fontsize=12)
    ax.set_ylabel('GW head[m]',fontsize =20)
    plt.yticks(fontsize=15)
    
    ax.xaxis.set_major_locator(plt.MaxNLocator(11))
    ax.yaxis.set_major_locator(plt.MaxNLocator(7))
    plt.xticks(fontsize=15,rotation='vertical')
    
    plt.legend(loc=4, numpoints=1, ncol =2,fontsize=16)
    plt.tight_layout()
    plt.savefig(".\ Results\simhead_nsga_case{}_modvar{}.png".format(test_case,mv),dpi=600,bbox_inches='tight')
    plt.show()
    
