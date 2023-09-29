## code to read data from Socialstyrelsen into a pandas dataframe
## and plot it

import pandas as pd
import json
import urllib.request

from matplotlib import pyplot as plt
import numpy as np


## SoS has an API that we can use to fetch data from the databases
## See: https://sdb.socialstyrelsen.se/sdbapi.aspx (in Swedish)


## preamble to replace the age indices with actual age range
url="http://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/alder"
agevar=pd.read_json(url)
agevar=dict(zip(agevar['id'],agevar['text']))


## for example, let's look deaths deemed to be suicides (code is 2026)
url="http://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/resultat/matt/1/diagnos/2026/region/0/kon/1,2"
## here "matt" (mått, measure in Swedish) is set to "1" which returns counts
## "diagnos" decides which diagnosis to return results for (2026 is suicides)
## "region" is set to 0 which means the whole of Sweden
## "kon" is sex (1=men, 2=women)

dat=pd.read_json(url)

## reshape the data into a pandas datafram
df=pd.DataFrame(dat['data'].to_list())
## create a variable that has the right format
df['antal']=df['varde'].apply(pd.to_numeric)

## change the values for sex
df.loc[df["konId"]==1,'konId']="men"
df.loc[df["konId"]==2,'konId']="women"

## sum over age groups
gdf=pd.DataFrame(df.groupby(['ar','konId'])['antal'].sum())

dum = gdf.pivot_table(index='ar', columns='konId', values=['antal'])
##dum.columns=dum.columns.map(','.join)
ax=dum.plot(marker="*")
ax.set(xlabel="year", ylabel="number of cases")
ax.legend(['men','women'])
plt.title("Suicides, all ages")
plt.grid()
plt.show()


###########################################################3
### plot data as a function of age group instead

url="http://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/resultat/matt/2/diagnos/2026/region/0/kon/1,2"
## C-19
##url="http://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/resultat/matt/2/diagnos/U07/region/0/kon/1,2"
dat=pd.read_json(url)
## X42
##url="http://sdb.socialstyrelsen.se/api/v1/sv/dodsorsaker/resultat/matt/2/diagnos/X42/region/0/kon/1,2"
##dat=pd.read_json(url)

## reshape the data into a pandas dataframe
df=pd.DataFrame(dat['data'].to_list())
df['varde']=df['varde'].str.replace(",",".")
## create a variable that has the right format
df['andel']=df['varde'].apply(pd.to_numeric)/100

## change the values for sex
df.loc[df["konId"]==1,'konId']="men"
df.loc[df["konId"]==2,'konId']="women"

gdf=pd.DataFrame(df.groupby(['alderId','konId'])['andel'].mean())
dum = gdf.pivot_table(index='alderId', columns='konId', values=['andel'])
dum=dum.assign(age=[agevar[i] for i in dum.index])

plt.rc('axes', titlesize=12) 
plt.rc('axes', labelsize=12) 

dum.columns=dum.columns.map(','.join)
ax=dum.plot(x="age,",kind="bar")
##ax=ddum.plot(kind="bar")
ax.set(xlabel="age,", ylabel="cases per 1000 people")
ax.legend(['men','women'])
plt.title("Suicides, average rates for 1997-2022")
plt.show()

#################################################3
## use PAR instead 

## F19, all age groups
url="http://sdb.socialstyrelsen.se/api/v1/sv/diagnoserislutenvard/resultat/matt/6/diagnos/F19/region/0/kon/1,2/alder/19"
##pd.set_option('display.max_rows', 100)
dat=pd.read_json(url)

df=pd.DataFrame(dat['data'].to_list())
df['antal']=df['varde'].apply(pd.to_numeric)
df.loc[df["konId"]==1,'konId']="men"
df.loc[df["konId"]==2,'konId']="women"
## sum over age groups
gdf=pd.DataFrame(df.groupby(['ar','konId'])['antal'].sum())

dum = gdf.pivot_table(index='ar', columns='konId', values=['antal'])
dum.columns=dum.columns.map(','.join)
ax=dum.plot(marker="*")
ax.set(xlabel="year", ylabel="number of cases")
ax.legend(['men','women'])
plt.title("Inpatient care under F19 diagnosis")
plt.grid()
plt.show()

