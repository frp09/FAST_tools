import pandas
import matplotlib as mpl
import matplotlib.pyplot as plt
import os

#SCRIPT PLOTS LIFETIME DAMAGE EQUIVALENT LOADS 


#sets font size in interactive python plots


def savefig(figure, title, folder):
    plt.rcParams['font.size'] = 33
    plt.rcParams['lines.linewidth'] = 0.9
    plt.rcParams["font.family"] = 'Times New Roman'
    mpl.rcParams['figure.figsize'] = [20.0, 11]
    plt.rcParams['grid.linewidth'] = 0.55
    plt.rcParams['legend.edgecolor'] = 'black'
    plt.rcParams['legend.loc'] = 'upper center'
    fig_path='\\'.join([folder, title])
    figure.savefig(fig_path, dpi=200)

filepathOF='C:\\Python\\DLC12Postprocessing\\OpenFAST\\PP_ResultsOF_NoDBEMT\\LifetimeDEL\\Lifetime_DEL.txt'
#filepathOFII='C:\\Python\\DLC12Postprocessing\\OpenFAST\\PP_ResultsOF_DBEMT\\LifetimeDEL\\Lifetime_DEL.txt'
filepathQB='C:\\Python\\DLC12Postprocessing\\QBlade\\PP_ResultsQB\\LifetimeDEL\\Lifetime_DEL.txt'

Ext_OF=pandas.read_table(filepathOF, index_col=0)
#Ext_OFII=pandas.read_table(filepathOFII, index_col=0)
Ext_QB=pandas.read_table(filepathQB, index_col=0)

def ColumnLabels(dataframe):
#creates more elegant column labels
    
    columnval=dataframe.index.values
    for i in range(len(columnval)):
        splitval=columnval[i].split()
        columnval[i]='\n'.join(splitval)
        if '[X]' in columnval[i]:
            columnval[i]=columnval[i].replace('[X]', '')
    print(type(columnval))
    return columnval

#Gets Column values without '[X]'        
colLab_OF=ColumnLabels(Ext_OF) 
#colLab_OFII=ColumnLabels(Ext_OFII) 
colLab_QB=ColumnLabels(Ext_QB)

for i in range(len(colLab_QB)):
    colLab_QB[i]=colLab_QB[i].replace('[','(')
    colLab_QB[i]=colLab_QB[i].replace(']',')')
    colLab_QB[i]=colLab_QB[i].replace('(N','(kN-')

print(colLab_QB, colLab_OF)    

## Plot Absolute Damage Equivalent Loads
#plots={}
#ax={}
#for j,column in enumerate(Ext_OF.columns.values): 
#               
#    if column == 'm=10':
#        
#        plots[column], ax[column] = plt.subplots()
#        ax[column].set_ylabel('DEL for '+ column+ ' (kNm)')
#        
#        dfindex=Ext_OF.index.values
#        ax[column].bar(colLab_OF[0:3]+'\nm=10', Ext_OF.loc[dfindex[0]:dfindex[2], column], label='OpenFAST DBEMT DELs (m=10)',color='black', alpha=0.5, align='center', width=0.2)
#        ax[column].bar(colLab_OFII[0:3]+'\nm=10', Ext_OFII.loc[dfindex[0]:dfindex[2], column], label='OpenFAST DBEMT DELs (m=10)',color='blue', alpha=0.5, align='edge', width=0.2)
#        #plots[column].show()
#        
#    elif column == 'm=4':
#        
#        plots[column], ax[column] = plt.subplots()
#        ax[column].set_ylabel('DEL for '+ column+ ' (kNm)')
#        
#        dfindex=Ext_OF.index.values
#        ax[column].bar(colLab_OF[3:8]+'\nm=4', Ext_OF.loc[dfindex[3]:dfindex[7], column], label='OpenFAST DBEMT DELs (m=4)', color='black',alpha=0.5, align='center', width=0.2)
#        ax[column].bar(colLab_OFII[3:8]+'\nm=4', Ext_OFII.loc[dfindex[3]:dfindex[7], column], label='OpenFAST DBEMT DELs (m=4)', color='blue',alpha=0.5, align='edge', width=0.2)
#        #plots[column].show()
#
#for j,column in enumerate(Ext_QB.columns.values): 
#               
#    if column == 'm=10': 
#
#        dfindex=Ext_QB.index.values
#        ax[column].bar(colLab_QB[0:3]+'\nm=10', Ext_QB.loc[dfindex[0]:dfindex[2], column]/1000, label='QBlade LLT DELs (m=10)', color='red', alpha=0.5, align='edge', width=-0.2)
#        ax[column].legend()
#        plots[column].show()
#        
#    elif column == 'm=4':
#
#        dfindex=Ext_QB.index.values
#        ax[column].bar(colLab_QB[3:8]+'\nm=4', Ext_QB.loc[dfindex[3]:dfindex[7], column]/1000, label='QBlade LLT DELs (m=4)', color='red',alpha=0.5, align='edge', width=-0.2)
#        ax[column].legend()
#        plots[column].show()
#
#
##Plot Normalized Damage Equivalent Loads
#        
#relplots={}
#relax={}
#
#for j, column in enumerate(Ext_OF.columns.values):
#    
#    if column == 'm=10':
#        
#        relplots[column], relax[column] = plt.subplots()
#        relax[column].set_ylabel('Normalized DEL for '+ column+ ' (kNm)')
#        
#        dfindex=Ext_OF.index.values
#        OF_DEL= Ext_OF.loc[dfindex[0]:dfindex[2], column]
#        OF_DELII= Ext_OFII.loc[dfindex[0]:dfindex[2], column]
#        QB_DEL= Ext_QB.loc[dfindex[0]:dfindex[2], column]
#        relax[column].bar(colLab_OF[0:3]+'\nm=10', OF_DEL/OF_DEL, label='OpenFAST DBEMT DELs (m=10)',color='black', alpha=0.5, align='center', width=0.2)
#        relax[column].bar(colLab_OFII[0:3]+'\nm=10', OF_DELII/OF_DEL, label='OpenFAST DBEMT DELs (m=10)',color='blue', alpha=0.5, align='edge', width=0.2)
#        relax[column].bar(colLab_QB[0:3]+'\nm=10', QB_DEL/(OF_DEL*1000), label='QBlade LLT DELs (m=10)',color='red', alpha=0.5, align='edge', width=-0.2)
#        relax[column].legend()
#        #plots[column].show()
#        
#    elif column == 'm=4':
#        
#        relplots[column], relax[column] = plt.subplots()
#        relax[column].set_ylabel('Normalized DEL for '+ column+ ' (kNm)')
#        
#        dfindex=Ext_OF.index.values
#        OF_DEL= Ext_OF.loc[dfindex[3]:dfindex[7], column]
#        OF_DELII= Ext_OFII.loc[dfindex[3]:dfindex[7], column]
#        QB_DEL= Ext_QB.loc[dfindex[3]:dfindex[7], column]
#        relax[column].bar(colLab_OF[3:8]+'\nm=4', OF_DEL/OF_DEL, label='OpenFAST DBEMT DELs (m=4)',color='black', alpha=0.5, align='center', width=0.2)
#        relax[column].bar(colLab_OFII[3:8]+'\nm=4', OF_DELII/OF_DEL, label='OpenFAST DBEMT DELs (m=4)',color='blue', alpha=0.5, align='edge', width=0.2)
#        relax[column].bar(colLab_QB[3:8]+'\nm=4', QB_DEL/(OF_DEL*1000), label='QBlade LLT DELs (m=4)',color='red', alpha=0.5, align='edge', width=-0.2)
#        relax[column].legend()
#        
#for element in ax:
#    element.legend()

