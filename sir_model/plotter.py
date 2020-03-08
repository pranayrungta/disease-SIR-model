from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from . import core

sir_title = lambda t,s,i,r: f'Time={t}      S={s:.2f}   I={i:.2f}   R={r:.2f}'

def set_pop(singleInfected,size,fs):
    global population
    if singleInfected:
        population = core.singleinfectedpop(size, fs)
    else: population = core.fracinfectedpop(size, fs)

def set_long_range(is_nbrs_4, p, f):
    global popRange
    popRange = core.LongRangePop(population,is_nbrs_4,p,f)

def set_short_range(is_nbrs_4):
    global popRange
    popRange = core.ShortRangePop(population,is_nbrs_4)

def pop_image(axes, pop):
    from .core import Ti,Tr
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap(['g','r','k'])
    norm = BoundaryNorm(  [ 0,  1,  Ti+1,  Ti+Tr+1], cmap.N, clip=True)
    im = axes.imshow(pop, interpolation='none', cmap=cmap, norm=norm)
    rows,cols = pop.shape
    axes.vlines(np.arange(0.5,cols-1),ymin=0,ymax=rows-1,color='w',lw=0.5)
    axes.hlines(np.arange(0.5,rows-1),xmin=0,xmax=cols-1,color='w',lw=0.5)
    axes.set_xlim(0,cols-1); axes.set_ylim(0,rows-1)
    return im

def plotinitialpop():
    fig = Figure(figsize=[6, 6])
    canvas = FigureCanvasQTAgg(fig)
    canvas.setWindowTitle('Initial Population')
    axes = fig.add_subplot(111)
    rows,cols = population.shape
    total = (rows-2)*(cols-2)
    axes.set_title( sir_title(0,*(core.census(population)/total)) )
    pop_image(axes, population)
    canvas.show()


def timeSeriesLines(axes, data):
    l, = axes.plot(data[:,0], data[:,1], 'g-', lw=2, label='Susceptible')
    m, = axes.plot(data[:,0], data[:,2], 'r-', lw=2, label='Infected'   )
    n, = axes.plot(data[:,0], data[:,3], 'k-', lw=2, label='Refractory' )
    return [ l, m, n ]

def plot_time_series(ti,tf):
    data = []
    popRange.jumptostep(ti)
    current_census = [None, None, None]
    while popRange.time<tf and current_census[0]!=popRange.total:
        popRange.updatepop()
        current_census = core.census(popRange.currentpop)
        data.append([popRange.time,*(current_census/popRange.total)])
        perCom = (popRange.time-ti)/(tf-ti)*100
        print(f'{perCom:.0f}% Done  ', end='\r')
    print(f'{100:.0f}% Done  ', end='\r')
    data=np.reshape(data, newshape=(len(data),4))

    fig = Figure()
    canvas = FigureCanvasQTAgg(fig)
    canvas.setWindowTitle('Time series')
    axes = fig.add_subplot(111)
    timeSeriesLines(axes, data)
    axes.set_title( sir_title(*data[-1,:]) )
    axes.legend()
    canvas.show()

class Population_visual:
    def __init__(self):
        global popRange
        self.data = np.zeros(shape=(0,6))
        self.current_census = core.census(popRange.currentpop)
        self.fig = Figure(figsize=[12, 6])
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setWindowTitle('Time evolution')

        self.axes = list()
        self.axes.append( self.fig.add_subplot(121) )
        self.axes.append( self.fig.add_subplot(222) )
        self.axes.append( self.fig.add_subplot(224) )

        self.im = pop_image(self.axes[0], popRange.currentpop)
        self.ln = timeSeriesLines(self.axes[1], self.data)
        self.ln.append( *self.axes[2].plot([],[],lw=2) )
        self.axes[1].set_ylim(0.0, 1.0)
        tau_i = r'$\tau_{i}$=%i'%core.Ti
        tau_r = r'$\tau_{r}$=%i'%core.Tr
        nbrs = f'nbrs={len(popRange.nbrs)}'
        self.axes[1].set_title(f'Time Series\t{tau_i}\t{tau_r}\t{nbrs}')
        self.axes[1].legend(loc='upper right')
        self.axes[2].set_ylim(-1, 3)
        ham_dist_phase = r'|$\frac{1}{N}\Sigma e^{i\phi}$|'
        self.axes[2].set_title(f'Order Parameter = {ham_dist_phase}')

    def update_lines(self):
        popRange.updatepop()
        self.current_census = core.census(popRange.currentpop)
        census_frac = self.current_census/popRange.total
        self.data = np.vstack((self.data, [popRange.time,*census_frac,
                                           *popRange.hamming_dist()]))
        self.im.set_data(popRange.currentpop)
        self.ln[0].set_data(self.data[:,0], self.data[:,1])
        self.ln[1].set_data(self.data[:,0], self.data[:,2])
        self.ln[2].set_data(self.data[:,0], self.data[:,3])
        self.ln[3].set_data(self.data[:,0], self.data[:,5])
        self.axes[0].set_title( sir_title(popRange.time, *census_frac) )
        self.axes[1].set_xlim(self.data[0,0], self.data[-1,0]+1)
        self.axes[2].set_xlim(self.data[0,0], self.data[-1,0]+1)

    def update(self,i):
        if self.current_census[0]!=popRange.total:
            self.update_lines()

    def animate(self, ti, tf, delay):
        from matplotlib.animation import FuncAnimation
        popRange.jumptostep(ti)
        self.fig.tight_layout()
        line_ani = FuncAnimation(self.fig, self.update, (tf-ti-1),
                                 interval=delay*1000, repeat=False)
        self.canvas.draw()
        self.canvas.show()

def animate(ti, tf, delay):
    Population_visual().animate(ti, tf, delay)
