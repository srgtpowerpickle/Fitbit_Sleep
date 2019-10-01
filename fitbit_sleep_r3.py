# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from matplotlib.dates import HourLocator, MinuteLocator, DateFormatter
from datetime import datetime
from datetime import timedelta

my_colors = ['r', 'g', 'b', 'k', 'y', 'm', 'c']

# Number of .json files
N_files = 49

# First date of .json data
DATE0 = datetime(2015, 7, 16, 0, 0)

# Number of dats to plot
N_days = 650

# Generate list of files to pull
dateString = [DATE0] * N_files
for i in range(N_files):
    if i > 0:
        dateString[i] = dateString[i-1] + timedelta(days=30)
            
# Initialize the variables
C_DATE = dict(); C_RESTLESS = dict(); C_AWAKE = dict(); C_ASLEEP = dict()
S_DATE = dict(); S_DEEP = dict(); S_WAKE = dict(); S_LIGHT = dict()
S_REM = dict(); C_START = dict(); C_END = dict(); S_START = dict()
S_END = dict(); CLASSIC_DICT = dict(); STAGES_DICT = dict()

# --------------------------- READ THE DATA --------------------------------- #

# Open the datas
for i in range(N_files):
    with open('sleep-' + dateString[i].strftime("%Y-%m-%d") + '.json') as f:
        data = json.load(f)
    
    #pprint(data)
    
    # Pull out sleep level summaries for each day
    for j in range(len(data)):
        
        if data[j]['type'] == 'classic':
            C_DATE[j+30*i] = data[j]['dateOfSleep']
            C_RESTLESS[j+30*i] = data[j]['levels']['summary']['restless']['minutes']
            C_AWAKE[j+30*i] = data[j]['levels']['summary']['awake']['minutes']
            C_ASLEEP[j+30*i] = data[j]['levels']['summary']['asleep']['minutes']
            startTIME = str.split(data[j]['startTime'],"T")[1]
            C_START[j+30*i] = datetime.strptime(startTIME,"%H:%M:%S.%f").strftime("%H:%M:%S") 
            endTIME = str.split(data[j]['endTime'],"T")[1]
            C_END[j+30*i] = datetime.strptime(endTIME,"%H:%M:%S.%f").strftime("%H:%M:%S") 
            
        if data[j]['type'] == 'stages': 
            S_DATE[j+30*i] = data[j]['dateOfSleep']
            S_DEEP[j+30*i] = data[j]['levels']['summary']['deep']['minutes']
            S_WAKE[j+30*i] = data[j]['levels']['summary']['wake']['minutes']
            S_LIGHT[j+30*i] = data[j]['levels']['summary']['light']['minutes']
            S_REM[j+30*i] = data[j]['levels']['summary']['rem']['minutes']
            startTIME = str.split(data[j]['startTime'],"T")[1]
            S_START[j+30*i] = datetime.strptime(startTIME,"%H:%M:%S.%f").strftime("%H:%M:%S") 
            endTIME = str.split(data[j]['endTime'],"T")[1]
            S_END[j+30*i] = datetime.strptime(endTIME,"%H:%M:%S.%f").strftime("%H:%M:%S") 

CLASSIC = [C_DATE,C_AWAKE,C_RESTLESS,C_ASLEEP,C_START,C_END]
CLASSIC_df = pd.concat([pd.Series(d) for d in CLASSIC], axis=1).fillna(0).reset_index()

STAGES = [S_DATE,S_WAKE,S_DEEP,S_LIGHT,S_REM,S_START,S_END]
STAGES_df = pd.concat([pd.Series(d) for d in STAGES], axis=1).fillna(0).reset_index()

# Save out .csv files with the sleep data for debugging
CLASSIC_df.to_csv("classic_sleep.csv")
STAGES_df.to_csv("stages_sleep.csv")

STAGES_df = STAGES_df.sort_values(0)
        
# --------------------------- PLOT THE DATA --------------------------------- #

fig, ax1 = plt.subplots(figsize = (8,20),dpi=100)
ax1.grid(zorder=0,alpha=0.35)

for n in range(N_days):
    
    if datetime.strptime(STAGES_df[5][n],"%H:%M:%S").hour < 12:
        startP = datetime.strptime(STAGES_df[5][n],"%H:%M:%S") + timedelta(days=1)
    else:
        startP = datetime.strptime(STAGES_df[5][n],"%H:%M:%S")
        
    if datetime.strptime(STAGES_df[5][n],"%H:%M:%S").hour >= 3 and datetime.strptime(STAGES_df[5][n],"%H:%M:%S").hour <= 7:   
        startP = datetime(1900, 1, 2, 1, 0)
        

    endP = datetime.strptime(STAGES_df[6][n],"%H:%M:%S") + timedelta(days=1)
    
    yval = [N_days - n, N_days - n]
    xval = [startP, endP]
    
    ax1.plot_date(pd.to_datetime(xval),yval,"-",color="k",zorder =3)

ax1.xaxis.set_major_formatter(DateFormatter('%#I %p'))
ax1.set_xlim([datetime(1900, 1, 1, 21, 0), datetime(1900, 1, 2, 10, 0)])
ax1.xaxis.set_major_locator(HourLocator(np.arange(0,24,1)))
ax1.set_ylim([0,N_days])
ax1.set_yticks(np.arange(0,N_days+1,50))
ax1.set_xlabel("Time")

#fig.suptitle("2 Years of Sleep Data From Fitbit Charge 2", weight="bold",size=16)
#fig.tight_layout(rect=[0, 0.0, 1, 0.975])


plt.savefig('outputPLOT.png')
        