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
    sus,inf,ref = core.sus_inf_ref(population)
    rows,cols = population.shape
    total = (rows-2)*(cols-2) 
    title = sir_title(0,*(core.census(population)/total))
    
    fig = plt.figure(figsize=[6, 6])
    canvas = FigureCanvasQTAgg(fig)
    plt.xlim(0,cols-1); plt.ylim(0,rows-1)
    plt.title( title ); ms = ( 100/(rows-2) )*3
    plt.plot(sus[:, 0], sus[:, 1], 'gs', markersize=ms)
    plt.plot(inf[:, 0], inf[:, 1], 'rs', markersize=ms)
    plt.plot(ref[:, 0], ref[:, 1], 'ks', markersize=ms)
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
        self.p = list()
        
        ax0 = self.axes[0]; ms=3.1*100/(rows-2)
        self.p.append(ax0.plot([],[],'gs',markersize=ms,label='Susceptible')[0])
        self.p.append(ax0.plot([],[],'rs',markersize=ms,label='Infected')[0])
        self.p.append(ax0.plot([],[],'ks',markersize=ms,label='Refractory')[0])
        ax0.set_xlim(0, rows-1); ax0.set_ylim(0, cols-1)

        ax1 = self.axes[1]
        self.p.append(ax1.plot([], [], 'g', lw=2, label='Susceptible')[0])
        self.p.append(ax1.plot([], [], 'r', lw=2, label='Infected')[0])
        self.p.append(ax1.plot([], [], 'k', lw=2, label='Refractory')[0])
        ax1.set_ylim(0.0, 1.0)
        ax1.set_title('Time Series\t' + r'$\tau_{i}$=%i    '%core.Ti +
                       r'$\tau_{r}$=%i     nbrs=%i'%(core.Tr,len(popRange.nbrs) ) )
        ax2 = self.axes[2]
        self.p.append(ax2.plot([], [], lw=2)[0])
        ax2.set_ylim(-3, 3)
        ax2.set_title(r'Order Parameter |$\frac{1}{N}\Sigma e^{i\phi}|$')
        
    def update_lines(self):
        popRange.updatepop()
        sus, inf, ref = core.sus_inf_ref(popRange.currentpop)
        self.current_census = core.census(popRange.currentpop)
        census_frac = self.current_census/popRange.total
        self.data = np.vstack((self.data, [popRange.time,*census_frac,
                                           *popRange.hamming_dist()]))
        self.p[0].set_data(sus[:,0], sus[:,1])
        self.p[1].set_data(inf[:,0], inf[:,1])
        self.p[2].set_data(ref[:,0], ref[:,1])
        self.p[3].set_data(self.data[:,0], self.data[:,1])
        self.p[4].set_data(self.data[:,0], self.data[:,2])
        self.p[5].set_data(self.data[:,0], self.data[:,3])
        self.p[6].set_data(self.data[:,0], self.data[:,5])
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
