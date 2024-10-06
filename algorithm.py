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

    rtm_array_small = np.zeros(num_frames)
    rtm_array_large = np.zeros(num_frames)
    time_array = np.zeros(num_frames)
    
    for i in prange(num_frames):
        index = i*factor
        # change to leading block algorithm (smaller block leading)
        subset_small = vel[index+block_large-block_small:index+block_large]
        subset_large = vel[index:index+block_large]

        time_array[i] = time[index+block_large]        
        rtm_array_small[i] = np.average(np.abs(subset_small))
        rtm_array_large[i] = np.average(np.abs(subset_large))
    return time_array,rtm_array_small,rtm_array_large

def showGraph(time,vel):
    timestep = time[-1]/len(time)

    fig, (filter_ax,rtm_rat_ax) = plt.subplots(2)

    filter_ax.plot(time,vel)
    rtm_rat_ax.set_xlabel("Time (s)")
    filter_ax.set_ylabel("Velocity (m/s)")
    rtm_rat_ax.set_ylabel("Velocity (m/s)")

    plt.setp(filter_ax.get_xticklabels(), visible=False)
    filter_ax.grid()

    filter_ax.set_xlim([time[0],time[-1]])

    time_rtm,rtm_ratio_small,rtm_ratio_large = forwardMarch(time,vel)
    
    rtm_rat_ax.plot(time_rtm,rtm_ratio_small-rtm_ratio_large,label="Difference")
    rtm_rat_ax.fill_between(time_rtm, rtm_ratio_small-rtm_ratio_large, 0,alpha=0.3, facecolor='#089FFF')

    rtm_rat_ax.plot(time_rtm,rtm_ratio_small,label="Small Box")
    rtm_rat_ax.fill_between(time_rtm, rtm_ratio_small, 0,alpha=0.3, facecolor='#FF8419')

    rtm_rat_ax.plot(time_rtm,rtm_ratio_large,label="Large Box")
    rtm_rat_ax.fill_between(time_rtm, rtm_ratio_large, 0,alpha=0.3, facecolor='#65BC85')
    
    rtm_rat_ax.set_xlim([time_rtm[0],time_rtm[-1]])
    rtm_rat_ax.legend()
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

    time_rtm,rtm_ratio_small,rtm_large = forwardMarch(time,vel)
    rtm_ratio = rtm_ratio_small - rtm_large
    return time_rtm[np.argmax(rtm_ratio)] - adjustment_factor
