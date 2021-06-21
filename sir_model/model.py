import numpy as np
from sir_model.core import (singleinfectedpop, fracinfectedpop,
                            LongRangePop, ShortRangePop, census)

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

    # def set_short_range(self, is_nbrs_4):
    #     self.popRange = ShortRangePop(self.population,is_nbrs_4)

    def time_series_data(self, ti, tf):
        data = []
        self.popRange.jumptostep(ti)
        current_census = [None, None, None]
        while self.popRange.time<tf and current_census[0]!=self.popRange.total:
            self.popRange.updatepop()
            current_census = census(self.popRange.currentpop)
            data.append([self.popRange.time,*(current_census/self.popRange.total)])
            perCom = (self.popRange.time-ti)/(tf-ti)*100
            print(f'{perCom:.0f}% Done  ', end='\r')
        print(f'{100:.0f}% Done  ', end='\r')
        data=np.reshape(data, newshape=(len(data),4))
        return data

    def animation_data(self):
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
                self.animation_data)

if __name__=='__main__':
    m = Model()
    nbrs, pop, updater = m.get_anim_updater()


