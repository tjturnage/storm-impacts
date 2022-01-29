import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pylab as plt

fin = 'C:/data/131_96_interchange/131_96_interchange.csv'

D = pd.read_csv(fin, index_col=['measurement_tstamp'],parse_dates=True)
D['ratio'] = D['average_speed']/D['reference_speed']

fig, ax = plt.subplots(nrows = 1, ncols = 1)
for x in D.tmc_code.unique():
    E = D[(D.index.dayofyear >= 1) & (D.index.dayofyear <= 365) &  (D.tmc_code == x) & (D.cvalue > 60)]
    #E = D
    #tt = E['travel_time_seconds'].plot()
    try:
        tt = E['travel_time_minutes']
    except:
        tt = E['travel_time_seconds']
    sr = E['ratio']
    avg_sp =  E['average_speed']
    #myFmt = mdates.DateFormatter('%Y-%m-%d\n%a %H Z')
    myFmt = mdates.DateFormatter('%H:%M')
    ax.plot(avg_sp,color='b',linewidth=1,label='tt')
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_title(x)
    #myFmt2 = mdates.DateFormatter('%H UTC')


    plt.show()
    plt.close()