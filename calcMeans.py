# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 11:40:06 2023

@author: Francesco Papi
"""

import os
import pandas as pd
import glob
import sys
import matplotlib.pyplot as plt
import numpy as np
import pyFAST
from pyFAST.input_output import FASTOutputFile
import math

sys.path.append('C:\\Users\\Papi\\Desktop')
from FASTAverageCalculator import *

#------------------------------------------------------------------------------
#   FAST OUTPUT MEAN CALCULATOR
#
#   description:    script calculates average, std, max and min of user-defined
#                   values for FAST outputs with same WS
#
#   usage:          the file quantities needed are defined in "user values"
#
#   author:         Francesco Papi
#
#   date:           Jul 2021
#
#   warnings:       Make sure len(sourcepaths)=len(resultsPaths)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#-------------------------- USER VALUES ---------------------------------------    


windspeeds=[4,6,8,10,12,14,16,18,20,22,24]

sourcepaths = [
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13\Results',
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13_onshore\Results'
                ]


resultsPaths = [
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13\Results\Means&Stds',
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13_onshore\Results\Means&Stds'
                ]


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
    
# dictionaries to store results
means={}
stds={}
units={}
maxs={}
mins={}

ref_means={}
ref_stds={}
ref_units={}
ref_maxs={}
ref_mins={}
ref_abs_max={}

means_plus={}
stds_plus={}
units_plus={}
maxs_plus={}
mins_plus={}

maximum_values=[]
temp=[]

windspeeds=np.array(windspeeds)

#calculate dataframe with per-ws average of all quantities in FAST results
#one dataframe per sourcepath

for k,sourcepath in enumerate(sourcepaths):
    
    readPath=sourcepath
    writePath=resultsPaths[k]
    
    files = glob.glob(readPath+'\*.outb')
    tmp = FASTOutputFile(files[0]).toDataFrame()
    sensors = tmp.columns
    
    ref_means[readPath], ref_stds[readPath], ref_units[readPath], ref_maxs[readPath], ref_mins[readPath], ref_abs_max[readPath]=averageCalculator(readPath, windspeeds, sensors)
    
    averageWriter(ref_means[readPath], ref_units[readPath], writePath, 'Means.txt')
    averageWriter(ref_stds[readPath], ref_units[readPath], writePath, 'Stds.txt') 
    averageWriter(ref_maxs[readPath], ref_units[readPath], writePath, 'Maximums.txt') 
    averageWriter(ref_mins[readPath], ref_units[readPath], writePath, 'Minimums.txt')
    averageWriter(ref_abs_max[readPath], ref_units[readPath], writePath, 'Absolute_Maximums.txt')
Footer
© 2023 GitHub, Inc.
Footer navigation
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
