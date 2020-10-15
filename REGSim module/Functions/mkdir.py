# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:53:11 2020

@author: Lakshmi
"""

import os  
    
def addpath():
    # working current directory 
    
    dirpath = os.getcwd()
 
    path_new = dirpath +'\ Results'
    
# Create the directory  
 
    try:  
        os.mkdir(path_new)  
    except OSError as error:  
        print(error)  