# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 13:55:20 2020

@author: Laks
"""

import pandas as pd
import numpy as np
from numpy import arange, sin, pi, cos
import matplotlib.pyplot as plt

def sinefunc(t,pmax,pmin,phi=0):
    P_rang  = [pmin,pmax] 
    c       = np.mean(P_rang)  # midline
    A       = float(pmax- c)  # amplitude 
    T       = len(t)
    sinp    = []
    
    for i in t:
        sinp.append(A*sin((((2*pi*i)/T)+phi)) +c) 
    return sinp
              
def linearfunc(t,pmax,pmin):
    linf = []
    
    m    = float((pmax-pmin))/(pmin)# slope MCM
    c    =  pmin*1.5#slope MCM#
    
    for ii in range(1,len(t[:6])):
        linf.append(m*ii + c)
    
    for jj in range(1,len(t[:5])):
        linf.append(-m*jj+c)
    
    for kk in range(1,len(t[:4])):
        linf.append(m*kk+c)
        
    return np.array(linf)

def stepfunc(t,pmax,pmin):
    stp  = []

    for k in t:
        if(k<=6 or k>10):
            stp.append(pmax)
        if(k>6 and k<11):
            stp.append(pmin)
    return stp

def trapzfunc(t,pmax,width=1., slope=1.): 
    trp = []
    for x in t:       
        if (x <= 2*width):
            # Ascending line
            trp.append(width*0.5)
        elif (x <= 3.*width):
            # Top horizontal line
            trp.append(width*slope)
        elif (x <= 5.*width):
            # Descending line
            trp.append(width*slope)
        elif (x <= 6*width):
            # Bottom horizontal line
            trp.append(width*slope*0.5)
        elif(x<=10*width):
            trp.append(0.2)
        elif(x<=12*width):
            trp.append(width*0.5)

    return np.array(trp)* pmax
