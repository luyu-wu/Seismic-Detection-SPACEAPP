# LIBRARIES
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import algorithm
from pathlib import Path

# DEFINITIONS
mars = True
highPass = False

## Catalogs
file_dir = Path(__file__).parent /'./data/lunar/test/data/'
if mars:
    file_dir = Path(__file__).parent /'./data/mars/test/data/'
    
counter = 0

for file in os.listdir(file_dir):
    file_path = file_dir/os.fsdecode(file)
    print("Save",counter)
    counter +=1;
    if os.path.exists(file_path):

        data_cat = pd.read_csv(file_path)

        # MAIN CODE
        csv_times = None
        csv_data = None
        
        if not mars:
            csv_times = np.array(data_cat['time_rel(sec)'].tolist())
            csv_data = np.array(data_cat['velocity(m/s)'].tolist())
        else:
            csv_times = np.array(data_cat['rel_time(sec)'].tolist())
            csv_data = np.array(data_cat['velocity(c/s)'].tolist())

        algo_spot = algorithm.findTime(csv_times,csv_data,highpass=highPass)
        
        fig, temp_ax = plt.subplots()

        temp_ax.set_title("Graph: "+str(file))
        temp_ax.plot(csv_times,csv_data)
        temp_ax.set_ylabel("Velocity $(m/s)$")
        temp_ax.set_xlabel("Time $(s)$")

        temp_ax.axvline(x=algo_spot,c='blue',linestyle="dashed",label="Algorithm Arrival")
        temp_ax.legend()

        fig.savefig('./mars_results/figure_'+str(counter)+'.png')   # save the figure to file
        plt.close(fig)
            
#print("Show plots??")
#plt.show()
