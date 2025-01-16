import pandas as pd
import glob
import os

import openfast_toolbox
from openfast_toolbox.io import FASTOutputFile

'''
#------------------------------------------------------------------------------
#   FAST OUTPUT FUCTIONS
#
#   description:    collection of fuctions useful to manipulate FAST output data
#                   
#
#   usage:          functions are called from separate script
#
#   author:         Francesco Papi
#
#   date:           Jul 2021
#
#   warnings:       "openFast toolbox" IS REQUIRED:
                    https://github.com/OpenFAST/openfast_toolbox
#------------------------------------------------------------------------------
'''


def averageCalculator(folderPath, windspeeds, sensors):
    
    ''' calculate mean values '''
    
    files=glob.glob(folderPath+'\*.outb')
    means=pd.DataFrame(index=windspeeds, columns=sensors)
    standardDeviations=pd.DataFrame(index=windspeeds, columns=sensors)
    maximums=pd.DataFrame(index=windspeeds, columns=sensors)
    minimums=pd.DataFrame(index=windspeeds, columns=sensors)
    abs_maximums=pd.DataFrame(index=windspeeds, columns=sensors)
    for wind in windspeeds: 

        toAverage=pd.DataFrame()

        for file in files:
             
            if 'ws'+str(wind)+'_' in file:

                toAverageTMP = FASTOutputFile(file).toDataFrame()
                toAverage=pd.concat([toAverage, toAverageTMP])
                print('Appending ', file)
                
            elif 'ws'+str(wind).replace('.','-')+'_' in file:                

                toAverageTMP = FASTOutputFile(file).toDataFrame()
                toAverage=pd.concat([toAverage, toAverageTMP])
                print('Appending ', file)
                
        if toAverage.empty:
            
            print('WARNING: no files with wind speed = ', wind, ' in folder: ', folderPath)
            
        units=[]
        
        for sensor in sensors:
            
            means.loc[wind, sensor] = toAverage.loc[:, sensor].mean()
            standardDeviations.loc[wind,sensor] = toAverage.loc[:,sensor].std()
            maximums.loc[wind,sensor] = toAverage.loc[:,sensor].max()
            minimums.loc[wind,sensor] = toAverage.loc[:,sensor].min()
            abs_maximums.loc[wind,sensor] = abs(toAverage.loc[:,sensor]).max()
     
    
    return means, standardDeviations, units, maximums, minimums, abs_maximums

def averageWriter(dataframe, units, path, name):
    
    '''write averages to a given folder'''

    if not os.path.exists(path):
        os.mkdir(path)
        
    resultfile='\\'.join([path, name])
    # result=open(resultfile, 'w')

    # unitsString = "\t".join(units)
    # result.write(unitsString)
    # result.write('\n')
    dataframe.to_csv(resultfile, sep='\t')
    # result.close()
    
def averageReader(path, seed):
   
    '''read averages in folder'''
    
    files=glob.glob(path+'\*.txt')
    for file in files:
        
        if seed in file:
            
            df = pd.read_table(file)#, index_col = 0)
        
            
    return df
    