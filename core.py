import numpy as np

Ti=4;  Tr=10

def traverse(population):
    rows,cols = population.shape
    for i in range(1,rows-1):
        for j in range(1,cols-1):
            yield i,j,population[i,j]

def set_boundary(mat):
    rows,cols = mat.shape
    for i in range(rows):
        mat[i, 0] = Ti+1
        mat[i, cols-1] = Ti+1
    for j in range(cols):
        mat[0, j] = Ti+1
        mat[rows-1, j] = Ti+1

def singleinfectedpop(size, fs):
    a = np.random.rand(size,size)
    set_boundary(a)
    for i,j,aij in traverse(a):
        if aij<fs: a[i,j] = 0 # suseptible
        else: a[i,j] = Ti+1 # refractory
    x,y = np.random.randint(1,size-1,2)
    a[x,y] = 1  #infected
    return a

def fracinfectedpop(size, fi):
    a = np.random.rand(size, size)
    set_boundary(a)
    fs = (1-fi)/2
    for i,j,aij in traverse(a):
        if aij<fs: a[i,j] = 0   #suseptible
        elif aij<fi+fs: a[i,j] = 1   #infected
        else: a[i,j] = Ti+1  #refractory
    return a

def census(population):
    sus, inf, ref = 0, 0, 0
    for i,j,a_ij in traverse(population):
        if a_ij == 0: sus += 1
        elif a_ij <= Ti: inf += 1
        else: ref += 1
    return np.array([sus, inf, ref])

class Population(object):
    def __init__(self, initpop, is_nbrs_4):
        self.initpop = initpop
        self.currentpop = np.copy(initpop)
        self.tpop = np.copy(initpop)
        self.nbrs = self.get_nbr_list(is_nbrs_4)
        rows,cols = initpop.shape
        self.total = (rows-2)*(cols-2)
        self.time = 0

    def get_nbr_list(self,is_nbrs_4):
        if is_nbrs_4: return [[1,0], [-1,0], [0,1], [0,-1]]
        else: return [[-1,-1], [0,-1], [1,-1],
                      [-1, 0],         [1, 0],
                      [-1, 1], [0, 1], [1, 1]]

    def hamming_dist(self):
        phase = 0
        for i,j,a_ij in traverse(self.currentpop):
            theta = (2*np.pi)*(a_ij-1)/(Ti+Tr)
            phase += np.exp(1j*theta)
            if a_ij != 0 : phase += np.exp(1j*theta)
        phase /= self.total
        hammdist = np.sum(np.subtract(self.currentpop,self.initpop))/self.total
        return hammdist, np.absolute(phase)

    def jumptostep(self, t):
        self.currentpop = np.copy(self.initpop)
        self.time = 0
        for i in range(t):
            self.updatepop()

    def initinfnbrs(self):
        sus,ref = [],[]
        for i,j, a_ij in traverse(self.initpop):
            if 0 < a_ij < Ti+Tr:
                sus.append( sum(self.initpop[i+m,j+n]==0 
                                for [m,n] in self.nbrs) )
                ref.append( sum(Ti <self.initpop[i+m,j+n]<=Tr 
                                for [m,n] in self.nbrs) )
        return np.mean(sus)/len(self.nbrs),np.mean(ref)/len(self.nbrs)

    def updatepop(self):
        for i,j, a_ij in traverse(self.currentpop):
            if a_ij==0:
                self.tpop[i,j] = a_ij
                self.susUpdate(i,j)
            elif self.infCond(a_ij):
                self.tpop[i,j] = a_ij+1
            else: self.tpop[i,j] = 0
        self.currentpop, self.tpop = self.tpop, self.currentpop
        self.time += 1

class ShortRangePop(Population):
    def __init__(self, initpop, nbrs=4):
        super().__init__(initpop, nbrs)

    def susUpdate(self,i,j):
        if any(0<self.currentpop[i+m,j+n]<=Ti for [m,n] in self.nbrs):
            self.tpop[i,j] += 1

    def infCond(self,a_ij):
        return a_ij<Ti+Tr

class LongRangePop(Population):
    def __init__(self, initpop, nbrs=4, prob=0.1, freq=1):
        super().__init__(initpop, nbrs)
        self.prob = prob
        self.freq = freq

    def susUpdate(self,i,j):
        rows,cols = self.tpop.shape
        if np.random.rand()>self.prob or self.time%self.freq!=0:
            if any(0<self.currentpop[i+m,j+n]<=Ti for [m, n] in self.nbrs):
                self.tpop[i,j] += 1
        else:
            shuffled_nbrs = np.copy(self.nbrs)
            np.random.shuffle(shuffled_nbrs)
            nbrs = False
            for m,n in shuffled_nbrs:
                if 0 < self.currentpop[i+m,j+n] <= Ti:
                    nbrs=True; break
                x,y = np.random.randint(1,rows-1,2)
                if 0 < self.currentpop[x,y] <= Ti:
                    nbrs=True; break
            if nbrs:self.tpop[i,j] += 1

    def infCond(self,a_ij):
        return (a_ij<Ti+Tr or self.time%self.freq!=0)

class LongRangePop1(Population):
    def __init__(self, initpop, nbrs=4, prob=0.1,freq = 1):
        super().__init__(initpop, nbrs)
        self.prob = prob
        self.freq = freq

    def susUpdate(self,i,j):
        rows,cols = self.tpop.shape
        nbrs = False
        for m,n in self.nbrs:
            if np.random.rand()<self.prob and self.time%self.freq==0:
                x,y = np.random.randint(1,rows-1,2)
                if 0<self.currentpop[x,y]<=Ti:
                    nbrs = True; break
            elif 0<self.currentpop[i+m,j+n]<=Ti:
                    nbrs = True; break
        if nbrs:self.tpop[i,j] += 1

    def infCond(self,a_ij):
        return (a_ij<Ti+Tr or self.time%self.freq!=0)

class VisitorPop(Population):
    def __init__(self, initpop, nbrs=4, prob=0.1, freq=1):
        super().__init__(initpop, nbrs)
        self.prob = prob
        self.freq = freq

    def susUpdate(self,i,j):
        if np.random.rand() > self.prob:
            if any(0<self.currentpop[i+m,j+n]<=Ti for [m,n] in self.nbrs):
                self.tpop[i,j] += 1
        else:
            x,y = np.random.randint(1,self.popdims[0]+1,2)
            if any(0<self.currentpop[x+m,y+n]<=Ti for [m,n] in self.nbrs):
                self.tpop[i,j] += 1

    def infCond(self,a_ij):
        return a_ij<Ti+Tr
