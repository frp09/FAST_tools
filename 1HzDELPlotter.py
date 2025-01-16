import pandas
import matplotlib.pyplot as plt
import numpy as np 
import scipy.special as special
import glob

# def savefig(figure, title, folder):
#     plt.rcParams['font.size'] = 20
#     plt.rcParams['lines.linewidth'] = 0.9
#     plt.rcParams["font.family"] = 'Times New Roman'
#     mpl.rcParams['figure.figsize'] = [15.0, 7]
#     plt.rcParams['grid.linewidth'] = 0.55
#     plt.rcParams['legend.edgecolor'] = 'black'
#     plt.rcParams['legend.loc'] = 'best'
#     fig_path='\\'.join([folder, title])
#     figure.savefig(fig_path, dpi=200)

'''

#------------------------------------------------------------------------------
#   1Hz DEL PLOTTER
#
#   description:    script selects 1Hz DELs calculateb by Crunch in folder
#                   specified in sourcepaths. 
#                   that a results file is being loaded
#
#   usage:          relative = flag for creation of relative plots. If true "refpaths" must also be specified
                    weighted = flag for creation of weibull-weighted bars
                    sensors = list of sensors to plot. For each sensor one plot will be generated
                    expnt = list of Wholer-curve eponents to use. len(expnt) = len(sensors)
                    sourcepaths = list of sourcepaths to compare in plots
                    refpaths = list of reference data. On per each source
                    shift = amount to shift each bar. One balue per source
                    colors = colors to use in plots. One value per source
                    label15 = label for source 1
                    label5 = label for source 2
                    shape = shape factor of weibull ws distribution (default = 2)
                    mean = mean of Weibull ws distribution
                    ws = array of wind mean simulation windspeed. Useful to bin the simulations. One array per source. 
                    
#   author:         Francesco Papi
#
#   date:           09/2020
#
#   warnings:       "openFast toolbox" IS REQUIRED:
                    https://github.com/OpenFAST/openfast_toolbox
#------------------------------------------------------------------------------

 '''

  
#Function reads the dataframes and outputs, per each wind speed bin, a dataframe containing average quantities. 
def AverageDEL(bin_mid, files):
    
    #this part creates a list of dictionaries. Each dictionary represents one wind speed bin and contains the dataframes
    #of the 1hz DELs of the bin 
    groupedDELs=[]
    AverageDELs=[]
    
    for n,wind in enumerate(bin_mid):
        dic={}
        groupedDELs.append(dic)
        
        for file in files:
            if 'ws'+str(wind) in file:
                groupedDELs[n][file]=pandas.read_table(file, index_col=0)
                
                
    for n,element in enumerate(groupedDELs):
        for m,dataframe in enumerate(element):
            if m==0:
                AverageDELs.append(element[dataframe])
            else:
                AverageDELs[n]=AverageDELs[n]+element[dataframe]
        
        #Divides the total by 6
        AverageDELs[n]= AverageDELs[n]/6
   
    return AverageDELs
        


def ColumnLabels(dataframe):
#creates more elegant column labels
    
    columnval=dataframe.index.values
    for i in range(len(columnval)):
        splitval=columnval[i].split()
        columnval[i]='\n'.join(splitval)
        if '[X]' in columnval[i]:
            columnval[i]=columnval[i].replace('[X]', '')
          
    return columnval
    
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# -------------------------------- USER DATA -----------------------------------

relative = True
weighted = False

sensors = ['TwrBsMyt[X] (kN-m)','TwrBsMxt[X] (kN-m)', 'TwrBsFxt[X] (kN)',
           'YawBrFxp[X] (kN)', 'YawBrMyp[X] (kN-m)', 'YawBrMxp[X] (kN-m)']
expnt = [4, 4, 4, 4, 4, 4]

sourcepaths = [r'D:\Wind\FLOATING\DLC1X\Fatigue_Post\Results5MW\1HzDEL\DLC12',
                r'D:\Wind\FLOATING\DLC1X\Fatigue_Post\Results15MW\1HzDEL\DLC12']

