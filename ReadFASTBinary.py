# Script that mimics the functionality of the ReadFASTbinary.m functionality
# But you get a pandas data frame instead of a lousy matrix
# 2018 SPB

# % Input:
# %  FileName      - string: contains file name to open
# %
# % Output:
# %  Channels      - Pandas Dataframe with all the channels: Index and 1st column: Time, Column name = ChanName
# %  ChanUnit      - cell array containing unit names of output channels
# %  FileID        - constant that determines if the time is stored in the
# %                  output, indicating possible non-constant time step
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import struct as st
import pandas as pd
from numpy import array,arange,zeros,divide

FileFmtID = pd.Series([1, 2], list(['WithTime', 'WithoutTime']))

# FileFmtID
# FileFmtID.WithTime

#FileName='DTU10MW_16ms_1_3_400_t1.outb'

def ReadFASTbinary(FileName):
    LenName = 10
    LenUnit = 10

    FileFmtID = pd.Series([1, 2], list(['WithTime', 'WithoutTime']))

    # FileName = 'a:\\Publications\\180611_ASME_Turbo_Expo\\Results\\FAST\\Turbulent\\ws18ms_d8_s118_noDOF.outb'

    try:
        Fil = open(FileName,'rb')
        # Fil.close()
    except:
        print('Could not open the FAST binary file: {0}'.format(FileName))


    else:
        with Fil as fobj:
            FileID = st.unpack('h',fobj.read(2))[0]
            NumOutChans = st.unpack('i',fobj.read(4))[0]
            NT = st.unpack('i',fobj.read(4))[0]
            # NumOutChans, NT = st.unpack('hii',fobj.read(10))
            if FileID == FileFmtID.WithTime:
                TimeScl = st.unpack('d',fobj.read(8))[0]
                TimeOff = st.unpack('d',fobj.read(8))[0]
            else:
                TimeOut1 = st.unpack('d',fobj.read(8))[0]
                TimeIncr = st.unpack('d',fobj.read(8))[0]
            ColScl = st.unpack('f'*NumOutChans, fobj.read(4*NumOutChans))[:]
            ColScl = array(ColScl)
            ColOff = st.unpack('f'*NumOutChans, fobj.read(4*NumOutChans))[:]
            ColOff = array(ColOff)
            LenDesc = st.unpack('i',fobj.read(4))[0]
            DescStr = st.unpack('{}s'.format(LenDesc),fobj.read(1*LenDesc))
            DescStr = DescStr[0].decode('utf-8').strip()
            ChanName = []
            for iChan in range(NumOutChans+1):
                Name = st.unpack('{}s'.format(LenName), fobj.read(1*LenName))[:]
                Name = Name[0].decode('utf-8').strip()
                ChanName.append(Name)
            ChanUnit = []
            for iChan in range(NumOutChans+1):
                Unit = st.unpack('{}s'.format(LenUnit), fobj.read(1*LenUnit))[:]
                Unit = Unit[0].decode('unicode_escape').strip()
                ChanUnit.append(Unit)
            print("Reading from the file {0} with heading: \n {1}.".format(FileName,DescStr))
# ----------------------------
#  get the channel time series
# ----------------------------
            nPts = NT*NumOutChans
            Channels = zeros((NT,NumOutChans+1))
            if FileID == FileFmtID.WithTime:
                PackedTime = st.unpack('i'*NT,fobj.read(4*NT))[:]
                PackedTime = array(PackedTime)
                cnt = len(PackedTime)
                if(cnt < NT):
                    print("Could not read entire {0} file: read {1} of {2} time values".format(FileName,cnt,NT))
            PackedData = st.unpack('h'*nPts,fobj.read(2*nPts))[:]
            PackedData = array(PackedData)
            cnt = len(PackedData)
            if (cnt < nPts):
                print("Could not read entire {0} file: read {1} of {2} values".format(FileName,cnt,nPts))
# -------------------
# Scale the packed binary to real data
# -------------------
        for it in range(NT):
            Channels[it,1:] = divide(PackedData[NumOutChans*it:NumOutChans*(it+1)] -ColOff,ColScl)
        if FileID == FileFmtID.WithTime:
            Channels[:,0] = divide(PackedTime - TimeOff, TimeScl)
        else:
            Channels[:,0] = TimeOut1 + TimeIncr*arange(NT)
#---------------------
#Convert into a pandas dataframe
#---------------------

        Chans = pd.DataFrame(Channels,index = Channels[:,0], columns = ChanName)
        return (Chans,ChanUnit,FileID,DescStr)

# Chans
# %%
# # len(Channels[:,0])
# Channels[:,78]
# ChanName
#
# it
# NumOutChans
# ColOff
# ColScl
# Channels[:,4]
# PackedData
# arange
# PackedData
# nPts
# FileFmtID.WithTime
# Unit
# FileID
# NumOutChans
# NT
# TimeOut1
# TimeIncr
# ColScl
# DescStr
# PackedTime
# cnt
# # ChanName
# # ChanName[0][0]
# # ChanName[:] = [x[0].decode('utf-8') for x in ChanName]
# # ChanName
# # Name = list(Name)
# # for i in range(len(Name)):
# #     Name[i] = ' '.join(Name[i].decode('utf-8'))
# Name

#for index,row in Chans.iterrows(): 
#    if '*********' in Chans.loc[index]:
#        print(row)