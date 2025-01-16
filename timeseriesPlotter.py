import matplotlib.pyplot as plt
import sys
import os
import pandas as pd
import math
import numpy as np

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
#   usage:          #path = LIST of paths to file folders
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
#   warnings:       "openFast toolbox" IS REQUIRED:
                    https://github.com/OpenFAST/openfast_toolbox
#------------------------------------------------------------------------------
'''

#%%-------- USER PARAMETERS ---------------------------------------------------


paths = [
            r'path to folder containing result to plot',

            ]

seed_to_compare = [
                    'pattern in name or name of file to plot', 

                   ]

labels = [
           'label of files for graph', 

          ]


binary = True
# saveFig = False

colors = ['r', 'b', 'black', 'green']
linestyle = ['-','-', '-', '-']


sensor = 'RtAeroFxh_[N]'
# sensor = 'RtAeroMxh_[N-m]'
# sensor = 'RotSpeed_[rpm]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'TipDyc1_[m]'
# sensor = 'GenPwr'


time = 'Time_[s]'
# # time = 'Azimuth_[deg]'
# time = 'RotSpeed_[rpm]'


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
