import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import pyFAST
import math
from pyFAST.input_output import FASTOutputFile

#------------------------------------------------------------------------------
#   TIMESERIES PLOTTER
#
#   description:    *plotter selects file in a folder given by the user that
#                   contains "seed_to_compare" in the file name. Make sure
#                   that a results file is being loaded
#
#   usage:          #OFPath2 = path to folder containing second file
                    #OFPath = path to containing first file
                    #sensor = sensor to plot
                    #sensorlabel = label to display on plot
                    #xrng,yrng = x and y ranges
                    #seed_to_compare = keyword to select file to compare
                    #binary = select if data is in binary format (if it is set path to read_FAST_binary correctly)
#
#   author:         Francesco Papi
#
#   date:           09/2020
#
#   warnings:       **********************************************************
#------------------------------------------------------------------------------

#---------- USER PARAMETERS ---------------------------------------------------

# OFPath=r'D:\Wind\FLOATING\DLC1X\IEA15MW_DLC11\Results'
# OFPath2=r'D:\Wind\FLOATING\DLC1X\IEA15MW_DLC11\Results\onshore'
OFPath=r'G:\Drive condivisi\MsC Menchetti\OpenFAST\OpenFAST_Setup\EPS_6.6882_GF_0.5'
OFPath2=r'G:\Drive condivisi\MsC Menchetti\OpenFAST\OpenFAST_Setup\EPS_6.6882_GF_0.5'

sensor='GenPwr_[kW]'
# sensor = 'Wind1VelY_[m/s]'
# sensor = 'RootMxb1_[kN-m]'
# sensor = 'TipDxc1_[m]'
# sensor = 'RotSpeed_[rpm]'
# sensor = 'NacYaw_[deg]'
# sensor = 'PtfmSurge_[m]'
# sensor = 'PtfmPitch_[deg]'
# sensor = 'PtfmYaw_[deg]'
# sensor = 'TTDspSS_[m]'
# sensor = 'YawBrMyp_[kN-m]'
# sensor = 'YawBrFxp_[kN]'
# sensor = 'TwrBsMyt_[kN-m]'
# sensor = 'TwrBsFxt_[kN]'
# sensor = 'TipDxc1_[m]'
# sensor = 'Wind1AngXY_[NVALI]'
# sensor = 'PtfmRoll_[deg]'
# sensor = 'NcIMUTAxs_[m/s^2]'
# sensor = 'YawBrTDxt_[m]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'B1N8Cd_[-]'
# sensor = 'RtTSR_[-]'
# sensor = 'GenTq_[kN-m]'

sensorlabel = sensor
#sensorlabel='$ T_X^{BT} $ (m)'  #'wind speed @ hub (m/s)' #'$ T_X^{BT} $ (m)'
# xrng=[500,550]
# yrng=[0,15]

binary = True

seed_to_compare = 'ws5_ti0_flex.out'

#------------------------------------------------------------------------------


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
    Channels_OF2 = pd.read_table(OFfile2, skiprows=6, skipinitialspace=True)
    Channels_OF = pd.read_table(OFfile, skiprows=6, skipinitialspace=True)
    Channels_OF.columns = Channels_OF.columns.str.replace(' ', '')
    Channels_OF2.columns = Channels_OF2.columns.str.replace(' ', '')
    Channels_OF=Channels_OF.drop(labels=0)
    Channels_OF2=Channels_OF2.drop(labels=0)
    Channels_OF=Channels_OF.astype(float)
    Channels_OF2=Channels_OF2.astype(float)

fig1, ax1 = plt.subplots()

ax1.set_xlabel("t (s)")
ax1.set_ylabel(sensorlabel)

ax1.grid()

ax1.plot(Channels_OF2['Time_[s]'], Channels_OF2[sensor], label = "OF2", linewidth=2, color='b')
ax1.plot(Channels_OF['Time_[s]'], Channels_OF[sensor], label = "OF1", linewidth=2, color='r')
# ax1.set_xlim(xrng)
# ax1.set_ylim(yrng)
# ax1.set_xticks([500,510,520,530,540,550])


ax1.legend(framealpha=1)
plt.tight_layout()

#uncomment to save figure
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'.jpg', dpi=300)
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'_HQ.tiff', dpi=600)