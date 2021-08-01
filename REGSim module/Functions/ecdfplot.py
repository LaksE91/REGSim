# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:14:33 2020

@author: Lakshmi
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick

#Function defintion for cummulative distribution function plot 
def eplt(evar_p,evar_q,test_case,mv):
    
    fig = plt.figure(figsize=(12,7))
    
    fig.text(-0.001, 0.78, 'Cumulative Distribution Function',fontsize =12, va='center', rotation='vertical')
    if test_case ==1:
        sp = 0.35
        title = ' (a) Case {}: constant recharge factor'.format(test_case)
    if test_case ==2:
        sp = 0.4
        title = ' (b) Case {}: two seasonal recharge factor'.format(test_case)
    if test_case == 3:
        sp = 0.5
        title = ' (c) Case {}: three seasonal recharge factor'.format(test_case)
        
    fig.text(sp, 0.95, title,fontsize =12, ha='center', rotation='horizontal')
     
    ax1 = fig.add_subplot(3, 5, 1)
    ax1.plot(evar_q[0], evar_p[0], c='grey',  alpha=0.4,linewidth=10,label='all parameter set')
    ax1.plot(evar_q[1], evar_p[1], '-b', linewidth=5, label='behavioural set')
    ax1.plot(evar_q[2], evar_p[2], '--r', linewidth=5, label='non-behavioural set')
    ax1.set_xlabel('Pumping',fontsize =12)    
    ax1.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True)) 

    ax1.tick_params(axis='both', which='major', labelsize=15)
    
    ax2 = fig.add_subplot(3, 5, 2,sharey =ax1)
    ax2.plot(evar_q[3], evar_p[3],  c='grey',  alpha=0.4,linewidth=10,label='totalsample_set')
    ax2.plot(evar_q[4], evar_p[4], '-b', linewidth=5, label='behavioural set')
    ax2.plot(evar_q[5], evar_p[5], '--r', linewidth=5, label='non-behavioural set')
    ax2.set_xlabel('Specific Yield',fontsize =12)
    ax2.tick_params(axis='both', which='major', labelsize=15)
        
    if test_case==1:
        ax3 = fig.add_subplot(3, 5, 3,sharey=ax1)
        ax3.plot(evar_q[6], evar_p[6],  c='grey',  alpha=0.4,linewidth=10,label='totalsample_set')
        ax3.plot(evar_q[7], evar_p[7], 'b', linewidth=5, label='behaviouralset')
        ax3.plot(evar_q[8], evar_p[8], '--r', linewidth=5, label='non-behavioural set')
        ax3.set_xlabel('Recharge factor',fontsize =12)
        ax3.tick_params(axis='both', which='major', labelsize=15)
        box_spx = 0.35
        
    if test_case==2:
        ax6 = fig.add_subplot(3, 5, 3, sharey=ax1)
        ax6.plot(evar_q[6], evar_p[6],  c='grey',  alpha=0.4,linewidth=10,label='totalsample_set')
        ax6.plot(evar_q[7], evar_p[7], '-b', linewidth=5, label='behavioural set')
        ax6.plot(evar_q[8], evar_p[8], '--r', linewidth=5, label='non-behavioural set')
        ax6.set_xlabel('Recharge factor(nonmonsoon)',fontsize =12)
        ax6.tick_params(axis='both', which='major', labelsize=15)
        
        ax7 = fig.add_subplot(3, 5, 4, sharey=ax1)
        ax7.plot(evar_q[9], evar_p[9],  c='grey',  alpha=0.4,linewidth=10,label='totalsample_set')
        ax7.plot(evar_q[10], evar_p[10], '-b', linewidth=5, label='behavioural set')
        ax7.plot(evar_q[11], evar_p[11], '--r', linewidth=5, label='non-behavioural set')
        ax7.set_xlabel('Recharge factor(monsoon)',fontsize =12)
        ax7.tick_params(axis='both', which='major', labelsize=15)
        box_spx = 0.4
    
    if test_case==3:
        ax10 =fig.add_subplot(3, 5,3, sharey=ax1)
        ax10.plot(evar_q[6], evar_p[6],  c='grey',  alpha=0.4,linewidth=10,label='totalsample_set')
        ax10.plot(evar_q[7], evar_p[7], '-b', linewidth=5, label='behavioural set')
        ax10.plot(evar_q[8], evar_p[8], '--r', linewidth=5, label='non-behavioural set')
        ax10.set_xlabel('Recharge factor(winter)',fontsize =12)
        ax10.tick_params(axis='both', which='major', labelsize=15)
        
        ax11 = fig.add_subplot(3, 5, 4, sharey=ax1)
        ax11.plot(evar_q[9], evar_p[9],  c='grey',  alpha=0.4,linewidth=10,label='Prior distribution')
        ax11.plot(evar_q[10], evar_p[10], '-b', linewidth=5, label='behavioural set')
        ax11.plot(evar_q[11], evar_p[11], '--r', linewidth=5, label='non-behavioural set')
        ax11.set_xlabel('Recharge factor(summer)',fontsize =12)
        ax11.tick_params(axis='both', which='major', labelsize=15)
        
        ax12 = fig.add_subplot(3, 5, 5, sharey=ax1)
        ax12.plot(evar_q[12], evar_p[12],  c='grey',  alpha=0.4,linewidth=10,label='totalsample_set')
        ax12.plot(evar_q[13], evar_p[13], '-b', linewidth=5, label='behavioural set')
        ax12.plot(evar_q[14], evar_p[14], '--r', linewidth=5, label='non-behavioural set')
        ax12.set_xlabel('Recharge factor(monsoon)',fontsize =12)
        ax12.tick_params(axis='both', which='major', labelsize=15) 
        box_spx = 0.4
        
    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels,loc='lower center',ncol=3, fontsize=10,bbox_to_anchor=(box_spx, 0.27),borderaxespad=0.)

    plt.tight_layout()
    plt.subplots_adjust(left=0.1,top=0.9,bottom=0.1,wspace=0.6,hspace = 0.6)
    fig.savefig('.\ Results\ecdf_subplots_case_{}_modvar{}.png'.format(test_case,mv), dpi=300, bbox_inches='tight')
    plt.show()
    #end of the script
    
