import scipy.signal as signal

# channel = timeseries
# samplingfreq = 1/timestep
# nperseg = 2048
# noverlap = 0.5


def calcPSD(channel, samplingfreq, nperseg, noverlap):

    f, PSD=signal.welch(channel, samplingfreq, nperseg=nperseg, noverlap=noverlap)
    
    return f, PSD

