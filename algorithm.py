import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from numba import njit, prange


block_large = 50000
block_small = 10000

# for mars
#block_large = 500
#block_small = 100

plt.show()
@njit(parallel=True)
def forwardMarch(time,vel):
    factor = 6000

    time = np.append(np.zeros(block_large),time)
    vel = np.append(np.zeros(block_large),vel)
    time = np.append(time,np.repeat(time[-1],block_large))
    vel = np.append(vel,np.zeros(block_large))
    num_frames = int((len(vel) - block_large)/factor)

    rtm_array = np.zeros(num_frames)
    time_array = np.zeros(num_frames)
    
    for i in prange(num_frames):
        index = i*factor
        # change to leading block algorithm (smaller block leading)
        subset_small = vel[index+block_large-block_small:index+block_large]
        subset_large = vel[index:index+block_large]

        time_array[i] = time[index+block_large]        
        rtm_array[i] =  np.average(np.abs(subset_small))-np.average(np.abs(subset_large))
    return time_array,rtm_array

def showGraph(time,vel):
    timestep = time[-1]/len(time)

    sos = signal.butter(10, 1.5, 'hp', fs=1/timestep, output='sos')
    filtered = signal.sosfilt(sos, vel)

    fig, (filter_ax,rtm_rat_ax) = plt.subplots(2)

    filter_ax.plot(time,vel,label="No Filter")
    filter_ax.plot(time,filtered,label="Filtered Signal")
    filter_ax.set_title("High-Pass Filter")
    filter_ax.set_xlabel("Time (s)")
    filter_ax.set_ylabel("Velocity (m/s)")
    filter_ax.grid()
    filter_ax.legend()

    filter_ax.set_xlim([time[0],time[-1]])

    time_rtm,rtm_ratio_nofilt = forwardMarch(time,vel)
    rtm_rat_ax.plot(time_rtm,rtm_ratio_nofilt)
    rtm_rat_ax.fill_between(time_rtm, rtm_ratio_nofilt, 0,alpha=0.3, facecolor='#089FFF')

    rtm_rat_ax.set_xlim([time_rtm[0],time_rtm[-1]])

    rtm_rat_ax.grid()

    plt.show()

    
def findTime(time,vel,highpass=False,showgraphs=False):

    adjustment_factor = block_small/6

    timestep = time[-1]/len(time)
    
    if showgraphs:
        showGraph(time,vel)        

    if highpass:
        sos = signal.butter(10, 1.5, 'hp', fs=1/timestep, output='sos')
        vel = signal.sosfilt(sos, vel)

    time_rtm,rtm_ratio_nofilt = forwardMarch(time,vel)

    return time_rtm[np.argmax(rtm_ratio_nofilt)] - adjustment_factor
