# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
from datetime import datetime
import os
import pandas as pd
#import matplotlib.pyplot as plt
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})

# Updated: 9/12/2019 2:01:29 AM GMT
test_file = 'C:/data/outages/MIoutages201912040810.html'

def getDateTime(fh,fname):
    output = []
    try:
        html = open(fname).read()
        soup = BeautifulSoup(html,features="lxml")
        table = soup.find("table")
        raw_text = soup.get_text()
        data = raw_text.splitlines()
        output_rows = []
        for table_row in table.findAll('tr'):
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_rows.append(output_row)
    

        for d in range(0,(len(data))):
            if 'Updated' in data[d]:
                #print (data[d])
                dt_line = data[d]
                dtime = dt_line[9:]
                dt = datetime.strptime(dtime,'%m/%d/%Y %I:%M:%S %p GMT')
                #print(dt)
    
        for r in range(0,len(output_rows)):
            this_row = output_rows[r]
            if len(this_row) > 0:
                county = this_row[0]
                tracked = this_row[1].replace(',', '')
                outages = this_row[2].replace(',', '')
                if int(outages) > -1:
                    text = str(dt) + ',' + county + ',' + counties_dict[county] + ',' + tracked + ',' + outages + '\n'
                    #print(text)
                    fh.write(text)
        return output
    except:
        pass

try:
    os.listdir('/usr')
    base_dir = '/data'
except:
    base_dir = 'C:/data'


process_files = False
src_dir = os.path.join(base_dir,'outages')

fileList = os.listdir(src_dir)
outFile = os.path.join(base_dir,'outages4.txt')

if process_files:
    with open(outFile,'a') as fout:
        for item in fileList:
            if 'html' in item:
                #print(os.path.join(src_dir,item))
                output = getDateTime(fout,os.path.join(src_dir,item))
            else:
                pass
else:
    pass
        #thefile.write("%s\n" % item)


counties_dict = {'Allegan': 'grr',
 'Alpena': 'apx',
 'Antrim': 'apx',
 'Arenac': 'apx',
 'Barry': 'grr',
 'Bay': 'dtx',
 'Benzie': 'apx',
 'Berrien': 'grr',
 'Branch': 'iwx',
 'Calhoun': 'grr',
 'Charlevoix': 'apx',
 'Cheboygan': 'apx',
 'Clare': 'grr',
 'Clinton': 'grr',
 'Crawford': 'apx',
 'Eaton': 'grr',
 'Emmet': 'apx',
 'Genesee': 'dtx',
 'Gladwin': 'apx',
 'Grand Traverse': 'apx',
 'Gratiot': 'grr',
 'Hillsdale': 'iwx',
 'Huron': 'dtx',
 'Ingham': 'grr',
 'Ionia': 'grr',
 'Iosco': 'apx',
 'Isabella': 'grr',
 'Jackson': 'grr',
 'Kalamazoo': 'grr',
 'Kalkaska': 'apx',
 'Kent': 'grr',
 'Lake': 'grr',
 'Lapeer': 'dtx',
 'Leelanau': 'apx',
 'Lenawee': 'dtx',
 'Livingston': 'dtx',
 'Macomb': 'dtx',
 'Manistee': 'apx',
 'Mason': 'grr',
 'Mecosta': 'grr',
 'Midland': 'dtx',
 'Missaukee': 'apx',
 'Monroe': 'dtx',
 'Montcalm': 'grr',
 'Montmorency': 'apx',
 'Muskegon': 'grr',
 'Newaygo': 'grr',
 'Oakland': 'dtx',
 'Oceana': 'grr',
 'Ogemaw': 'apx',
 'Osceola': 'grr',
 'Oscoda': 'apx',
 'Otsego': 'apx',
 'Ottawa': 'grr',
 'Presque Isle': 'apx',
 'Roscommon': 'apx',
 'Saginaw': 'dtx',
 'Shiawassee': 'dtx',
 'St. Clair': 'dtx',
 'St. Joseph': 'iwx',
 'Tuscola': 'dtx',
 'Van Buren': 'grr',
 'Washtenaw': 'dtx',
 'Wayne': 'dtx',
 'Wexford': 'apx',
 'Alcona': 'apx'}



D = None
D = pd.read_csv(outFile, header=0, index_col=['time'],parse_dates=True,names=['time', 'county', 'cwa', 'tracked', 'outages'])
D['ratio'] = (D.outages/D.tracked) * 100
D['log'] = np.log10(D.outages)

F = D.replace([np.inf, -np.inf], 0)
# Jul 20,2019 = 201
# Sep 11,2019 = 254
# Nov. 25, 2019 = 329
# Nov 30, 2019 = 334 ... 334-338
E = F[(F.index.dayofyear > 329) & (F.index.dayofyear <334)]
df_e = E.resample('H').sum()
df_e_outages = df_e['outages']

GRR = E[E.cwa == 'grr']
df_grr = GRR.resample('H').sum()
df_grr_outages = df_grr['outages']

DTX = E[E.cwa == 'dtx']
df_dtx = DTX.resample('H').sum()
df_dtx_outages = df_dtx['outages']

APX= E[E.cwa == 'apx']
df_apx = APX.resample('H').sum()
df_apx_outages = df_apx['outages']

IWX= E[E.cwa == 'iwx']
df_iwx = IWX.resample('H').sum()
df_iwx_outages = df_iwx['outages']

fig, ax = plt.subplots(nrows = 1, ncols = 1)
ax.plot(df_dtx_outages,color='b',linewidth=1,label='DTX')
ax.plot(df_grr_outages,color='r',linewidth=1.75,label='GRR')
#ax.plot(df_apx_outages,color='g',label='APX')
#ax.plot(df_iwx_outages,color='m',label='IWX')
ax.plot(df_e_outages,color='black', linewidth=2.5,ls='--',label='ALL')
ax.legend()
plt.ylabel('Outages')
myFmt = mdates.DateFormatter('%Y-%m-%d\n%H UTC')
myFmt2 = mdates.DateFormatter('%H UTC')
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.grid(True, which='minor')
ax.xaxis.set_minor_formatter(myFmt2)
plt.title('Consumers Outages')
