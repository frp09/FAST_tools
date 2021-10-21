import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import pyFAST
import math
from pyFAST.input_output import FASTOutputFile

cwd = os.getcwd()
sys.path.append(cwd)
from CalculatePSD import calcPSD

#------------------------------------------------------------------------------
#   PSD PLOTTER
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

binary = True                                                                   #read binary file (requires FAST toolbox by NREL)
log = False                                                                     #semilog plot

# OFPath2=r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61_idle\Results'
# OFPath=r'D:\Wind\FLOATING\DLC6.X\IEA15MW_DLC61_idle\Results\onshore'

# OFPath2=r'D:\Wind\FLOATING\DLC1X\NREL5MW_DLC11\Results'
# OFPath=r'D:\Wind\FLOATING\DLC1X\NREL5MW_DLC11\Results\onshore'
OFPath2=r'D:\Wind\FLOATING\DLC1X\IEA15MW_DLC11\Results\onshore'
OFPath=r'D:\Wind\FLOATING\DLC1X\IEA15MW_DLC11\Results'

# OFPath2=r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC14\Results'
# OFPath=r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC14\Results\onshore_old'

# sensor = 'GenPwr_[kW]'
# sensor = 'Wind1VelX_[m/s]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'RootMxb1_[kN-m]'
# sensor = 'TipDxc1_[m]'
# sensor = 'TwrBsMyt_[kN-m]'
sensor = 'RtAeroMyh_[N-m]'
# sensor = 'RotSpeed_[rpm]'
# sensor = 'RtAeroFxh_[N]'
# sensor = 'RotThrust_[kN]'

# sensor = 'YawBrTDxt_[m]'
# sensor = 'TTDspFA_[m]'
# sensor = 'YawBrFxp_[kN]'
# sensor = 'NcIMUTAxs_[m/s^2]'

# sensor = 'GenSpeed_[rpm]'
# sensor = 'NacYaw_[deg]'
# sensor = 'PtfmSurge_[m]'
# sensor = 'PtfmYaw_[deg]'
# sensor = 'TwrBsFxt_[kN]'
# sensor = 'PtfmPitch_[deg]'

sensorlabel = sensor
#sensorlabel='$ T_X^{BT} $ (m)'  #'wind speed @ hub (m/s)' #'$ T_X^{BT} $ (m)'
xrng=[0,1]
yrng=[0,1]



# seed_to_compare = 'OF_ws11_ti0_ECD+r'
seed_to_compare = 's574'
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

sf1 = 1/(Channels_OF.loc[1, 'Time_[s]'] - Channels_OF.loc[0, 'Time_[s]'])
sf2 = 1/(Channels_OF2.loc[1, 'Time_[s]'] - Channels_OF2.loc[0, 'Time_[s]'])
noverlap = 0.5
nperseg1 = len(Channels_OF['Time_[s]'])
nperseg2 = len(Channels_OF2['Time_[s]'])

f1, PSD1 = calcPSD(Channels_OF[sensor], sf1, nperseg1, noverlap)
f2, PSD2 = calcPSD(Channels_OF2[sensor], sf2, nperseg2, noverlap)

fig1, ax1 = plt.subplots()

ax1.set_xlabel("Hz (-)")
ax1.set_ylabel(sensorlabel)

ax1.grid()

ax1.plot(f2, PSD2, label = "OF2", linewidth=2, color='b')
ax1.plot(f1, PSD1, label = "OF1", linewidth=2, color='r')

ax1.set_xlim(xrng)
# ax1.set_ylim(yrng)
# ax1.set_xticks([500,510,520,530,540,550])

# ax1.fill_between([0.3375, 0.45, 0.45, 0.3375, 0.3375], [10^-16,10^-16, 10, 10, 10^-16], alpha = 0.4)
# ax1.fill_between([0.23, 0.45, 0.45, 0.23, 0.23], [10^-16,10^-16, 10, 10, 10^-16], alpha=0.4)
ax1.legend(framealpha=1)
plt.tight_layout()

if log: 
    
    ax1.set_yscale('log') 

#uncomment to save figure
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'.jpg', dpi=300)
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'_HQ.tiff', dpi=600)