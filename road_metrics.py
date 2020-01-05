# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pylab as plt

fin = 'C:/data/Polar-vortex2/Polar-vortex2.csv'
#fin = 'C:/data/granular2/granular2.csv'

D = pd.read_csv(fin, index_col=['measurement_tstamp'],parse_dates=True)
D['ratio'] = D['average_speed']/D['reference_speed']

E = D[(D.index.dayofyear >= 28) & (D.index.dayofyear <= 33) & (D.cvalue > 60)]

#tt = E['travel_time_seconds'].plot()
try:
    tt = E['travel_time_minutes']
except:
    tt = E['travel_time_seconds']
sr = E['ratio']
avg_sp =  E['average_speed']
fig, ax = plt.subplots(nrows = 1, ncols = 1)
myFmt = mdates.DateFormatter('%Y-%m-%d\n%a %H Z')
ax.plot(avg_sp,color='b',linewidth=1,label='tt')
#myFmt2 = mdates.DateFormatter('%H UTC')
ax.xaxis.set_major_formatter(myFmt)