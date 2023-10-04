## code by Luca Mingarelli, https://lucamingarelli.com/Teaching/schelling.html

## parameters
N = 60       # Grid will be N x N
SIM_T = 0.4  # Similarity threshold (that is 1-τ)
EMPTY = 0.1  # Fraction of vacant properties
B_to_R = 1   # Ratio of blue to red people

import numpy as np

def rand_init(N, B_to_R, EMPTY):
    """ Random system initialisation.
    BLUE  =  0
    RED   =  1
    EMPTY = -1
    """
    vacant = N * N * EMPTY
    population = N * N - vacant
    blues = int(population * 1 / (1 + 1/B_to_R))
    reds = population - blues
    M = np.zeros(N*N, dtype=np.int8)
    M[:int(reds)] = 1
    M[-int(vacant):] = -1
    np.random.shuffle(M)
    return M.reshape(N,N)


KERNEL = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]], dtype=np.int8)


from scipy.signal import convolve2d

def evolve(M, sim_T=SIM_T,boundary='wrap'):
    """
    Args:
        M (numpy.array): the matrix to be evolved
        boundary (str): Either wrap, fill, or symm
    If the similarity ratio of neighbours
    to the entire neighbourhood population
    is lower than the SIM_T,
    then the individual moves to an empty house.
    """
    print(sim_T)
    kws = dict(mode='same', boundary=boundary)
    B_neighs = convolve2d(M == 0, KERNEL, **kws)
    R_neighs = convolve2d(M == 1, KERNEL, **kws)
    Neighs   = convolve2d(M != -1,  KERNEL, **kws)

    B_dissatified = (B_neighs / Neighs < sim_T) & (M == 0)
    R_dissatified = (R_neighs / Neighs < sim_T) & (M == 1)
    M[R_dissatified | B_dissatified] = - 1
    vacant = (M == -1).sum()

    N_B_dissatified, N_R_dissatified = B_dissatified.sum(), R_dissatified.sum()
    filling = -np.ones(vacant, dtype=np.int8)
    filling[:N_B_dissatified] = 0
    filling[N_B_dissatified:N_B_dissatified + N_R_dissatified] = 1
    np.random.shuffle(filling)
    M[M==-1] = filling



######################################33
## here we run the model
N = 100       # Grid will be N x N
SIM_T = 0.3  # Similarity threshold (that is 1-τ)
EMPTY = 0.1  # Fraction of vacant properties
B_to_R = 1   # Ratio of blue to red people


import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.animation as animation
import mingarelli as lm ## for luca mingarelli
## show the initial random configuration
M=lm.rand_init(N,B_to_R,EMPTY)

##plt.imshow(M)
##plt.show()


## loop to evolve the system and make the graphics
frames=[]
niter=35
##fig=plt.figure()
fig=plt.figure(figsize=(10,10))
for i in range(niter):
    frames.append([plt.imshow(M, cmap=cm.Greys_r,animated=True)])
    ##frames.append([plt.imshow(M,animated=True)])
    lm.evolve(M,sim_T=SIM_T)

##plt.sca(frames[3][0])
##plt.plot(frames[3][0])
##plt.show()

##ani = animation.ArtistAnimation(fig, frames, interval=50, blit=True,repeat_delay=10)


ani = animation.ArtistAnimation(fig, frames, interval=1000, blit=True,repeat_delay=100,repeat=False)
##ani = animation.ArtistAnimation(fig, frames)

plt.show()
