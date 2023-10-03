## code to display the output of a simulation of a simple discrete SIR model 

## Anders Ledberg

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
from simEpi import simepi

######################################
N=50 ## size of grid
T=250 ## number of "days" to simulate
n_inits=5 ## number of individuals in the population who are infected at time 0
pr_s_to_i=0.1 ## probability of spreading the infection on each time step
pr_i_to_r=0.1 ## probability of recovery 
arr,sval,ival,rval,fval=simepi(nrow=N,ncol=N,nsteps=T,ninit=n_inits,stoi=pr_s_to_i,itor=pr_i_to_r)

## plot the data
##fig=plt.figure(figsize=(10,10))
fig=plt.figure()
frames=[]
for i in range(len(arr)):
    frames.append([plt.imshow(arr[i], cmap=cm.Greys_r,animated=True)])

ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True,repeat_delay=10)

ani
plt.show()
plt.close()

