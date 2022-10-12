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
#   usage:          paths = dictionary with paths to folders
                    #sensor = sensor to plot
                    #sensorlabel = label to display on plot
                    #xrng,yrng = x and y ranges
                    #seed_to_compare = dictionary with keywords to select files to compare
                    #colors = dictionary with colors of data in plots
                    #log = flag for PSD plot with log y-scale
                    #lines_to_skip = number of lines to skip at beginning of file if data in ASCII format
                    #labels = dictionary with timeseries labels
                    #binary = select if data is in binary format 
#
#   author:         Francesco Papi
#
#   date:           10/2022
#
#   warnings:       **********************************************************
#------------------------------------------------------------------------------

#---------- USER PARAMETERS ---------------------------------------------------

# %% USER INPUTS

binary = False                                                                 #read binary file (requires FAST toolbox by NREL)
log = False                                                                   #semilog plot
lines_to_skip=2
extend = 20
labels = {
    '1': 'LC21', 
    '2': 'LC25',
    '3': 'LC27'
    }

paths = {
    '1': r'D:\SHARED_ICARO&POLARIS\ALM\FOR_PLOTS\LC21', 
    '2': r'D:\SHARED_ICARO&POLARIS\ALM\FOR_PLOTS\LC25',
    '3': r'D:\SHARED_ICARO&POLARIS\ALM\FOR_PLOTS\LC27'
    }

seed_to_compare = {
    '1': 'rotor_aero_forces_0',
    '2': 'rotor_aero_forces_0',
    '3': 'rotor_aero_forces_0'
    }

colors = {
    '1': 'r',
    '2': 'b',
    '3': 'g'
    }

sensor = 'F_x'
# sensor = 'GenPwr_[kW]'
# sensor = 'Wind1VelY_[m/s]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'RootMxb1'
# sensor = 'YawBrTDxt_[m]'
# sensor = 'TipDxc2_[m]'
# sensor = 'TwrBsMxt_[kN-m]'
# sensor = 'TwrBsFxt_[kN]'
# sensor = 'RtAeroMyh_[N-m]'
# sensor = 'PtfmRDyi_[deg]'
# sensor = 'TipDxc1_[m]'
# sensor = 'YawPos_[deg]'
# sensor = 'HSSBrTqC_[kN-m]'
# sensor = 'RtAeroFxh_[N]'
# sensor = 'RotThrust_[kN]'
# sensor = 'RotPwr_[kW]'
# sensor = 'Wave1Elev_[m]'
# sensor = 'RotSpeed_[rpm]'
# sensor = 'Azimuth_[deg]'
# sensor = 'B1N3Alpha_[deg]'
# sensor = 'YawBrTDyt_[m]'
# sensor = 'TTDspFA_[m]'
# sensor = 'YawBrFxp_[kN]'
# sensor = 'RotSpeed_[rpm]'
# sensor = 'NcIMUTAxs_[m/s^2]'
# sensor = 'GenSpeed_[rpm]'
# sensor = 'YawPos_[deg]'
# sensor = 'PtfmTDzi_[m]'
# sensor = 'L3N70T_[N]'
# sensor = 'PtfmYaw_[deg]'
# sensor = 'PtfmPitch_[deg]'
# sensor = 'HorSpd'
# sensor = 'RootMyc1_[kN-m]'
# sensor = 'TipDxc1_[m]'
# sensor = 'Wave1Elev_[m]'

sensorlabel = sensor
#sensorlabel='$ T_X^{BT} $ (m)'  #'wind speed @ hub (m/s)' #'$ T_X^{BT} $ (m)'

xrng=[0,5]

#------------------------------------------------------------------------------

sf = {}
nperseg = {}
noverlap = {}
Channels = {}
f = {}
PSD = {}

fig1, ax = plt.subplots(2,1)

for key in paths: 
    for file in os.listdir(paths[key]):
        if seed_to_compare[key] in file and '.out' in file:
            OFfile='\\'.join([paths[key], file])
            
    if binary:
        
        Channels[key] = FASTOutputFile(OFfile).toDataFrame()
        
        sf[key] = 1/(Channels[key].loc[1, 'Time_[s]'] - Channels[key].loc[0, 'Time_[s]'])
        nperseg[key] = len(Channels[key]['Time_[s]'])
        noverlap[key] = nperseg[key]/2

        
    else: 
        
        Channels[key] = pd.read_table(OFfile, skiprows=lines_to_skip, skipinitialspace=True, sep = '\s+')
        
        sf[key] = int(1/(Channels[key].loc[1, 'Time'] - Channels[key].loc[0, 'Time']))
        
        if extend == 0:
            ConcatData = Channels[key]
        else:
            ConcatData = Channels[key]
            total_time = Channels[key].loc[:,'Time'].iloc[-1]
            start_time = Channels[key].loc[:,'Time'].iloc[0]

            
            Data_temp = Channels[key].copy()
            Data_temp = Data_temp.drop(labels = Channels[key].index[0])
            
            for kkk in range(extend):
                
                Data_temp_II = Data_temp.copy()
                # try: 
                #     Data_temp_II.loc[:,'Time'] = Data_temp.loc[:,'Time'] + ConcatData.iloc[-1:0] #total_time*(kkk+1)
                # except: 
                Data_temp_II.loc[:,'Time'] = Data_temp.loc[:,'Time'] + (total_time-start_time)*(kkk+1)
                    
                ConcatData = pd.concat([ConcatData, Data_temp_II], ignore_index = True)
                
        Channels[key] = ConcatData    
        nperseg[key] = len(Channels[key]['Time'])
        noverlap[key] = nperseg[key]/2
        
    f[key], PSD[key] = calcPSD(Channels[key][sensor], sf[key], nperseg[key], noverlap[key])     
    
    if binary: 
        
        ax[0].plot(Channels[key]['Time_[s]'], Channels[key][sensor], label = labels[key], linewidth=2, color=colors[key]) 
        
    else: 
        
        ax[0].plot(Channels[key]['Time'], Channels[key][sensor], label = labels[key], linewidth=2, color=colors[key]) 
    

    ax[1].plot(f[key], PSD[key], label = labels[key], linewidth=2, color=colors[key])

    
# set plot labels and stuff like that -----------------------------------------
ax[1].set_xlabel("Hz [-]")
ax[1].set_ylabel(sensorlabel.replace(']', '^2/Hz]'))
ax[1].grid()
ax[1].set_xlim(xrng)
ax[1].legend(framealpha=1)
ax[0].set_ylabel(sensorlabel)
ax[0].set_xlabel("time [s]")

# log scale if wanted ---------------------------------------------------------
if log: 
    
    ax[1].set_yscale('log') 


fig1.tight_layout()

#uncomment to save figure
# fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+seed_to_compare+'15.svg', dpi=300)
#fig1.savefig('C:\\Users\\Papi\\Desktop\\'+sensor+'_HQ.tiff', dpi=600)