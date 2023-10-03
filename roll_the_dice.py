import numpy as np
from matplotlib import pyplot as plt

## roll a die (one dice) N times
def dice(N=1):
    import random
    out=[]
    for i in range(N):
        out.append(random.randrange(1,7))
    return out


## roll it once
die=dice(1)
print(die)

## roll it N times
N=10000
die=dice(N)
print(die)

## make a histogram to check that the outcomes are (more or less) equally likely
plt.hist(die)
plt.show()

## we can also make an estimate of the probability
for face in range(1,7):
    print("Probability of getting " + str(face) + " was " + str(sum([i==face for i in die])/N))

