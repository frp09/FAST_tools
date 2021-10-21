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
# windspeeds = [38]
# windspeeds = [47.5]
# windspeeds = [9,11,13]

sourcepaths = [#r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11\Results',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC11\Results',
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11\Results\onshore',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC11\Results\onshore']#,
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13\Results']#,
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13\Results',
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13\Results\onshore',
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13_onshore\Results']

# sourcepaths = [r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16\Results',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC16\Results']
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16_onshore\Results']#,
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC16_onshore\Results']

# sourcepaths = [#r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC14\Results',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC14\Results',
#                 r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC14\Results\onshore',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC14\Results\onshore',]

# sourcepaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61\Results',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61\Results',
#                 r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61\Results\onshore',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61\Results\onshore']

# sourcepaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63\Results',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_rigid\Results',
#                 r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63\Results\onshore',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_rigid\Results\onshore']

resultsPaths = [#r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC11\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11\Results\onshore\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC11\Results\onshore\Means&Stds']#,
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13\Results\Means&Stds']#,
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13\Results\onshore\Means&Stds',
                r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC13_onshore\Results\Means&Stds']

# resultsPaths = [r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC16\Results\Means&Stds']
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16_onshore\Results\Means&Stds']#,
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC16_onshore\Results\Means&Stds']

# resultsPaths = [#r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC14\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC14\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC14\Results\onshore\Means&Stds',
                # r'D:\Wind\FLOATING\DLC1.X\NREL5MW_DLC14\Results\onshore\Means&Stds']

# resultsPaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61\Results\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61\Results\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61\Results\onshore\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61\Results\onshore\Means&Stds']

# resultsPaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63\Results\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_rigid\Results\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63\Results\onshore\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_rigid\Results\onshore\Means&Stds']

# sourcepaths = ['D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11_onshore\Results',
#                # 'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13_onshore\Results',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16_onshore\Results',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11\Results',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13\Results',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16\Results']

# resultsPaths = ['D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11_onshore\Results\Means&Stds',
#                # 'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13_onshore\Results\Means&Stds',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16_onshore\Results\Means&Stds',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11\Results\Means&Stds',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC13\Results\Means&Stds',
#                'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16\Results\Means&Stds']


# sourcepaths = [r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_idle_rigid\Results',
                # r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_idle_rigid\Results\onshore']

# resultsPaths = [r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_idle_rigid\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC63_idle_rigid\Results\onshore\Means&Stds']

# sourcepaths = [r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61_idle\Results',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61_idle\Results\onshore']

# resultsPaths = [r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61_idle\Results\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61_idle\Results\onshore\Means&Stds']

# sourcepaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63_idle_rigid\Results',
                # r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63_idle_rigid\Results\onshore']

# resultsPaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63_idle_rigid\Results\Means&Stds',
                # r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC63_idle_rigid\Results\onshore\Means&Stds']

# sourcepaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61_idle_rigid\Results',
#                 r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61_idle_rigid\Results\onshore']

# resultsPaths = [r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61_idle_rigid\Results\Means&Stds',
#                 r'D:\Wind\FLOATING\DLC6.X\NREL5MW_DLC61_idle_rigid\Results\onshore\Means&Stds']
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