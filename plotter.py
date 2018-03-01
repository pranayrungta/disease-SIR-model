from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import core

sir_title = lambda t,s,i,r: f'Time={t}      S={s:.2f}   I={i:.2f}   R={r:.2f}'

def set_pop(singleInfected,size,fs,fi):
    global population
    if singleInfected:
        population = core.singleinfectedpop(size,fs)
    else: population = core.fracinfectedpop(size,fi)

def set_range(longrange, is_nbrs_4, p, f):
    global popRange
    if longrange: popRange = core.LongRangePop(population,is_nbrs_4,p,f)
    else: popRange = core.ShortRangePop(population,is_nbrs_4)

def plotinitialpop():
    from matplotlib.colors import ListedColormap, BoundaryNorm
    from core import Ti,Tr
    rows,cols = population.shape
    total = (rows-2)*(cols-2) 
    title = sir_title(0,*(core.census(population)/total))    
    fig = plt.figure(figsize=[6, 6])
    canvas = FigureCanvasQTAgg(fig)
    plt.xlim(0,cols-1); plt.ylim(0,rows-1)
    plt.title( title )
    cmap = ListedColormap(['g','r','k'])
    norm = BoundaryNorm(  [ 0,  1,  Ti+1,  Ti+Tr+1], cmap.N)
    plt.imshow(population, interpolation='none', cmap=cmap, norm=norm)
    plt.vlines(np.arange(0.5,cols-1),ymin=0,ymax=cols-1,color='w',lw=0.5)
    plt.hlines(np.arange(0.5,rows-1),xmin=0,xmax=rows-1,color='w',lw=0.5)
    canvas.show()
    

def plottimeseries(ti,tf):
    data = []
    popRange.jumptostep(ti)
    current_census = [None, None, None]
    while popRange.time<tf and current_census[0]!=popRange.total:
        popRange.updatepop()
        current_census = core.census(popRange.currentpop)
        data.append([popRange.time,*(current_census/popRange.total)])
        perCom = (popRange.time-ti)/(tf-ti)*100
        print(f'\r {perCom:.0f}% Done  ', end='')
    print(f'\r {100:.0f}% Done  \r', end='')
    data=np.reshape(data, newshape=(len(data),4))
    
    fig = plt.figure(); fig.clear()
    canvas = FigureCanvasQTAgg(fig)
    plt.plot(data[:,0],data[:,1],'g-',lw=2,label='Susceptible')
    plt.plot(data[:,0],data[:,2],'r-',lw=2,label='Infected')
    plt.plot(data[:,0],data[:,3],'k-',lw=2,label='Refractory')
    plt.title( sir_title(*data[-1,:]) )
    plt.legend()
    canvas.show()

class Population_visual:
    def __init__(self):
        global popRange
        self.data = np.zeros(shape=(0,6))
        rows,cols = popRange.currentpop.shape
        self.current_census = core.census(popRange.currentpop)

        self.fig = plt.figure(figsize=[12, 6])
        self.canvas = FigureCanvasQTAgg(self.fig)

        self.axes = list()
        self.axes.append( self.fig.add_subplot(121) )
        self.axes.append( self.fig.add_subplot(222) )
        self.axes.append( self.fig.add_subplot(224) )
        
        ax0 = self.axes[0]
        from matplotlib.colors import ListedColormap, BoundaryNorm
        from core import Ti,Tr
        cmap = ListedColormap(['g','r','k'])
        norm = BoundaryNorm(  [ 0,  1,  Ti+1,  Ti+Tr+1], cmap.N)
        self.im = ax0.imshow(popRange.currentpop, interpolation='none',
                             cmap=cmap, norm=norm)
        ax0.vlines(np.arange(0.5,cols-1),ymin=0,ymax=cols-1,color='w',lw=0.5)
        ax0.hlines(np.arange(0.5,rows-1),xmin=0,xmax=rows-1,color='w',lw=0.5)
        ax0.set_xlim(0, rows-1); ax0.set_ylim(0, cols-1)

        ax1 = self.axes[1]
        self.ln = list()
        self.ln.append(ax1.plot([], [], 'g', lw=2, label='Susceptible')[0])
        self.ln.append(ax1.plot([], [], 'r', lw=2, label='Infected')[0])
        self.ln.append(ax1.plot([], [], 'k', lw=2, label='Refractory')[0])
        ax1.set_ylim(0.0, 1.0)
        ax1.set_title('Time Series\t' + r'$\tau_{i}$=%i    '%core.Ti +
                       r'$\tau_{r}$=%i     nbrs=%i'%(core.Tr,len(popRange.nbrs) ) )
        ax2 = self.axes[2]
        self.ln.append(ax2.plot([], [], lw=2)[0])
        ax2.set_ylim(-3, 3)
        ax2.set_title(r'Order Parameter |$\frac{1}{N}\Sigma e^{i\phi}|$')
        
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
        popRange.jumptostep(ti)
        self.fig.tight_layout()
        line_ani = animation.FuncAnimation(self.fig, self.update, (tf-ti-1),
                                           interval=delay*1000, repeat=False)
        self.canvas.draw()
        self.canvas.show()

def animate(ti, tf, delay):
    cnvs = Population_visual()
    cnvs.animate(ti, tf, delay)
