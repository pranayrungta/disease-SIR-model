from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

def sir_title(t,s,i,r):
    return f'Time={t}      S={s:.2f}   I={i:.2f}   R={r:.2f}'

def pop_image(axes, pop, Ti, Tr):
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap(['g','r','k'])
    norm = BoundaryNorm(  [ 0,  1,  Ti+1,  Ti+Tr+1], cmap.N, clip=True)
    im = axes.imshow(pop, interpolation='none', cmap=cmap, norm=norm)
    rows,cols = pop.shape
    axes.vlines(np.arange(0.5,cols-1),ymin=0,ymax=rows-1,color='w',lw=0.5)
    axes.hlines(np.arange(0.5,rows-1),xmin=0,xmax=cols-1,color='w',lw=0.5)
    axes.set_xlim(0,cols-1); axes.set_ylim(0,rows-1)
    return im

def plotinitialpop(population, census, Ti, Tr):
    fig = Figure(figsize=[6, 6])
    canvas = FigureCanvasQTAgg(fig)
    canvas.setWindowTitle('Initial Population')
    axes = fig.add_subplot(111)
    rows,cols = population.shape
    total = (rows-2)*(cols-2)
    axes.set_title( sir_title(0,*(census/total)) )
    pop_image(axes, population, Ti, Tr)
    canvas.show()

def timeSeriesLines(axes, data):
    l, = axes.plot(data[:,0], data[:,1], 'g-', lw=2, label='Susceptible')
    m, = axes.plot(data[:,0], data[:,2], 'r-', lw=2, label='Infected'   )
    n, = axes.plot(data[:,0], data[:,3], 'k-', lw=2, label='Refractory' )
    return [ l, m, n ]

def plot_time_series(data):
    fig = Figure()
    canvas = FigureCanvasQTAgg(fig)
    canvas.setWindowTitle('Time series')
    axes = fig.add_subplot(111)
    timeSeriesLines(axes, data)
    axes.set_title( sir_title(*data[-1,:]) )
    axes.legend()
    canvas.show()

class Population_visual:
    def __init__(self, nbrs, currentpop, Ti, Tr):
        self.fig = Figure(figsize=[12, 6])
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setWindowTitle('Time evolution')
        self.axes = list()
        self.axes.append( self.fig.add_subplot(121) )
        self.axes.append( self.fig.add_subplot(222) )
        self.axes.append( self.fig.add_subplot(224) )

        self.im = pop_image(self.axes[0], currentpop, Ti, Tr)
        self.ln = timeSeriesLines(self.axes[1], np.zeros(shape=(0,6)))
        self.ln.append( *self.axes[2].plot([],[],lw=2) )
        self.axes[1].set_ylim(0.0, 1.0)
        tau_i = r'$\tau_{i}$=%i'%Ti
        tau_r = r'$\tau_{r}$=%i'%Tr
        nbrs = f'nbrs={nbrs}'
        self.axes[1].set_title(f'Time Series\t{tau_i}\t{tau_r}\t{nbrs}')
        self.axes[1].legend(loc='upper right')
        self.axes[2].set_ylim(-1, 3)
        ham_dist_phase = r'|$\frac{1}{N}\Sigma e^{i\phi}$|'
        self.axes[2].set_title(f'Order Parameter = {ham_dist_phase}')
        self.canvas.show()

    def update(self, i):
        currentpop, data, time, census_frac = self.updates_data()
        self.im.set_data(currentpop)
        self.ln[0].set_data(data[:,0], data[:,1])
        self.ln[1].set_data(data[:,0], data[:,2])
        self.ln[2].set_data(data[:,0], data[:,3])
        self.ln[3].set_data(data[:,0], data[:,5])
        self.axes[0].set_title( sir_title(time, *census_frac) )
        self.axes[1].set_xlim(data[0,0], data[-1,0]+1)
        self.axes[2].set_xlim(data[0,0], data[-1,0]+1)

    def animate(self, ti, tf, delay, animation_data):
        from matplotlib.animation import FuncAnimation
        self.fig.tight_layout()
        self.updates_data = animation_data
        line_ani = FuncAnimation(self.fig, self.update, (tf-ti-1),
                                 interval=delay*1000, repeat=False)
        self.canvas.draw()
        self.canvas.show()
