import numpy as np
from sir_model.core import (singleinfectedpop, fracinfectedpop,
                            LongRangePop, ShortRangePop,
                            census, Ti, Tr)

class Model:
    def __init__(self):
        self.population = singleinfectedpop(5, 0.5)
        self.popRange = ShortRangePop(self.population, True)
        self.data = np.zeros(shape=(0,6))

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
        current_census = [None, None, None]
        while self.popRange.time<tf:
            self.popRange.updatepop()
            current_census = census(self.popRange.currentpop)
            data.append([self.popRange.time,*(current_census/self.popRange.total)])
        data=np.reshape(data, newshape=(len(data),4))
        return data

    def anim_updates(self):
        currentpop = self.popRange.currentpop
        self.popRange.updatepop()
        current_census = census(currentpop)
        census_frac = current_census/self.popRange.total
        self.data = np.vstack((self.data,
           [self.popRange.time, *census_frac,
            *self.popRange.hamming_dist() ]  ))
        return currentpop, self.data, self.popRange.time, census_frac

    def get_anim_updater(self, ti=0):
        import numpy as np
        self.popRange.jumptostep(ti)
        self.data = np.zeros(shape=(0,6))
        return (len(self.popRange.nbrs), self.popRange.currentpop,
                Ti, Tr, self.anim_updates)

if __name__=='__main__':
    m = Model()
    nbrs, pop, Ti, Tr, updater = m.get_anim_updater()
    pop, ts, t, census_frac = updater()
