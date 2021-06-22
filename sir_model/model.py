import numpy as np
from sir_model.core import (singleinfectedpop, fracinfectedpop,
                            LongRangePop, ShortRangePop,
                            census, Ti, Tr)

class Model:
    def __init__(self):
        self.population = singleinfectedpop(5, 0.5)
        self.popRange = ShortRangePop(self.population, True)
        self.data = np.zeros(shape=(0,5))

    def set_pop(self, singleInfected, size, fs):
        if singleInfected:
            self.population = singleinfectedpop(size, fs)
        else: self.population = fracinfectedpop(size, fs)

    def set_popRange(self, p):
        if p['longRange']:
            self.popRange = LongRangePop(self.population, p['nbr4'],
                                         p['p'], p['f'])
        else:
            self.popRange = ShortRangePop(self.population, p['nbr4'])

    def init_pop(self):
        current_census = census(self.population)
        return self.population, current_census, Ti, Tr

    def time_series_data(self, ti, tf):
        data = []
        self.popRange.jumptostep(ti)
        while self.popRange.time<tf:
            self.popRange.updatepop()
            fs, fi, fr = census(self.popRange.currentpop)
            data.append( [self.popRange.time, fs, fi, fr] )
        data = np.array(data)
        return data

    def anim_updates(self):
        self.popRange.updatepop()
        currentpop = self.popRange.currentpop
        t = self.popRange.time
        fs,fi,fr = census(currentpop)
        hdist, phase = self.popRange.hamming_dist()
        self.data = np.vstack((self.data, [t, fs,fi,fr, phase]))
        return currentpop, self.data

    def get_anim_updater(self, ti=0):
        import numpy as np
        self.popRange.jumptostep(ti)
        self.data = np.zeros(shape=(0,5))
        return (len(self.popRange.nbrs), self.popRange.currentpop,
                Ti, Tr, self.anim_updates)

if __name__=='__main__':
    m = Model()
    nbrs, pop, Ti, Tr, updater = m.get_anim_updater()
    pop, data = updater()
