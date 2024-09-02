import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import openfast_toolbox
import math
import numpy as np
from openfast_toolbox.io import FASTOutputFile

#------------------------------------------------------------------------------
#   TIMESERIES PLOTTER
#
#   description:    *plotter selects file in a folder given by the user that
#                   contains "seed_to_compare" in the file name. Make sure
#                   that a results file is being loaded
#
#   usage:          #path = list of paths to file folders
                    #sensor = sensor to plot
                    #sensorlabel = label to display on plot
                    #xrng,yrng = x and y ranges
                    #seed_to_compare = list of keywords to select files to compare
                    #binary = select if data is in binary format (if it is set path to read_FAST_binary correctly)
#
#   author:         Francesco Papi
#
#   date:           09/2020
#
#   warnings:       **********************************************************
#------------------------------------------------------------------------------

#---------- USER PARAMETERS ---------------------------------------------------


paths = [
            r'D:\Wind\FLOATING\FLOATECH\OC4\DLC62\Results',
            r'D:\Wind\FLOATING\FLOATECH\OC4\DLC12\Results',
            r'D:\Wind\FLOATING\FLOATECH\OC4\DLC61\Results',
            r'D:\Wind\FLOATING\FLOATECH\OC4\DLC16\Results',
            ]

seed_to_compare = [
                    'OF_5MWOC4_LC62_s10003_ws36_hs16_tp18_mis30_i0_y90', 
                    'OF_5MWOC4_LC12_s200_ws17_hs3_tp12_mis-30_i0_y10', 
                    'OF_5MWOC4_LC61_s10000_ws36_hs16_tp18_mis30_i0_y10', 
                    'OF_5MWOC4_LC16_s1067_ws19_hs10_tp16_mis0_i0_y0', 
                   ]

labels = [
           'LC 62', 
           'LC 12', 
           'LC 61', 
           'LC 16', 
          ]


binary = True
# saveFig = False

colors = ['r', 'b', 'black', 'green']
linestyle = ['-','-', '-', '-']

# %%4
# labels = ['old', 'new', 'other']
# colors = ['black', 'red', 'green', 'brown', 'green']

# binary = True

# paths = [
#     r'G:\Il mio Drive\WIP\Task30\01_Model_Data\AD\LLFVW_OLAF\LCs\OLD\SteadyAero\LC 2.27_steady',
#     r'G:\Il mio Drive\WIP\Task30\01_Model_Data\AD\LLFVW_OLAF\LCs\SteadyAero\LC 2.27_steady',
#     # r'G:\Il mio Drive\WIP\Task30\01_Model_Data\AD\BEM_steady\IEA_Task30_III_AeroDyn_LC2X',
#     r'G:\Il mio Drive\WIP\Task30\01_Model_Data\AD\DBEM_OfficialTaskResults\results_LC2X'
#     ]

sensor = 'RtAeroFxh_[N]'
# sensor = 'RtAeroMxh_[N-m]'
# sensor = 'RotSpeed_[rpm]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'TipDyc1_[m]'
# sensor = 'GenPwr'
# sensor = 'DBEMTau1_[s]'
# sensor = 'YawBrTAxp_[m/s^2]'
# sensor = 'Wind1VelX_[m/s]'
# sensor = 'Wave1Elev_[m]'
# sensor = 'TipDxc1_[m]'

# sensor = 'B1N3Cl_[-]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'PtfmSurge_[m]'
# sensor = 'PtfmRoll_[deg]'
# sensor = 'GenPwr_[kW]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'GenTq_[kN-m]'


# time = 'B1N3Alpha_[deg]'
time = 'Time_[s]'
# # time = 'Azimuth_[deg]'
# time = 'RotSpeed_[rpm]'

# seed_to_compare = ['LC227', 'LC227', 'LC227']

sensorlabel = sensor
# # sensorlabel='$ T_X^{BT} $ (m)'  #'wind speed @ hub (m/s)' #'$ T_X^{BT} $ (m)'

# # xrng=[500,550]
# # yrng=[0,15]

#------------------------------------------------------------------------------

OFfiles = [] 
for ii,path in enumerate(paths): 
    
    for file in os.listdir(path):
        if seed_to_compare[ii] in file and '.out' in file:
            OFfiles.append('\\'.join([path, file]))
            print('processing ', file)


data = {}
for OFfile in OFfiles:
    
    if binary:
        data[OFfile] = FASTOutputFile(OFfile).toDataFrame()

    else:
        data[OFfile] = pd.read_table(OFfile, skiprows=6, skipinitialspace=True)
        data[OFfile].columns = data[OFfile].columns.str.replace(' ', '')
        data[OFfile]=data[OFfile].drop(labels=0)
        data[OFfile]=data[OFfile].astype(float)
        
        


fig1, ax1 = plt.subplots()

ax1.set_xlabel("t (s)")
ax1.set_ylabel(sensorlabel)

ax1.grid()

for i,OFfile in enumerate(OFfiles): 
    
    ax1.plot(data[OFfile][time], data[OFfile][sensor], label = labels[i], linewidth=2, color=colors[i], linestyle = linestyle[i])
    # ax1.plot(data[OFfile][time], data[OFfile][sensor].iloc[:,1], label = labels[i], linewidth=2, color=colors[i], linestyle = linestyle[i])


# ax1.legend(framealpha=1)
plt.tight_layout()



# ax1.plot(data[OFfile][time], data[OFfile]['Wind1VelY_[m/s]'], label = 'Wind Velocity Y', linewidth=2, color='b', linestyle = linestyle[i])


ax1.legend(framealpha=1)
plt.tight_layout()

# ax1.set_ylim(-55200000000,-551500000000)

# if saveFig:
    # fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'.jpg', dpi=300)
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'_HQ.tiff', dpi=600)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#PLOT FFT OF SIGNAL

# from scipy.fft import fft, fftfreq 
# import numpy as np

# N = (1/(Channels_OF2['Time_[s]'].iloc[1]+Channels_OF2['Time_[s]'].iloc[0])) * (Channels_OF2['Time_[s]'].iloc[-1]-Channels_OF2['Time_[s]'].iloc[0])
# N=int(N)+1
# signal = np.array(Channels_OF[sensor])
# yf = fft(signal)
# xf = fftfreq(N, (Channels_OF2['Time_[s]'].iloc[1]+Channels_OF2['Time_[s]'].iloc[0]))

# fig, ax = plt.subplots()
# ax.plot(xf,2/N*np.abs(yf), color='b')

# data[OFfile][time].to_csv('time.txt')
# data[OFfile][sensor].to_csv('sensor.txt')