refpaths = [r'D:\Wind\FLOATING\DLC1X\Fatigue_Post\Results5MW_onshore\1HzDEL\DLC12',
              r'D:\Wind\FLOATING\DLC1X\Fatigue_Post\Results15MW_onshore\1HzDEL\DLC12']

shift = [-0.15, 0.15]
colors = ['b', 'r']

label15 = 'IEA 15MW'
label5 = 'NREL 5MW'

shape = 2
mean = 8.5

ws = np. array([[3.635149,5.582053,7.438090,9.268921,11.339183,13.045674,14.947802,16.669432,18.613011,20.530736,22.302983],
                [4,6,8,10,12,14,16,18,20,22,24]])
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

files = {}
reffiles = {}

bin_mid=[i for i in range(4,25,2)]
bins = [[3,5],[5,7],[7,9],[9,11],[11,13],[13,15],[15,17],[17,19],[19,21],[21,23],[23,25]]

for path in sourcepaths:
    
    files[path] = glob.glob(path+'\*.txt')

if relative:     
    for spath in refpaths: 
        
        reffiles[spath] = glob.glob(spath+'\*.txt')

avDELs = {}
refavDELs = {}
for iii, path in enumerate(sourcepaths):
    
    avDELs[path] = AverageDEL(bin_mid, files[path])

if relative:    
    for iii, path in enumerate(refpaths):
        
        refavDELs[path] = AverageDEL(bin_mid, reffiles[path])


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#calculate Weibull probability distribution if user wats to weigh ws bins

bins = pandas.DataFrame(data = bins, index = bin_mid)

G_arg = 1+(1/shape)
G_ws = special.gamma(G_arg)
scale = mean/G_ws

arg_top = (bins.loc[:,1]/scale)**(shape)
p_top = (1-np.exp(-arg_top))


arg_bottom=(bins.loc[:,0]/scale)**(shape)
p_bottom=(1-np.exp(-arg_bottom))
p=p_top-p_bottom

binnum = np.digitize(ws, p.index-1)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#FOLLOWING PART CREATES ONE PLOT PER LOADSENSOR WITH ALL THE WIND SPEEDS COMPARED           
senplt={}
senax={}
senax_twin={}

for n,sensor in enumerate(sensors):
        
    senplt[sensor], senax[sensor] = plt.subplots(figsize=(7,4)) 
    senax[sensor].set_xlabel('Wind Speed (m/s)')
    senax[sensor].xaxis.set_ticks(bin_mid)
    
    
    for m,wind in enumerate(bin_mid):
                 
        senax[sensor].set_ylabel(sensor.replace('[X]','')+ '\n 1HzDEL averaged per WS bin (m=4)')
        
        for kkk,path in enumerate(sourcepaths): 
            
            if relative: 
                value = avDELs[path][m].loc[sensor, 'm='+str(expnt[kkk])] / refavDELs[refpaths[kkk]][m].loc[sensor, 'm='+str(expnt[kkk])]
                senax[sensor].set_ylim([0,2.75])
                
            else:
                
                if weighted:
                    
                    value = avDELs[path][m].loc[sensor, 'm='+str(expnt[kkk])] * p.loc[wind]
                    
                else: 
                    
                    value = avDELs[path][m].loc[sensor, 'm='+str(expnt[kkk])]

            if wind == 6 and kkk == 0: 
                
                senax[sensor].bar(wind+shift[kkk], value, fill = False, linestyle = '--', edgecolor = colors[kkk])
            
            else:
                senax[sensor].bar(wind+shift[kkk], value, color = colors[kkk])
                
   
    
    senax[sensor].legend([label5, label15]) 
    senax[sensor].set_axisbelow(True)
    senax[sensor].grid(linestyle = 'dashed', axis = 'y')
    senplt[sensor].tight_layout()
    
    
    senplt[sensor].savefig(r'C:\Users\Papi\Desktop\1HzDELS\\'+(sensor+'_av_DEL_grpbyws').replace('\n','_').replace('=','').replace(' ', '_'), dpi=300)
    # savefig(senplt[sensor], (sensor+'_av_DEL_grpbyws').replace('\n','_').replace('=','').replace(' ', '_'), r'C:\Users\Papi\Desktop\1HzDELS')
