## simulate the escape from a potential

## Anders Ledberg

import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt

N = 100
etime = list()
dt = 0.1
T = 365*150
x = np.tile(0.0,T)
sqdt=np.sqrt(dt)
for n in range(N):
    x0=-1
    
    sigma = 2.5

    ## parameters controllong the height of the barrier
    beta=13
    x[0]=x0
    t = 1
    while (t < T):
        ## simple forward Euler
        beta=beta - 2.5e-4
        x[t] = x[t-1]+dt*(x[t-1]**2-beta)+sqdt*rnd.randn()*sigma
        if (x[t] > 5):
            break
        t = t+1
    etime.append(t/365.25)

plt.hist(etime,30)
plt.show()

print(np.mean(etime))

