import numpy as np

Ti=4;  Tr=10

def traverse(population):
    rows, cols = population.shape
    for i in range(1,rows-1):
        for j in range(1, cols-1):
            yield i, j, population[i,j]

def rand(size):
    a = np.random.rand(size,size)
    a[ :, 0 ] = 1
    a[ :, -1] = 1
    a[ 0, : ] = 1
    a[-1, : ] = 1
    return a

def singleinfectedpop(size, fs):
    mat = np.full((size, size), Ti+1, dtype=int) # refractory
    a = rand(size)
    mat[a<fs] = 0  # suseptible
    x,y = np.random.randint(1,size-1,2)
    mat[x,y] = 1  #infected
    return mat

def fracinfectedpop(size, fs):
    mat = np.full((size, size), Ti+1, dtype=int) # refractory
    a = rand(size)
    sus = a<fs # say fs => <0.3
    inf = (~sus) & (a<1-fs)# say  0.3 < inf < 0.7
    mat[sus] = 0
    mat[inf] = 1
    return mat

def census(population):
    mat = population[1:-1, 1:-1]
    sus = (mat==0).sum()
    inf = ((0<mat) & (mat<=Ti)).sum()
    ref = (mat>Ti).sum()
    rows,cols = population.shape
    total = (rows-2)*(cols-2)
    frac = np.array([sus, inf, ref])/total
    return frac


class Population(object):
    def __init__(self, initpop, is_nbrs_4):
        self.initpop = initpop
        self.currentpop = initpop.copy()
        self.tpop = initpop.copy()
        self.nbrs = self.get_nbr_list(is_nbrs_4)
        rows, cols = initpop.shape
        self.total = (rows-2)*(cols-2)
        self.time = 0

    def get_nbr_list(self,is_nbrs_4):
        if is_nbrs_4: return [[1,0], [-1,0], [0,1], [0,-1]]
        else: return [[-1,-1], [0,-1], [1,-1],
                      [-1, 0],         [1, 0],
                      [-1, 1], [0, 1], [1, 1]]

    def hamming_dist(self):
        from numpy import pi, exp, absolute
        a = self.currentpop[1:-1,1:-1]
        theta = 2*pi*(a-1)/(Ti+Tr)
        phase = exp(1j*theta)
        phase = (phase[a!=0].sum() + phase.sum())/self.total
        hammdist = (self.currentpop - self.initpop).sum()/self.total
        return hammdist, absolute(phase)


    def jumptostep(self, t):
        self.currentpop = self.initpop.copy()
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
        fs, fi, fr = census(self.currentpop)
        return self.currentpop, self.time, fs, fi, fr

class ShortRangePop(Population):
    def __init__(self, initpop, nbrs=4):
        super().__init__(initpop, nbrs)

    def susUpdate(self,i,j):
        if any(0<self.currentpop[i+m,j+n]<=Ti
               for [m,n] in self.nbrs):
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

if __name__=='__main__':
    s = singleinfectedpop(10,0.5)
    p = ShortRangePop(s)
