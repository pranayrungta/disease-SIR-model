from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg,
                                                NavigationToolbar2QT)
from matplotlib.figure import Figure
import PyQt5.QtWidgets as qt
import numpy as np

class PlotDialog(qt.QDialog):
    def __init__(self, width=5, height=4, title='Plot'):
        super().__init__()
        self.fig = Figure(figsize=(width, height))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.axes = self.fig.add_subplot(111)
        layout = qt.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.resize(int(width*100), int(height*100+30))

def _pop_image(axes, pop, Ti, Tr):
    from matplotlib.colors import ListedColormap, BoundaryNorm
    cmap = ListedColormap(['g','r','k'])
    norm = BoundaryNorm(  [ 0,  1,  Ti+1,  Ti+Tr+1], cmap.N, clip=True)
    im = axes.imshow(pop, interpolation='none', cmap=cmap, norm=norm)
    rows,cols = pop.shape
    axes.vlines(np.arange(0.5,cols-1),ymin=0,ymax=rows-1,color='w',lw=0.5)
    axes.hlines(np.arange(0.5,rows-1),xmin=0,xmax=cols-1,color='w',lw=0.5)
    axes.set_xlim(0,cols-1); axes.set_ylim(0,rows-1)
    return im

def plotInitialPop(population, census, Ti, Tr):
    pdg = PlotDialog(6.5,6.5,'Initial Population')
    tau_i = r'$\tau_{i}$=%i'%Ti
    tau_r = r'$\tau_{r}$=%i'%Tr
    s, i, r = census
    title = f'{tau_i}\t{tau_r}\t S={s:.2f} \t I={i:.2f} \t R={r:.2f}'
    pdg.axes.set_title(title)
    _pop_image(pdg.axes, population, Ti, Tr)
    pdg.fig.tight_layout()
    pdg.canvas.draw()
    pdg.show()
    return pdg

def _timeSeriesLines(axes, data):
    l, = axes.plot(data[:,0], data[:,1], 'g-', lw=2, label='Susceptible')
    m, = axes.plot(data[:,0], data[:,2], 'r-', lw=2, label='Infected'   )
    n, = axes.plot(data[:,0], data[:,3], 'k-', lw=2, label='Refractory' )
    return [ l, m, n ]

def _sirTitle(t,s,i,r):
    return f'Time={t}      S={s:.2f}   I={i:.2f}   R={r:.2f}'

def plotTimeSeries(data):
    pdg = PlotDialog(6.5, 5, 'Time series')
    _timeSeriesLines(pdg.axes, data)
    pdg.axes.set_title( _sirTitle(*data[-1,:]) )
    pdg.axes.legend()
    pdg.fig.tight_layout()
    pdg.canvas.draw()
    pdg.show()
    return pdg


class AnimDialog(qt.QDialog):
    def __init__(self, nbrs, pop, Ti, Tr):
        super().__init__()
        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.playPause = qt.QPushButton("||")
        self.playPause.clicked.connect(self.onClick)

        self.axes = list()
        self.axes.append( self.fig.add_subplot(121) )
        self.axes.append( self.fig.add_subplot(222) )
        self.axes.append( self.fig.add_subplot(224) )
        self.im = _pop_image(self.axes[0], pop, Ti, Tr)
        self.ln = _timeSeriesLines(self.axes[1], np.zeros(shape=(0,6)))
        self.ln.append( *self.axes[2].plot([],[],lw=2) )
        self._title(Ti,Tr,nbrs)

        self._set_all_layouts()

    def _title(self, Ti, Tr, nbrs):
        tau_i = r'$\tau_{i}$=%i'%Ti
        tau_r = r'$\tau_{r}$=%i'%Tr
        nbrs = f'nbrs={nbrs}'
        self.axes[1].set_title(f'Time Series\t{tau_i}\t{tau_r}\t{nbrs}')
        ham_dist_phase = r'|$\frac{1}{N}\Sigma e^{i\phi}$|'
        self.axes[2].set_title(f'Order Parameter = {ham_dist_phase}')

    def _update(self, i):
        pop, data = self.updates_data()
        self.im.set_data(pop)
        self.ln[0].set_data(data[:,0], data[:,1])
        self.ln[1].set_data(data[:,0], data[:,2])
        self.ln[2].set_data(data[:,0], data[:,3])
        self.ln[3].set_data(data[:,0], data[:,4])
        t0, (t, fs, fi, fr, _) = data[0,0], data[-1]
        self.axes[0].set_title( _sirTitle(t, fs, fi, fr) )
        self.axes[1].set_xlim(t0, t+1)
        self.axes[2].set_xlim(t0, t+1)

    def animate(self, ti, tf, delay, updates_data):
        from matplotlib.animation import FuncAnimation
        self.updates_data = updates_data
        self.line_ani = FuncAnimation(self.fig, self._update, (tf-ti-1),
                                      interval=delay*1000, repeat=False)
        self.canvas.draw()

    def closeEvent(self, *args):
        self.line_ani.pause()

    def reject(self, *args):
        self.close()
        self.line_ani.pause()

    def onClick(self):
        if self.playPause.text()=='\u25ba':
            self.playPause.setText('||')
            self.line_ani.resume()
        else:
            self.playPause.setText('\u25ba')
            self.line_ani.pause()

    def _set_all_layouts(self, width=5, height=4):
        self.playPause.setStyleSheet('''
             font-size: 17px;
             background-color: white;
             border-style  : solid;
             border-width  : 2px;
             border-radius : 17px;
             border-color  : blue;
             max-width  : 30px;
             max-height : 30px;
             min-width  : 30px;
             min-height : 30px; ''')
        hl = qt.QHBoxLayout()
        hl.addStretch()
        hl.addWidget(self.playPause)
        hl.addWidget(self.toolbar)
        layout = qt.QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addLayout(hl)
        self.setLayout(layout)
        self.setWindowTitle('Time evolution animation')
        self.showMaximized() # self.resize(1200, 650)
        self.axes[1].set_ylim(0.0, 1.0)
        self.axes[1].legend(loc='upper right')
        self.axes[2].set_ylim(-1, 3)
        self.fig.tight_layout()
        self.show()
