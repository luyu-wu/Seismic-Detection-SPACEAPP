# LIBRARIES
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
import algorithm

# DEFINITIONS
mars = False
showGraphs = False
drawExceptions = False
highPass = False

## Catalogs
catalog_dir = './data/lunar/training/catalogs/'
if mars:
    catalog_dir = './data/mars/training/catalogs/'

catalog_file_str = catalog_dir + 'apollo12_catalog_GradeA_final.csv'
if mars:
    catalog_file_str = catalog_dir + 'Mars_InSight_training_catalog_final.csv'

catalog = pd.read_csv(catalog_file_str)

length = int(catalog.shape[0])
residuals = np.array([])
for i in range(length):
    ## Data
    row = catalog.iloc[i]
    arrival_time = row['time_rel(sec)']

    test_filename = row.filename
    print(int(1000*i/length)/10,"%")
    data_directory = './data/lunar/training/data/S12_GradeA/'
    if mars:
        data_directory = './data/mars/training/data/'

    csv_file = f'{data_directory}{test_filename}.csv' # Lunar
    if mars:
        csv_file = f'{data_directory}{test_filename}' # Lunar
    
    if os.path.exists(csv_file):
        data_cat = pd.read_csv(csv_file)

        # MAIN CODE
        csv_times = 0
        csv_data = 0
        if not mars:
            csv_times = np.array(data_cat['time_rel(sec)'].tolist())
            csv_data = np.array(data_cat['velocity(m/s)'].tolist())
        else:
            csv_times = np.array(data_cat['rel_time(sec)'].tolist())
            csv_data = np.array(data_cat['velocity(c/s)'].tolist())

        algo_spot = algorithm.findTime(csv_times,csv_data,highpass=highPass,showgraphs=showGraphs)
        
        if abs(algo_spot-arrival_time) > 1e+3 and drawExceptions: 
            print("HIGH DIFFERENCE:",algo_spot-arrival_time,"s")
            print("Row Number:",i)
            fig, temp_ax = plt.subplots()

            temp_ax.set_title("highDelta ROW: "+str(i)+" Diff: "+str(algo_spot-arrival_time)+" s")
            temp_ax.plot(csv_times,csv_data)
            temp_ax.set_ylabel("Velocity $(m/s)$")
            temp_ax.set_xlabel("Time $(s)$")

            temp_ax.axvline(x=arrival_time, c='red', label='Catalog Arrival')
            temp_ax.axvline(x=algo_spot,c='blue',linestyle="dashed",label="Algorithm Arrival")
            temp_ax.legend()
            
            
            
        residuals = np.append(residuals, algo_spot-arrival_time)
    else:
        print("FILE DNE ERROR")
if drawExceptions:
    plt.show()
    
fig, (norm_ax, log_ax) = plt.subplots(2)
norm_ax.set_title("Residuals of Algorithm training")
norm_ax.bar(range(len(residuals)),height=residuals,width=0.5,linewidth=3)
norm_ax.grid(axis="y")
norm_ax.set_ylabel("Time Difference [s]")   
plt.setp(norm_ax.get_xticklabels(), visible=False)
log_ax.set_title("Log Axis of Residuals")
log_ax.bar(range(len(residuals)),height=np.abs(residuals),width=0.5,linewidth=3)
log_ax.set_yscale("log")
log_ax.grid(axis="y")
log_ax.set_ylabel("Time Difference [$log_{10}s$]")   
log_ax.set_xlabel("Training Data")            


plt.show()
