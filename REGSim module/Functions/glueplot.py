# -*- coding: utf-8 -*-
"""
Created on Tue May 28 21:14:04 2019

@author: Lakshmi
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches


def myglueplot(df,test_case,mv,month,time_axis):
    
    def get_handle_lists(l):
        """returns a list of lists of handles.
        """
        tree = l._legend_box.get_children()[1]
    
        for column in tree.get_children():
            for row in column.get_children():
                yield row.get_children()[0].get_children()
   
    f,ax                    = plt.subplots()
   
    # plot the pareto-front of the objective functions
    ###############################################################################

    ci1              = ax.fill_between(time_axis,df.lf,df.uf,alpha=0.4, facecolor='grey')
    lb1              = ax.plot(time_axis, df.lb,'--',c='k',linewidth=2)
    ub1              = ax.plot(time_axis, df.ub,'--',c='k',linewidth=2)
    du11             = ax.scatter(time_axis[:48], df.H[:48], color='r',marker='*',s=50)
    du21             = ax.scatter(time_axis[49:], df.H[49:], color='r',marker='P',s=50)
    ax.axvline(x=48,linestyle='--',alpha= 0.4,c ='k')
    cd_int = input('Confidence_interval considered:')
    ax.text(2,3,'- - -  {}% Confidence interval'.format(cd_int),fontsize =10)
    ax.text(6,5,' Prior distribution',fontsize =10)
    # Create a Rectangle patch
    rect1 = patches.Rectangle((1.5,4),4,1,linewidth=1,edgecolor='grey',facecolor='grey',alpha=0.4)
    # Add the patch to the Axes
    ax.add_patch(rect1)
    ax.text(24,23,'Calibration',fontsize =10)
    ax.text(50,23,'Validation',fontsize=10)
    ax.annotate('', xy=(1,23.5), xytext=(46,23.5),
                arrowprops={'arrowstyle': '<->'}, va='center')
    ax.annotate('', xy=(49,23.5), xytext=(60,23.5),
                arrowprops={'arrowstyle': '<->'}, va='center')
    ax.margins(x=0)
    ax.invert_yaxis()
    ax.set_xticks(time_axis)
    ax.set_xticklabels(time_axis,fontsize=12)
    ax.set_xticklabels(month, rotation='vertical', fontsize=12)
    ax.set_ylabel('GW head[m]',fontsize =15)
    ax.locator_params(tight=True, nbins=10)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    
    if test_case ==1:
        title = ' (a) Case {}: constant recharge factor'.format(test_case)
    if test_case ==2:
        title = ' (b) Case {}: two seasonal recharge factor'.format(test_case)
    if test_case ==3:
        title = ' (c) Case {}: three seasonal recharge factor'.format(test_case)

    ax.set_title(title,  fontsize=15)
    
    ax.legend(loc=2, numpoints=1, fontsize=12)
    l1 = ax.legend( [(du11, du21)], ['Observed_head'],loc=2,scatterpoints=2, fontsize=10, frameon =False)
    
    
    handles_list1 = list(get_handle_lists(l1))
    handles1 = handles_list1[0] # handles is a list of two PathCollection.
                              # The first one is for red star, and the second
                              # is for red plus.
    handles1[0].set_facecolors(["red", "none"]) # for the fist
                       # PathCollection, make the
                       # second marker invisible by
                       # setting their facecolor and
                       # edgecolor to "none."
    handles1[0].set_edgecolors(["red", "none"])
    handles1[1].set_facecolors(["none", "red"])
    handles1[1].set_edgecolors(["none", "red"])

    plt.tight_layout()
    plt.savefig(".\ Results\glueplot_case{}_modvar{}.png".format(test_case,mv),dpi=300,bbox_inches='tight')

    plt.show()