#FOLLOWING PART CREATES ONE PLOT PER WIND SPEED BIN WITH ALL THE DAMAGE EQUIVALENT LOADS COMPARED


Windspeeds=[i for i in range(4,25,2)]

Xticks = [1, 2, 3, 4, 5, 6, 7, 8]
Xticklabel = colLab_OF
for i in range(len(Xticklabel)):
    Xticklabel[i]=Xticklabel[i].replace('\n(kN-m)','')
Xticklabel[0:2]=Xticklabel[0:2]+'\nm=10'
Xticklabel[2:7]=Xticklabel[2:7]+'\nm=4' 
        
for j,column in enumerate(Ext_OF.columns.values): 
                   
    if column == 'm=4':

        
        plot, ax = plt.subplots()
        
        ax.ticklabel_format(style='sci', scilimits=(-3,4), axis='y')
        ax.set_xticks(Xticks)
        ax.set_xticklabels(Xticklabel)
        ax2 = ax.twinx()
        ax2.ticklabel_format(style='sci', scilimits=(-3,4), axis='y')
        ax2.set_ylabel('DEL for '+ column+ ' (kNm)')
        title='Lifetime Damage Equivalent Loads'
        ax.set_title(title)
        #plots[i].suptitle(title, verticalalignment='top')
        
        dfindex=Ext_OF.index.values
        ax2.bar(Xticks[2:7], Ext_OF.loc[dfindex[2]:dfindex[6], column], label='OpenFAST BEM',color='mediumblue', alpha=1, align='center', width=0.2)
        
        #ax[column].bar(CL_OFast[i][0:3]+'\nm=10', Ext_OFII.loc[dfindex[0]:dfindex[2], column], label='OpenFAST DBEMT DELs (m=10)',color='blue', alpha=0.5, align='edge', width=0.2)
        #plots[column].show()
        
    elif column == 'm=10':

        ax.set_ylabel('DEL for '+ column+ ' (kNm)')
        
        dfindex=Ext_OF.index.values
        ax.bar(Xticks[0:2], Ext_OF.loc[dfindex[0]:dfindex[1], column], color='mediumblue',alpha=1, align='center', width=0.2)
        #ax[column].bar(colLab_OFII[3:8]+'\nm=4', Ext_OFII.loc[dfindex[3]:dfindex[7], column], label='OpenFAST DBEMT DELs (m=4)', color='blue',alpha=0.5, align='edge', width=0.2)
        #plots[column].show()
    
    

for j,column in enumerate(Ext_QB.columns.values): 
                   
    if column == 'm=4': 

        dfindex=Ext_QB.index.values
        ax2.bar(Xticks[2:7], Ext_QB.loc[dfindex[2]:dfindex[6], column]/1000, label='QBlade LLFVW', color='r', alpha=1, align='edge', width=0.2)
        ax2.legend()
        #plots[column].show()
        
    elif column == 'm=10':

        dfindex=Ext_QB.index.values
        ax.bar(Xticks[0:2], Ext_QB.loc[dfindex[0]:dfindex[1], column]/1000, color='r',alpha=1, align='edge', width=0.2)
        #ax[i].legend()
        #plots[column].show()
        
    figtitle=('Lifetime DEL').replace(' ','_')
    
    if not os.path.exists('C:\\Python\\Plots\\LifetimeDEL_Plots'):
        os.mkdir('C:\\Python\\Plots\\LifetimeDEL_Plots')
        
savefig(plot, figtitle, 'C:\\Python\\Plots\\LifetimeDEL_Plots')   
    