import matplotlib.pyplot as plt
import sys
import os
import pandas as pd

import openfast_toolbox
from openfast_toolbox.io import FASTOutputFile

'''
#------------------------------------------------------------------------------
#   TIMESERIES PLOTTER
#
#   description:    *plotter selects file in a folder given by the user that
#                   contains "seed_to_compare" in the file name. Make sure
#                   that a results file is being loaded
#
#   usage:          #OFPath2 = path to folder containing second file
                    #OFPath = path to containing first file
                    #seed_to_compare = keyword to select file to compare
                    #sensors = sensors along span to plot
                    #sensorlabel = label to display on plot
                    #binary = select if data is in binary format (if it is set path to read_FAST_binary correctly)
                    #span = span location of the nodes
#
#   author:         Francesco Papi
#
#   date:           09/2020
#
#   warnings:       "openFtast toolbox" IS REQUIRED:
                    https://github.com/OpenFAST/openfast_toolbox
#------------------------------------------------------------------------------
'''

#---------- USER PARAMETERS ---------------------------------------------------

OFPath2=r'path to folder cointaining first file to compare'
OFPath=r'path to folder cointaining second file to compare'

seed_to_compare = 'pattern in name of files to compare'

#sensors=['B1N1AxInd_[-]', 'B1N2AxInd_[-]', 'B1N3AxInd_[-]', 'B1N4AxInd_[-]', 'B1N5AxInd_[-]', 'B1N6AxInd_[-]', 'B1N7AxInd_[-]', 'B1N8AxInd_[-]', 'B1N9AxInd_[-]']
#sensors=['B1N1Alpha_[deg]', 'B1N2Alpha_[deg]', 'B1N3Alpha_[deg]', 'B1N4Alpha_[deg]', 'B1N5Alpha_[deg]', 'B1N6Alpha_[deg]', 'B1N7Alpha_[deg]', 'B1N8Alpha_[deg]', 'B1N9Alpha_[deg]']
sensors=['B1N1Fy_[N/m]', 'B1N2Fy_[N/m]', 'B1N3Fy_[N/m]', 'B1N4Fy_[N/m]', 'B1N5Fy_[N/m]', 'B1N6Fy_[N/m]', 'B1N7Fy_[N/m]', 'B1N8Fy_[N/m]', 'B1N9Fy_[N/m]']
#sensors=['B1N1Re_[-]', 'B1N2Re_[-]', 'B1N3Re_[-]', 'B1N4Re_[-]', 'B1N5Re_[-]', 'B1N6Re_[-]', 'B1N7Re_[-]', 'B1N8Re_[-]', 'B1N9Re_[-]']
#sensors=['B1N1Cl_[-]', 'B1N2Cl_[-]', 'B1N3Cl_[-]', 'B1N4Cl_[-]', 'B1N5Cl_[-]', 'B1N6Cl_[-]', 'B1N7Cl_[-]', 'B1N8Cl_[-]', 'B1N9Cl_[-]']
#sensors=['B1N1Cd_[-]', 'B1N2Cd_[-]', 'B1N3Cd_[-]', 'B1N4Cd_[-]', 'B1N5Cd_[-]', 'B1N6Cd_[-]', 'B1N7Cd_[-]', 'B1N8Cd_[-]', 'B1N9Cd_[-]']


span=[0.30059, 0.38379, 0.46581, 0.54530,	0.62105, 7.58E-01,	8.72E-01,	9.62E-01,	1.03E+00]

sensorlabel='$ T_X^{BT} $ (m)'  #'wind speed @ hub (m/s)' #'$ T_X^{BT} $ (m)'

binary = True



#------------------------------------------------------------------------------

#import ReadFASTBinary
sys.path.append("D:\\Python_Scripts")
from ReadFASTBinary import *

for file in os.listdir(OFPath2):
    if seed_to_compare in file and '.out' in file:
        OFfile2='\\'.join([OFPath2, file])
        
for file in os.listdir(OFPath):
    if seed_to_compare in file and '.out' in file:
        OFfile='\\'.join([OFPath, file])

if binary:
    
    Channels_OF2 = FASTOutputFile(OFfile2).toDataFrame()
    Channels_OF = FASTOutputFile(OFfile).toDataFrame()
    
else:
    #read ASCII data
    Channels_OF2 = pd.read_table(OFfile2, skiprows=6, skipinitialspace=True)
    Channels_OF = pd.read_table(OFfile, skiprows=6, skipinitialspace=True)
    
    #remove white spaces in column headers
    Channels_OF.columns = Channels_OF.columns.str.replace(' ', '')
    Channels_OF2.columns = Channels_OF2.columns.str.replace(' ', '')
    
    #drop lines with units
    Channels_OF=Channels_OF.drop(labels=0)
    Channels_OF2=Channels_OF2.drop(labels=0)
    
    #convert the datatype to float
    Channels_OF=Channels_OF.astype(float)
    Channels_OF2=Channels_OF2.astype(float)

fig1, ax1 = plt.subplots()

ax1.set_xlabel("span (m)")
ax1.set_ylabel(sensorlabel)
ax1.grid()


# create a list with mean spanwise quantities
# to select last value instead of mean: "Channels_OF2[sensor].iloc[-1]"
spanLoad_OF = []
spanLoad_OF2 = []

for sensor in sensors:
    spanLoad_OF.append(Channels_OF[sensor].mean())
    spanLoad_OF2.append(Channels_OF2[sensor].mean())

ax1.plot(span, spanLoad_OF2, label = "OF2", linewidth=1, color='b', marker = '.')
ax1.plot(span, spanLoad_OF, label = "OF1", linewidth=1, color='r', marker = '.')


ax1.legend(framealpha=1)
plt.tight_layout()

#uncomment to save figure
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'.jpg', dpi=300)
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'_HQ.tiff', dpi=600)