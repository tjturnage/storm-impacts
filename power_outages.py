# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
import os
import re
import pandas as pd
#import matplotlib.pyplot as plt
import matplotlib.pylab as plt
import seaborn as sns
import numpy as np
import matplotlib.dates as mdates



total = []
p = re.compile('\d{12}')
v = re.compile('\d')

# Use seaborn style defaults and set the default figure size
sns.set(rc={'figure.figsize':(11, 4)})


def parse_html_file(fname):
    m = p.search(fname)
    dt_str = str(m.group(0))
    html = open(fname).read()
    soup = BeautifulSoup(html,features="html.parser")
    table = soup.find("table")
    for table_row in table.findAll('tr'):
        row = []
        columns = table_row.findAll('td')

        row.append(pd.to_datetime(dt_str))
        for column in columns:
            if len(column.text) > 0:
                mv = v.search(column.text)
                if mv is not None:
                    row.append(locale.atoi(column.text))
                else:
                    row.append(column.text)
                    if column.text in counties_dict:
                        row.append(counties_dict[column.text])

        total.append(row)
    return

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



try:
    os.listdir('/usr')
    base_dir = '/data'
except:
    base_dir = 'C:/data/events/20201115/outages'

process_files = True

src_dir = base_dir
fileList = os.listdir(src_dir)


if __name__ == "__main__":
    # execute only if run as a script

    import locale
    locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' ) 
    if process_files:
        for item in fileList:
            if 'html' in item:
                parse_html_file(os.path.join(base_dir,item))


# =============================================================================
# 
# 
D = None
D = pd.DataFrame(total, columns=['time', 'county', 'cwa', 'tracked', 'outages'])
D.set_index(list(D)[0], inplace=True)
D.dropna(inplace=True)
D['ratio'] = (D.outages/D.tracked) * 100
#D['log'] = np.log10(D.outages)
F = D.replace([np.inf, -np.inf], 0)

# # # Nov 15, 2020 = 320
# # #E = F[(F.index.dayofyear > 329) & (F.index.dayofyear <334)]
E = F[(F.index.dayofyear >= 320) & (F.index.dayofyear <= 322)]
df_e = E.resample('H').sum()
df_e_outages = df_e['outages']
# # 
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
ax.plot(df_e_outages,color='black', linewidth=2.5,ls='--',label='ALL', zorder=4)
ax.plot(df_grr_outages,color='r',linewidth=1.75,label='GRR', zorder=3)
ax.plot(df_dtx_outages,color='b',linewidth=1,label='DTX', zorder=2)
ax.plot(df_apx_outages,color='g',label='APX', zorder=1)
ax.plot(df_iwx_outages,color='m',label='IWX')
ax.legend()
plt.ylabel('Outages')
myFmt = mdates.DateFormatter('%d%b%y\n%HZ')
myFmt2 = mdates.DateFormatter('%H UTC')
ax.xaxis.set_major_formatter(myFmt)
ax.xaxis.grid(True, which='minor')
ax.xaxis.set_minor_formatter(myFmt2)
plt.title('Customer Outages')

image_dst_path = 'C:\data\outages-20201115.png'
plt.savefig(image_dst_path,format='png')
plt.show()
plt.close()


# =============================================================================
