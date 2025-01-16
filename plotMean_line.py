import numpy as np
import sys
import matplotlib.pyplot as plt

#sys.path.append('C:\\Users\\Papi\\Desktop')
from FASTAverageCalculator import *

'''
#------------------------------------------------------------------------------
#   FAST OUTPUT BAR PLOTTER (MEAN)
#
#   description:    creates per-DLC bar plots of mean quantities
#                   windspeeds are read as average wind speeds.
#
#   usage:          the file quantities needed are defined in "user values"
#
#   author:         Francesco Papi
#
#   date:           Jul 2021
#
#   warnings:       Make sure len(sourcepaths)=len(refPaths)
                    "openFast toolbox" IS REQUIRED:
                    https://github.com/OpenFAST/openfast_toolbox
#------------------------------------------------------------------------------
'''

#%%------------------------ USER VALUES ---------------------------------------

# sensor = 'RotThrust_[kN]'
# sensor = 'RtAeroFxh_[N]'
# sensor = 'TwrBsMyt_[kN-m]'
# sensor = 'RtAeroCt_[-]'
# sensor = 'YawBrFxp_[kN]'
# sensor = 'YawBrMyp_[kN-m]'
# sensor = 'TwrBsFxt_[kN]'
# sensor = 'GenPwr_[kW]'
# sensor = 'BldPitch1_[deg]'
# sensor = 'Wind1VelX_[m/s]'
sensor = 'PtfmPitch_[deg]'
# sensor = 'TipDxc1_[m]'
# sensor = 'NcIMUTAxs_[m/s^2]'

wind = 'Wind1VelX_[m/s]'

relative = False

labels = ['NREL 5MW onshore', 'IEA 15MW onshore']
colors = ['r', 'b']

sourcepaths = [r'D:\Wind\FLOATING\DLC1X\IEA15MW_DLC11\Results\Means&Stds',
                r'D:\Wind\FLOATING\DLC1X\NREL5MW_DLC11\Results']

refpaths = [r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC11_onshore\Results',
            r'D:\Wind\FLOATING\DLC1.X\IEA15MW_DLC16_onshore\Results']

#-----------------------------------------------------------------------------

means = {}
maxs = {}
mins = {}
stds = {}

for path in sourcepaths: 
    
    if os.path.exists(path):
        
        readPath = path
        
        means[path] = averageReader(readPath, 'Means.txt')
        maxs[path] = averageReader(readPath, 'Maximums.txt')
        mins[path] = averageReader(readPath, 'Minimums.txt')
        stds[path] =averageReader(readPath, 'Stds.txt')
    
    # TO DO: creater outine to read .out files
    # else:
        
    #     averageCalculator(folderPath, windspeeds, sensors)
    #     averageWriter(dataframe, units, path, name)
        
        
means_r = {}
maxs_r = {}
mins_r = {}
stds_r = {}

if relative:
 
    for path in refpaths: 
        
        if os.path.exists(path):
            
            readPath = path
            
            means_r[path] = averageReader(readPath, 'Means.txt')
            maxs_r[path] = averageReader(readPath, 'Maximums.txt')
            mins_r[path] = averageReader(readPath, 'Minimums.txt')
            stds_r[path] =averageReader(readPath, 'Stds.txt')
            
        # TO DO: creater outine to read .out files    
        # else:
            
        #     averageCalculator(folderPath, windspeeds, sensors)
        #     averageWriter(dataframe, units, path, name)

fig, ax = plt.subplots()   
for iii,path in enumerate(sourcepaths):
    
    if relative:
        
        mean = means[path].loc[:,sensor] / means_r[refpaths[iii]].loc[:,sensor]
        ax.plot([2,26], [1,1], linestyle='--', color = 'black')
    
    else:
        error = np.array([means[path].loc[:,sensor]-mins[path].loc[:,sensor], maxs[path].loc[:,sensor]-means[path].loc[:,sensor]])
        #ax.plot(means[path].iloc[:,0]+offset[iii], means[path].loc[:,sensor], marker = 'o', linestyle = '', color = colors[iii])
        ax.fill_between(means[path].loc[:,wind], means[path].loc[:,sensor]-stds[path].loc[:,sensor], means[path].loc[:,sensor]+stds[path].loc[:,sensor], alpha = 0.2, color = colors[iii])
        mean = means[path].loc[:,sensor]
    
    
    ax.errorbar(means[path].loc[:,wind] ,means[path].loc[:,sensor], elinewidth = 0, marker = 'o', linestyle = '-', color = colors[iii], yerr = error, capsize = 5, label = labels[iii])
    print(means[path].loc[:,sensor])   
    #ax.plot(means[path].iloc[:,0]+offset[iii], mean, color = colors[iii], label = labels[iii])
         
ax.legend(fontsize = 'large', framealpha = 1, loc='lower center')


ax.set_xticks([4,6,8,10,12,14,16,18,20,22,24])
ax.grid(linestyle = 'dashed', axis = 'y')

ax.set_xlabel( 'average wind speed (m/s)', fontsize = 14 )
ax.set_ylabel(sensor, fontsize = 14 )
ax.tick_params(axis='both', labelsize=12)
fig.tight_layout()

# fig.savefig(r'c:\Users\Papi\Desktop\\'+sensor+'Mean.png', dpi = 300)
