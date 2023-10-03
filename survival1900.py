## read and look at mortality data from SDB7
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

## reset default values for font size
plt.rc('axes', titlesize=14) 
plt.rc('axes', labelsize=14) 

## read the file containing the date of birth and date of death of
## persons born 1900 who died in Sweden.

## The data comes from Sveriges Dödbok v7 published by the Swedish genealogical society
## 

## location of the dataset
url="https://raw.githubusercontent.com/aledberg/methodology/main/born1900.csv"
## read this into a pandas dataframe
dat=pd.read_csv(url)

## look at the first 10 entries
print(dat.head(10))

## convert string dates to datetime
dat['birthDate'] = pd.to_datetime(dat['birthDate'])
dat['deathDate'] = pd.to_datetime(dat['deathDate'])

## express the lifespan (age) in fractions of a year
dat['age']=((dat['deathDate']-dat['birthDate']).dt.days)/365.25

## make a histogram
ax=dat.hist('age',bins=100,grid=False,figsize=(12,8))
ax=ax[0][0]
ax.set(xlabel="age", ylabel="number of deaths")
plt.title("Lifespan of people born 1900")
plt.show()

## estimate probability of still being alive (survival function)

sortAge=dat['age'].sort_values()
nAlive=np.array([len(sortAge)-i for i in [*range(len(dat))]])
plt.plot(sortAge,nAlive)
plt.xlabel("age")
plt.ylabel("persons still alive")
plt.grid()
plt.figure(figsize=(12,8))
plt.show()

## if we divde with the total number we get the fraction who are still alive
nAlive=nAlive/len(nAlive)
plt.plot(sortAge,nAlive)
plt.xlabel("age")
plt.ylabel("probability of still being alive")
plt.title("Survival of persons born 1900")
plt.grid()
plt.show()

## we can compare men with women and see if survival differs
fig, ax = plt.subplots(figsize=(12,8))
## men
datm=dat[dat['sex']=="m"]
sortAge=datm['age'].sort_values()
nAlive=np.array([len(sortAge)-i for i in [*range(len(datm))]])
nAlive=nAlive/len(nAlive)
ax.plot(sortAge,nAlive)
## women
datw=dat[dat['sex']=="k"]
sortAge=datw['age'].sort_values()
nAlive=np.array([len(sortAge)-i for i in [*range(len(datw))]])
nAlive=nAlive/len(nAlive)
ax.plot(sortAge,nAlive)

plt.xlabel("age")
plt.ylabel("probability of still being alive")
plt.grid()
ax.legend(["men","women"])
plt.show()

## estimate the hazard rate (risk of dying in the next instance given you are still alive

## use simpel estimate, fraction of people dying during the next year
dat['rage']=dat['age'].round()
ndead=dat['rage'].value_counts()
ndead=ndead.sort_index()
ndead=[ i for i in ndead.values]
ndead.insert(0,0)
from itertools import accumulate
cndead=list(accumulate(ndead))

nalive=[len(dat)-i for i in cndead]
## here we calculate the hazard 
haz=[]
for i in range(len(ndead)):
    haz.append(ndead[i]/nalive[i])
plt.plot(haz)
plt.xlabel("age")
plt.ylabel("hazard rate (per year)")
plt.show()

## use a log-scale to demonstrate the exponential increase
plt.plot(haz)
plt.yscale("log")
plt.xlabel("age")
plt.ylabel("hazard rate (per year)")
plt.show()
