## function to simulate a three-state markov model with local connectivity
## 
## The units are allowed to be in three states:
## S - susseptible
## I - infected
## R - recovered/removed
## and can only transition from S -> I and from I -> R
## each unit can have it's own transition probability and
## connectivity. The default is to make transition probs the same
## and have local (8) connectivity (on a torus). 

## A. Ledberg 2021 08 05


import numpy as np


def simepi(nrow=20,ncol=20,stoi = 0.25,itor = 0.25, nsteps=100, ninit = 50, nneigh=8):
    ''' Simulate a three-state Markov model with 2D connectivity.
    
    Arguments: 
           nrow:   number of rows
           ncol:   number of columns
           stoi:   transition probability S -> I
           itor:   transition probability I -> R
           nsteps: number of "time" steps to simulate
           ninit:  number of units to start in the I state
           nneigh: number of neighbours
    Returns:
           outarray,sval,ival,rval,fval
           outarray: list with 2D arrays containing the unit states over time
           sval: sum of units in state S at time t
           ival: sum of units in state I at time t
           rval: sum of units in state R at time t
           fval: sum of units in that was initiated in I at time t
    '''
    ## Total number of units
    N=nrow*ncol
    v=list(range(N))
    
    ## convert linear index to rows and columns
    itorow=list(range(N))
    itocol=list(range(N))

    ## loop through v and find row and column
    for i in v:
        itorow[i]= int(i/ncol)
        itocol[i]=i%ncol

    ## Set up the connectivity. This is local and each unit is connected
    ## to a number of neighbours. at present only 8 (default) and 4 neighbours
    ## is implemented
    if ( (nneigh != 8 ) & (nneigh != 4 )):
        raise ValueError("number of neighbors must be 4 or 8")
    ## need a list with the neigbors of each unit
    neigh = [[0 for i in range(nneigh)] for j in range(N)]

    for i in v:
        if (nneigh==8):
            ## we do first the neighbors on the same row as i, i-1 and i+1
            neigh[i][0]= ((i - 1) % ncol) +itorow[i]*ncol
            ##    print( (i-1) % ncol)
            neigh[i][1]= ((i + 1) % ncol) +itorow[i]*ncol
            ##print( (i+1) % ncol)
            
            ## then neighbors on the row above 
            neigh[i][2]= ((i - 1) % ncol) +((itorow[i]-1) % nrow)*ncol
            neigh[i][3]= ((i) % ncol) +((itorow[i]-1) % nrow)*ncol
            neigh[i][4]= ((i+1) % ncol) +((itorow[i]-1) % nrow)*ncol
            
            ## then neighbors on the row below
            neigh[i][5]= ((i - 1) % ncol) +((itorow[i]+1) % nrow)*ncol
            neigh[i][6]= ((i) % ncol) +((itorow[i]+1) % nrow)*ncol
            neigh[i][7]= ((i+1) % ncol) +((itorow[i]+1) % nrow)*ncol
        else:
            ## we do first the neighbors on the same row as i, i-1 and i+1
            neigh[i][0]= ((i - 1) % ncol) +itorow[i]*ncol
            ##    print( (i-1) % ncol)
            neigh[i][1]= ((i + 1) % ncol) +itorow[i]*ncol
                       
            ## then neighbors on the row above 
            neigh[i][2]= ((i) % ncol) +((itorow[i]-1) % nrow)*ncol
            
            ## then neighbors on the row below
            neigh[i][3]= ((i) % ncol) +((itorow[i]+1) % nrow)*ncol

    ## Transition probability might later be allowed to vary
    ## so we allow them to be differnt 
    vstoi=np.zeros(N)+stoi
    vitor=np.zeros(N)+itor

    ## vector to hold the curren and next states of the units
    ## the states are coded as
    ## S == 0
    ## I == 1
    ## R == 2

    current = np.zeros(N,dtype="I")
    new = np.zeros(N,dtype="I")


    ## initialize by assigning a number of infected
    import numpy.random as rnd
    if ninit>1:
        indx = rnd.randint(0,N,ninit)
        current[indx]=1
    else:
        ## with only one starting point we might want to
        ## set that in the middle of the world
        indxr=[i for i,j in enumerate(itorow) if j==round(nrow/2)]
        indxc=[i for i,j in enumerate(itocol) if j==round(ncol/2)]
        indx=[set.intersection(set(indxc),set(indxr)).pop()]
        current[indx]=1
    ## initialize output variables
    sval=[]
    ival=[]
    rval=[]
    fval=[]
    outarray=[]

    for i in range(nsteps):
        sval.append(sum(current==0))
        ival.append(sum(current==1))
        rval.append(sum(current==2))
        fval.append(sum(current[indx]))
        iindx=np.where(current==1)[0]
        for u in iindx:
            ## this is now the units that are infectious
            
            ## check first if they will leave this state 
            new[u] = 1 + int(rnd.rand()< vitor[u])
        
            ## then we loop over neighbors that are still in state S
            ## and that has not already been switched to I
            nn=[n for n in neigh[u] if (current[n]==0 & new[n]==0)]
            for n in nn:
                ## check if we should switch this to 
                ## allow for hetrogeneity in transition rates
                new[n] = 0 + int(rnd.rand()< vstoi[u])
        
        ## save the data
        outarray.append(np.reshape(current,(nrow,ncol)))
        ## update states
        current = np.copy(new)


    ## return the data so computed
    return outarray,sval,ival,rval,fval

